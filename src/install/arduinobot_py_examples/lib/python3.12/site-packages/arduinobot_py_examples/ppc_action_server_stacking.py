#!/usr/stack/env python3

import math
import rclpy
from rclpy.node import Node
import serial
import time

from geometry_msgs.msg import PoseStamped, Pose, Quaternion
from moveit_msgs.msg import MotionPlanRequest, Constraints, PositionConstraint, PlanningScene, CollisionObject
from moveit_msgs.action import MoveGroup
from cube_msgs.action import PickAndPlace
from rclpy.action import ActionServer, ActionClient
from shape_msgs.msg import SolidPrimitive
from tf2_ros import Buffer, TransformListener, LookupException, ConnectivityException, ExtrapolationException


class PickAndPlaceServer(Node):
    def __init__(self):
        super().__init__('pick_and_place_server')

        self.move_group_client = ActionClient(self, MoveGroup, '/move_action')
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.pick_and_place_action_server = ActionServer(
            self,
            PickAndPlace,
            'pick_and_place',
            self.execute_callback)

        try:
            self.arduino = serial.Serial('/dev/ttyACM0', 57600, timeout=1)
            time.sleep(2)
            self.arduino.write(b'DeskMod\n')
            time.sleep(0.1)
            self.get_logger().info("Connected to Arduino")
        except (serial.SerialException, OSError) as e:
            self.get_logger().error(f'Serial error: {e}')
            self.arduino = None

        self.move_group_client.wait_for_server()

        self.scene_publisher = self.create_publisher(PlanningScene, '/planning_scene', 10)
        self.add_workspace_obstacles()

        self.gripper_value = 0
        self.pick_z = 0.01
        self.approach_z = 0.20
        
        self.place_z = 0.01
        self.counter=0.0
      
        self.predefined_xyz_poses = {
            'red': {'x': 0.185, 'y': 0.125},
            'green': {'x': 0.185, 'y': 0.125},
            'blue': {'x': 0.185, 'y': 0.125},
        }

    def add_workspace_obstacles(self):

        planning_scene = PlanningScene()
        planning_scene.is_diff = True

        #Define boxes: each with unique size [x, y, z] and position [x, y, z] (center in world frame)
        boxes = [
            {'id': 'restricted_area_1', 'size': [1.0, 0.3, 1.0], 'pos': [0.82, 0.125, 0.5]},
            {'id': 'restricted_area_2', 'size': [1.0, 1.0, 0.1], 'pos': [-0.711, 0.1, 0.05]},
            {'id': 'restricted_area_3', 'size': [0.4, 0.2, 0.1], 'pos': [0.05, -0.70, 0.05]},
            {'id': 'restricted_area_4', 'size': [0.4, 0.2, 0.1], 'pos': [0.05, 0.39, 0.05]},
        ]

        for box_info in boxes:
            box = CollisionObject()
            box.id = box_info['id']
            box.header.frame_id = 'world'

            primitive = SolidPrimitive()
            primitive.type = SolidPrimitive.BOX
            primitive.dimensions = box_info['size']

            box_pose = Pose()
            box_pose.position.x = box_info['pos'][0]
            box_pose.position.y = box_info['pos'][1]
            box_pose.position.z = box_info['pos'][2]

            box.primitives.append(primitive)
            box.primitive_poses.append(box_pose)
            box.operation = CollisionObject.ADD

            planning_scene.world.collision_objects.append(box)

        self.scene_publisher.publish(planning_scene)
        self.get_logger().info("Added 4 restricted areas to the planning scene.")

    async def execute_callback(self, goal_handle):
        color = goal_handle.request.color.lower()
        if color not in self.predefined_xyz_poses:
            msg = f"No predefined stack pose for {color}"
            self.get_logger().warn(msg)
            goal_handle.abort()
            return PickAndPlace.Result(success=False, message=msg)

        x, y,z = goal_handle.request.target_pose.position.x, goal_handle.request.target_pose.position.y,goal_handle.request.target_pose.position.z
        stack_pose = self.predefined_xyz_poses[color]

        home_wrist_angle = self.compute_wrist_angle(0.0, 0.0,0.0)
        pick_wrist_angle = self.compute_wrist_angle(x, y,z)
        place_wrist_angle = 0

        feedback = PickAndPlace.Feedback()

        def send_feedback(status):
            feedback.status = status
            goal_handle.publish_feedback(feedback)
            self.get_logger().info(f'📣 {status}')

        send_feedback(f'Planning pick for {color} cube at ({x:.3f}, {y:.3f})')


        def plan_and_wait(x, y, z, wrist_angle):
            pose_target = PoseStamped()
            pose_target.header.frame_id = 'world'
            pose_target.pose.position.x = x
            pose_target.pose.position.y = y
            pose_target.pose.position.z = z

            plan_request = MotionPlanRequest()
            plan_request.group_name = 'arm'
            plan_request.allowed_planning_time = 0.3  # increased for reliability
            plan_request.num_planning_attempts = 2000
            plan_request.goal_constraints.append(self.create_pose_constraint(pose_target))
            plan_request.max_velocity_scaling_factor = 1.0
            plan_request.max_acceleration_scaling_factor = 1.0

            move_goal = MoveGroup.Goal()
            move_goal.request = plan_request
            move_goal.planning_options.plan_only = False

            future = self.move_group_client.send_goal_async(move_goal)
            rclpy.spin_until_future_complete(self, future)
            goal_result = future.result()
            if not goal_result.accepted:
                raise RuntimeError("MoveGroup goal rejected.")

            result_future = goal_result.get_result_async()
            rclpy.spin_until_future_complete(self, result_future)
            result = result_future.result().result
            if result.error_code.val != 1:
                raise RuntimeError("MoveGroup planning failed.")

            trajectory = result.planned_trajectory.joint_trajectory
            joint_names = trajectory.joint_names

            if not trajectory.points:
                raise RuntimeError("Planned trajectory has no points.")

            for point in trajectory.points:
                positions = point.positions
                self.send_to_arduino(joint_names, positions, wrist_angle)
                time.sleep(0.05)  # adjust delay as needed for smoothness


        try:


            
            send_feedback("Moving to home position")
            plan_and_wait(0.0, 0.0, self.approach_z, home_wrist_angle)

            send_feedback("Approaching pick position")
            plan_and_wait(x, y, self.approach_z-0.16, pick_wrist_angle)

            send_feedback("Descending to pick")
            plan_and_wait(x, y, self.pick_z, pick_wrist_angle)

            send_feedback("Grasping cube")
            self.send_gripper_command(60)
            plan_and_wait(x, y, self.pick_z, pick_wrist_angle)

            send_feedback("Lifting cube")
            plan_and_wait(x-0.05, y, self.approach_z+0.05, pick_wrist_angle)

            if (y<=0.125):

                send_feedback("Centering Cube")
                plan_and_wait(0.105,y, self.approach_z+0.05, pick_wrist_angle)

            send_feedback("Moving to stack pose")
            plan_and_wait(stack_pose['x'], stack_pose['y'], self.approach_z, place_wrist_angle)

            send_feedback("Lowering to stack")
            plan_and_wait(stack_pose['x'], stack_pose['y'], self.place_z+(self.counter*0.03), place_wrist_angle)

            send_feedback("Releasing cube")
            self.send_gripper_command(0)
            plan_and_wait(stack_pose['x'], stack_pose['y'], self.place_z+(self.counter*0.03), place_wrist_angle)

            send_feedback("Retracting")
            plan_and_wait(stack_pose['x'], stack_pose['y'], self.approach_z, place_wrist_angle)

            send_feedback("Returning to home")
            plan_and_wait(0.0, 0.0, self.approach_z, home_wrist_angle)
            # stack_pose['counter']=stack_pose['counter']+1
            self.counter+=1
            send_feedback(f'The counter right now is {self.counter} ')
            

        except Exception as e:
            msg = f'❌ Pick and place failed: {str(e)}'
            self.get_logger().error(msg)
            goal_handle.abort()
            return PickAndPlace.Result(success=False, message=msg)

        goal_handle.succeed()
        return PickAndPlace.Result(success=True, message=f"{color.capitalize()} cube placed successfully.")

    def send_gripper_command(self, value):
        self.gripper_value = value
        self.get_logger().info(f'Gripper command value set: {value}')

    def send_to_arduino(self, joint_names, positions, wrist_angle):
        if not self.arduino or not self.arduino.is_open:
            self.get_logger().warn('Arduino not connected, skipping send.')
            return

        joint_map = dict(zip(joint_names, positions))
        joint_limits = [
            {'name': 'joint_one', 'lower': -1.57, 'upper': 1.57, 'reverse': True},
            {'name': 'joint_two', 'lower': -1.307, 'upper': 0.617, 'reverse': False},
            {'name': 'joint_three', 'lower': -1.57, 'upper': 1.57, 'reverse': True},
            {'name': 'joint_four', 'lower': -1.57, 'upper': 1.57, 'reverse': False},
            {'name': 'joint_five', 'lower': -1.57, 'upper': 1.57, 'reverse': False},
            {'name': 'joint_six', 'lower': 0, 'upper': 100, 'reverse': False},
        ]

        positions_out = []
        for joint in joint_limits:
            name = joint['name']
            if name == 'joint_six':
                positions_out.append(self.gripper_value)
            elif name == 'joint_five':
                wrist = int((wrist_angle - (-1.57)) * 100 / (1.57 + 1.57))
                wrist = max(0, min(100, wrist))
                positions_out.append(wrist)
            elif name in joint_map:
                val = joint_map[name]
                if joint['reverse']:
                    val = -val
                mapped = int((val - joint['lower']) * 100 / (joint['upper'] - joint['lower']))
                mapped = max(0, min(100, mapped))
                positions_out.append(mapped)
            else:
                positions_out.append(0)

        command = f"D,{','.join(str(v) for v in positions_out)},AX\n"
        self.get_logger().info(f'Sending: {command.strip()}')

        try:
            self.arduino.write(command.encode())
            self.arduino.flush()
        except serial.SerialException as e:
            self.get_logger().error(f'Serial error: {e}')

    def compute_wrist_angle(self, x, y,z):
        base_x, base_y = 0.0, 0.0
        try:
            trans = self.tf_buffer.lookup_transform('world', 'base_link', rclpy.time.Time())
            base_x, base_y = trans.transform.translation.x, trans.transform.translation.y
        except (LookupException, ConnectivityException, ExtrapolationException):
            pass
        dx, dy = x - base_x, y - base_y
        cube_rotation=z

        if (cube_rotation>=45):
            cube_rotation=(cube_rotation-45)
            angle=(math.atan2(dy, dx)-math.radians(cube_rotation))
        else:
            angle=(math.atan2(dy, dx)+math.radians(cube_rotation))
        return angle

    def create_pose_constraint(self, pose_stamped):
        constraints = Constraints()
        pos_constraint = PositionConstraint()
        pos_constraint.header = pose_stamped.header
        pos_constraint.link_name = 'ik_frame'
        primitive = SolidPrimitive()
        primitive.type = SolidPrimitive.BOX
        primitive.dimensions = [0.001, 0.001, 0.001]
        pos_constraint.constraint_region.primitives.append(primitive)
        pos_constraint.constraint_region.primitive_poses.append(pose_stamped.pose)
        pos_constraint.weight = 1.0
        constraints.position_constraints.append(pos_constraint)
        return constraints


def main(args=None):
    rclpy.init(args=args)
    node = PickAndPlaceServer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()











