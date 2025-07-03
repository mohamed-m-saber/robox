#!/usr/bin/env python3

import math
import rclpy
from rclpy.node import Node
import serial
import time

from geometry_msgs.msg import PoseStamped, Quaternion
from moveit_msgs.msg import MotionPlanRequest, Constraints, PositionConstraint
from moveit_msgs.action import MoveGroup
from builtin_interfaces.msg import Duration
from control_msgs.action import FollowJointTrajectory
from rclpy.action import ActionClient
from tf2_ros import Buffer, TransformListener, LookupException, ConnectivityException, ExtrapolationException
from shape_msgs.msg import SolidPrimitive


class MoveGroupMotionPlanner(Node):
    def __init__(self):
        super().__init__('move_group_motion_planner_client')

        # Action clients
        self.move_group_client = ActionClient(self, MoveGroup, '/move_action')
        self.trajectory_client = ActionClient(self, FollowJointTrajectory, '/arm_controller/follow_joint_trajectory')

        # TF listener
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        # Serial setup
        try:
            self.arduino = serial.Serial('/dev/ttyACM1', 57600, timeout=1)
            time.sleep(2)
            self.arduino.write(b'DeskMod\n')
            time.sleep(0.1)
            self.get_logger().info("✅ Connected to Arduino")
        except (serial.SerialException, OSError) as e:
            self.get_logger().error(f"❌ Failed to connect to Arduino: {e}")
            self.arduino = None

        # Wait for action servers
        self.get_logger().info('⏳ Waiting for /move_action server...')
        self.move_group_client.wait_for_server()
        self.get_logger().info('✅ /move_action server available.')

        # Example target position
        x_target, y_target = 0.105, 0.125
        cube_yaw = 0.0

        z_approach = 0.18
        z_pick = 0.01

        # Compute wrist angle based on cube location
        wrist_angle = self.compute_wrist_angle(x_target, y_target, cube_yaw)

        # Plan and move to approach pose
        self.plan_and_send(x_target, y_target, z_approach, wrist_angle)

        # Plan and move to pick pose
        self.plan_and_send(x_target, y_target, z_pick, wrist_angle)

    def plan_and_send(self, x, y, z, wrist_angle):
        pose_target = PoseStamped()
        pose_target.header.frame_id = 'world'
        pose_target.pose.position.x = x
        pose_target.pose.position.y = y
        pose_target.pose.position.z = z
        pose_target.pose.orientation = self.quaternion_from_yaw(wrist_angle)

        plan_request = MotionPlanRequest()
        plan_request.group_name = 'arm'
        plan_request.allowed_planning_time = 5.0
        plan_request.num_planning_attempts = 20
        plan_request.goal_constraints.append(self.create_pose_constraint(pose_target))
        plan_request.max_velocity_scaling_factor = 1.0
        plan_request.max_acceleration_scaling_factor = 1.0

        move_goal = MoveGroup.Goal()
        move_goal.request = plan_request
        move_goal.planning_options.plan_only = False

        self.get_logger().info(f'📌 Planning to ({x:.3f}, {y:.3f}, {z:.3f}) wrist: {math.degrees(wrist_angle):.1f}°...')
        send_goal_future = self.move_group_client.send_goal_async(move_goal)
        rclpy.spin_until_future_complete(self, send_goal_future)
        goal_handle = send_goal_future.result()

        if not goal_handle.accepted:
            self.get_logger().error('❌ MoveGroup goal was rejected.')
            return

        self.get_logger().info('✅ Plan goal accepted. Waiting for result...')
        result_future = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(self, result_future)
        result = result_future.result().result

        if result.error_code.val != 1:
            self.get_logger().error(f'❌ Planning failed with error code: {result.error_code.val}')
            return

        self.get_logger().info('✅ Plan computed successfully.')

        # Get the final joint positions
        trajectory = result.planned_trajectory.joint_trajectory
        final_point = trajectory.points[-1]
        joint_names = trajectory.joint_names
        positions = final_point.positions

        # Map and send via serial
        self.send_to_arduino(joint_names, positions)

    def send_to_arduino(self, joint_names, positions):
        if self.arduino and self.arduino.is_open:
            joint_map = dict(zip(joint_names, positions))

            # Same joint limits and reverse map as before
            joint_limits = [
                {'name': 'joint_one', 'lower': -1.57, 'upper': 1.57, 'reverse': True},
                {'name': 'joint_two', 'lower': -1.307, 'upper': 0.617, 'reverse': False},
                {'name': 'joint_three', 'lower': -1.57, 'upper': 1.57, 'reverse': True},
                {'name': 'joint_four', 'lower': -1.57, 'upper': 1.57, 'reverse': False},
                {'name': 'joint_five', 'lower': -1.57, 'upper': 1.57, 'reverse': False},
                {'name': 'joint_six', 'lower': -1.57, 'upper': 1.57, 'reverse': False},
            ]

            positions_out = []
            joint_one_value = None

            for joint in joint_limits:
                name = joint['name']
                if name == 'joint_six':
                    positions_out.append(0)
                elif name == 'joint_five':
                    if joint_one_value is not None:
                        positions_out.append(100 - joint_one_value)
                    else:
                        positions_out.append(0)
                elif name in joint_map:
                    val = joint_map[name]
                    if joint['reverse']:
                        val = -val
                    mapped = int((val - joint['lower']) * 100 / (joint['upper'] - joint['lower']))
                    mapped = max(0, min(100, mapped))
                    if name == 'joint_one':
                        joint_one_value = mapped
                    positions_out.append(mapped)
                else:
                    positions_out.append(0)

            command = f"D,{','.join(str(v) for v in positions_out)},AX\n"
            self.get_logger().info(f'📤 Sending final positions: {command.strip()}')
            try:
                self.arduino.write(command.encode())
                self.arduino.flush()
            except serial.SerialException as e:
                self.get_logger().error(f'❌ Serial error: {e}')

    def compute_wrist_angle(self, cube_x, cube_y, cube_yaw):
        base_x, base_y = self.get_base_position()
        dx = cube_x - base_x
        dy = cube_y - base_y
        angle = math.atan2(dy, dx)
        wrist_angle = (angle + cube_yaw) % (2 * math.pi)
        wrist_angle = (wrist_angle + math.pi) % (2 * math.pi) - math.pi
        self.get_logger().info(f'🧭 Wrist angle: {math.degrees(wrist_angle):.1f}°')
        return wrist_angle

    def get_base_position(self):
        try:
            trans = self.tf_buffer.lookup_transform('world', 'base_link', rclpy.time.Time())
            x = trans.transform.translation.x
            y = trans.transform.translation.y
        except (LookupException, ConnectivityException, ExtrapolationException):
            x, y = 0.0, 0.0
        return x, y

    def create_pose_constraint(self, pose_stamped):
        constraints = Constraints()
        pos_constraint = PositionConstraint()
        pos_constraint.header = pose_stamped.header
        pos_constraint.link_name = 'ik_frame'
        pos_constraint.target_point_offset.x = 0.0
        pos_constraint.target_point_offset.y = 0.0
        pos_constraint.target_point_offset.z = 0.0

        primitive = SolidPrimitive()
        primitive.type = SolidPrimitive.BOX
        primitive.dimensions = [0.01, 0.01, 0.01]
        pos_constraint.constraint_region.primitives.append(primitive)
        pos_constraint.constraint_region.primitive_poses.append(pose_stamped.pose)
        pos_constraint.weight = 1.0
        constraints.position_constraints.append(pos_constraint)
        return constraints

    def quaternion_from_yaw(self, yaw):
        q = Quaternion()
        q.x = 0.0
        q.y = 0.0
        q.z = math.sin(yaw / 2.0)
        q.w = math.cos(yaw / 2.0)
        return q


def main(args=None):
    rclpy.init(args=args)
    node = MoveGroupMotionPlanner()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()











# #!/usr/bin/env python3

# import math
# import rclpy
# from rclpy.node import Node
# import serial
# import time

# from geometry_msgs.msg import PoseStamped, Quaternion
# from moveit_msgs.msg import MotionPlanRequest, Constraints, PositionConstraint
# from moveit_msgs.action import MoveGroup
# from rclpy.action import ActionClient
# from cube_msgs.msg import ColorPoseStamped
# from shape_msgs.msg import SolidPrimitive
# from tf2_ros import Buffer, TransformListener, LookupException, ConnectivityException, ExtrapolationException


# class MotionPlannerPickAndPlace(Node):
#     def __init__(self):
#         super().__init__('motion_planner_pick_and_place')

#         self.move_group_client = ActionClient(self, MoveGroup, '/move_action')
#         self.tf_buffer = Buffer()
#         self.tf_listener = TransformListener(self.tf_buffer, self)

#         try:
#             self.arduino = serial.Serial('/dev/ttyACM1', 57600, timeout=1)
#             time.sleep(2)
#             self.arduino.write(b'DeskMod\n')
#             time.sleep(0.1)
#             self.get_logger().info("✅ Connected to Arduino")
#         except (serial.SerialException, OSError) as e:
#             self.get_logger().error(f"❌ Serial error: {e}")
#             self.arduino = None

#         self.move_group_client.wait_for_server()

#         self.predefined_xyz_poses = {
#             'red': {'x': -0.07348, 'y': 0.407},
#             'green': {'x': 0.3, 'y': 0.5},
#             'blue': {'x': -0.2, 'y': 0.4},
#         }

#         self.create_subscription(ColorPoseStamped, '/detected_color_pose', self.color_pose_callback, 10)
#         self.get_logger().info('✅ MotionPlannerPickAndPlace ready.')

#         self.current_color = None

#     def color_pose_callback(self, msg):
#         color = msg.color.lower()
#         if color not in self.predefined_xyz_poses:
#             self.get_logger().warn(f'⚠️ No predefined bin pose for {color}')
#             return

#         self.current_color = color
#         x, y = msg.pose.position.x, msg.pose.position.y
#         wrist_angle = self.compute_wrist_angle(x, y)

#         self.get_logger().info(f'🎨 Pick {color} cube at ({x:.3f}, {y:.3f})')

#         # Move to home pose first
#         self.plan_and_send(0.0, 0.0, 0.18, 0.0, lambda:
#             # Then move to cube approach
#             self.plan_and_send(x, y, 0.18, wrist_angle, lambda:
#                 # Then move to pick height
#                 self.plan_and_send(x, y, 0.01, wrist_angle, lambda:
#                     self.close_gripper_and_continue())))

#     def close_gripper_and_continue(self):
#         self.send_gripper_command(50)
#         time.sleep(1.0)

#         bin_pose = self.predefined_xyz_poses[self.current_color]
#         bin_x, bin_y = bin_pose['x'], bin_pose['y']
#         wrist_angle = self.compute_wrist_angle(bin_x, bin_y)

#         self.plan_and_send(bin_x, bin_y, 0.18, wrist_angle, lambda:
#             self.plan_and_send(bin_x, bin_y, 0.15, wrist_angle, lambda:
#                 self.open_gripper_and_go_home()))

#     def open_gripper_and_go_home(self):
#         self.send_gripper_command(100)
#         time.sleep(1.0)
#         self.get_logger().info('📌 Moving to home pose after drop.')
#         self.plan_and_send(0.0, 0.0, 0.18, 0.0)

#     def plan_and_send(self, x, y, z, wrist_angle, done_callback=None):
#         pose_target = PoseStamped()
#         pose_target.header.frame_id = 'world'
#         pose_target.pose.position.x = x
#         pose_target.pose.position.y = y
#         pose_target.pose.position.z = z
#         pose_target.pose.orientation = self.quaternion_from_yaw(wrist_angle)

#         plan_request = MotionPlanRequest()
#         plan_request.group_name = 'arm'
#         plan_request.allowed_planning_time = 5.0
#         plan_request.num_planning_attempts = 20
#         plan_request.goal_constraints.append(self.create_pose_constraint(pose_target))
#         plan_request.max_velocity_scaling_factor = 1.0
#         plan_request.max_acceleration_scaling_factor = 1.0

#         move_goal = MoveGroup.Goal()
#         move_goal.request = plan_request
#         move_goal.planning_options.plan_only = False

#         self.get_logger().info(f'📌 Move to ({x:.3f}, {y:.3f}, {z:.3f}) wrist: {math.degrees(wrist_angle):.1f}°...')
#         future = self.move_group_client.send_goal_async(move_goal)
#         future.add_done_callback(lambda f: self.goal_result_callback(f, done_callback))

#     def goal_result_callback(self, future, done_callback):
#         goal_handle = future.result()
#         if not goal_handle.accepted:
#             self.get_logger().error('❌ MoveGroup goal rejected.')
#             return

#         result_future = goal_handle.get_result_async()
#         result_future.add_done_callback(lambda f: self.execution_callback(f, done_callback))

#     def execution_callback(self, future, done_callback):
#         result = future.result().result
#         if result.error_code.val != 1:
#             self.get_logger().error('❌ Planning failed.')
#             return

#         self.get_logger().info('✅ Plan successful.')

#         if done_callback:
#             done_callback()

#     def send_gripper_command(self, value):
#         if self.arduino and self.arduino.is_open:
#             command = f'G,{value}\n'
#             try:
#                 self.arduino.write(command.encode())
#                 self.arduino.flush()
#                 self.get_logger().info(f'🤖 Gripper command value set: {value}')
#             except serial.SerialException as e:
#                 self.get_logger().error(f'❌ Serial error: {e}')

#     def compute_wrist_angle(self, x, y):
#         base_x, base_y = self.get_base_position()
#         dx, dy = x - base_x, y - base_y
#         return math.atan2(dy, dx)

#     def get_base_position(self):
#         try:
#             trans = self.tf_buffer.lookup_transform('world', 'base_link', rclpy.time.Time())
#             return trans.transform.translation.x, trans.transform.translation.y
#         except (LookupException, ConnectivityException, ExtrapolationException):
#             return 0.0, 0.0

#     def create_pose_constraint(self, pose_stamped):
#         constraints = Constraints()
#         pos_constraint = PositionConstraint()
#         pos_constraint.header = pose_stamped.header
#         pos_constraint.link_name = 'ik_frame'
#         primitive = SolidPrimitive()
#         primitive.type = SolidPrimitive.BOX
#         primitive.dimensions = [0.01, 0.01, 0.01]
#         pos_constraint.constraint_region.primitives.append(primitive)
#         pos_constraint.constraint_region.primitive_poses.append(pose_stamped.pose)
#         pos_constraint.weight = 1.0
#         constraints.position_constraints.append(pos_constraint)
#         return constraints

#     def quaternion_from_yaw(self, yaw):
#         q = Quaternion()
#         q.x = 0.0
#         q.y = 0.0
#         q.z = math.sin(yaw / 2.0)
#         q.w = math.cos(yaw / 2.0)
#         return q


# def main(args=None):
#     rclpy.init(args=args)
#     node = MotionPlannerPickAndPlace()
#     rclpy.spin(node)
#     node.destroy_node()
#     rclpy.shutdown()


# if __name__ == '__main__':
#     main()
