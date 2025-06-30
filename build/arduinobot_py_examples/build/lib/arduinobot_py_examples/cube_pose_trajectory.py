# # #!/usr/bin/env python3

# import math
# import rclpy
# from rclpy.node import Node
# import serial
# import time

# from geometry_msgs.msg import PoseStamped, Quaternion
# from moveit_msgs.msg import MotionPlanRequest, Constraints, PositionConstraint, RobotState
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
#             self.arduino = serial.Serial('/dev/ttyACM0', 57600, timeout=1)
#             time.sleep(2)
#             self.arduino.write(b'DeskMod\n')
#             time.sleep(0.1)
#             self.get_logger().info("Connected to Arduino")
#         except (serial.SerialException, OSError) as e:
#             self.get_logger().error(f'Serial error: {e}')
#             self.arduino = None

#         self.gripper_value = 0
#         self.last_pose = None
#         self.move_group_client.wait_for_server()

#         # Predefined bin poses (these will be cached)
#         self.predefined_xyz_poses = {
#             'red': {'x': -0.07348, 'y': 0.407},
#             # 'green': {'x': 0.3, 'y': 0.5},
#             # 'blue': {'x': -0.2, 'y': 0.4},
#             # 'yellow': {'x': 0.1, 'y': 0.3},      # Additional pose 1
#             # 'orange': {'x': -0.1, 'y': 0.35},    # Additional pose 2
#             # 'purple': {'x': 0.2, 'y': 0.45},     # Additional pose 3
#         }

#         # Pose cache for successful joint configurations
#         self.pose_cache = {}
#         self.bin_poses_cached = False

#         self.create_subscription(ColorPoseStamped, '/detected_color_pose', self.color_pose_callback, 10)
#         self.get_logger().info('MotionPlannerPickAndPlace ready.')

#         # State variables for current pick-and-place task
#         self.pick_pose = None
#         self.place_pose = None
#         self.home_wrist_angle = 0.0
#         self.pick_wrist_angle = 0.0
#         self.place_wrist_angle = 0.0
#         self.pick_z = 0.03
#         self.approach_z = 0.20
#         self.place_z = 0.15

#         # Cache bin poses on startup
#         self.cache_bin_poses()

#     def cache_bin_poses(self):
#         """Pre-cache all bin poses to speed up operations"""
#         self.get_logger().info('Caching bin poses...')
        
#         poses_to_cache = [
#             # Home position
#             (0.0, 0.0, self.approach_z, 0.0, 'home'),
#             # All bin positions at place height
#             *[(pose['x'], pose['y'], self.place_z, 0.0, f"bin_{color}") 
#               for color, pose in self.predefined_xyz_poses.items()],
#             # All bin positions at approach height  
#             *[(pose['x'], pose['y'], self.approach_z, 0.0, f"approach_{color}") 
#               for color, pose in self.predefined_xyz_poses.items()]
#         ]
        
#         self.cache_index = 0
#         self.poses_to_cache = poses_to_cache
#         self._cache_next_pose()

#     def _cache_next_pose(self):
#         """Cache poses one by one to avoid overwhelming the system"""
#         if self.cache_index >= len(self.poses_to_cache):
#             self.get_logger().info('Bin pose caching complete!')
#             self.bin_poses_cached = True
#             return

#         x, y, z, wrist, label = self.poses_to_cache[self.cache_index]
#         self.get_logger().info(f'Caching pose {self.cache_index + 1}/{len(self.poses_to_cache)}: {label}')
#         self._plan_for_cache(x, y, z, wrist, label)

#     def _plan_for_cache(self, x, y, z, wrist_angle, label):
#         """Plan a pose specifically for caching"""
#         pose_target = PoseStamped()
#         pose_target.header.frame_id = 'world'
#         pose_target.pose.position.x = x
#         pose_target.pose.position.y = y
#         pose_target.pose.position.z = z
#         pose_target.pose.orientation = self.quaternion_from_yaw(wrist_angle)

#         plan_request = MotionPlanRequest()
#         plan_request.group_name = 'arm'
#         plan_request.allowed_planning_time = 2.0  # More time for caching
#         plan_request.num_planning_attempts = 10
#         plan_request.planner_id = 'RRTConnect'
        
#         plan_request.start_state = RobotState()
#         plan_request.start_state.is_diff = True
        
#         constraints = self._create_adaptive_constraints(pose_target, [0.05, 0.05, 0.05])
#         plan_request.goal_constraints.append(constraints)
        
#         plan_request.max_velocity_scaling_factor = 0.5
#         plan_request.max_acceleration_scaling_factor = 0.5

#         move_goal = MoveGroup.Goal()
#         move_goal.request = plan_request
#         move_goal.planning_options.plan_only = True  # Only plan, don't execute

#         future = self.move_group_client.send_goal_async(move_goal)
#         future.add_done_callback(lambda f: self._cache_goal_callback(f, x, y, z, wrist_angle, label))

#     def _cache_goal_callback(self, future, x, y, z, wrist_angle, label):
#         """Handle caching goal results"""
#         goal_handle = future.result()
#         if not goal_handle.accepted:
#             self.get_logger().warn(f'Cache planning rejected for {label}')
#             self.cache_index += 1
#             self._cache_next_pose()
#             return

#         result_future = goal_handle.get_result_async()
#         result_future.add_done_callback(lambda f: self._cache_result_callback(f, x, y, z, wrist_angle, label))

#     def _cache_result_callback(self, future, x, y, z, wrist_angle, label):
#         """Store successful cache results"""
#         result = future.result().result
#         if result.error_code.val == 1:  # Success
#             trajectory = result.planned_trajectory.joint_trajectory
#             final_positions = trajectory.points[-1].positions
#             joint_names = trajectory.joint_names
            
#             pose_key = f"{x:.2f},{y:.2f},{z:.2f},{wrist_angle:.2f}"
#             self.pose_cache[pose_key] = {
#                 'names': joint_names,
#                 'positions': final_positions,
#                 'label': label
#             }
#             self.get_logger().info(f'Cached pose: {label}')
#         else:
#             self.get_logger().warn(f'Failed to cache pose: {label}')

#         self.cache_index += 1
#         self._cache_next_pose()

#     def color_pose_callback(self, msg):
#         if not self.bin_poses_cached:
#             self.get_logger().warn('Bin poses not yet cached, waiting...')
#             return

#         color = msg.color.lower()
#         if color not in self.predefined_xyz_poses:
#             self.get_logger().warn(f'No predefined bin pose for {color}')
#             return

#         x, y = msg.pose.position.x, msg.pose.position.y
#         bin_pose = self.predefined_xyz_poses[color]

#         self.pick_pose = (x, y)
#         self.place_pose = (bin_pose['x'], bin_pose['y'])
#         self.home_wrist_angle = self.compute_wrist_angle(0.0, 0.0)
#         self.pick_wrist_angle = self.compute_wrist_angle(x, y)
#         self.place_wrist_angle = 0

#         self.get_logger().info(f'Pick {color} cube at ({x:.3f}, {y:.3f})')

#         self.plan_and_send(0.0, 0.0, self.approach_z, self.home_wrist_angle, self.on_move_home_done)

#     def on_move_home_done(self):
#         x, y = self.pick_pose
#         self.plan_and_send(x, y, self.approach_z, self.pick_wrist_angle, self.on_approach_pick_done)

#     def on_approach_pick_done(self):
#         x, y = self.pick_pose
#         self.plan_and_send(x, y, self.pick_z, self.pick_wrist_angle, self.on_pick_done)

#     def on_pick_done(self):
#         self.send_gripper_command(33)
#         x, y = self.pick_pose
#         self.plan_and_send(x, y, self.pick_z, self.pick_wrist_angle, self.on_lift_pick_done)

#     def on_lift_pick_done(self):
#         bin_x, bin_y = self.place_pose
#         self.plan_and_send(bin_x, bin_y, self.approach_z, self.place_wrist_angle, self.on_approach_place_done)

#     def on_approach_place_done(self):
#         bin_x, bin_y = self.place_pose
#         self.plan_and_send(bin_x, bin_y, self.place_z, self.place_wrist_angle, self.on_place_done)

#     def on_place_done(self):
#         self.send_gripper_command(0)
#         bin_x, bin_y = self.place_pose
#         self.plan_and_send(bin_x, bin_y, self.place_z, self.place_wrist_angle, self.on_retract_place_done)

#     def on_retract_place_done(self):
#         self.plan_and_send(0.0, 0.0, self.approach_z, self.home_wrist_angle)

#     def plan_and_send(self, x, y, z, wrist_angle, done_callback=None):
#         """Adaptive planning with caching"""
#         self.last_pose = (x, y, z, wrist_angle)
        
#         # Check cache first
#         pose_key = f"{x:.2f},{y:.2f},{z:.2f},{wrist_angle:.2f}"
#         if pose_key in self.pose_cache:
#             self.get_logger().info(f'Using cached pose: {self.pose_cache[pose_key]["label"]}')
#             cached_joints = self.pose_cache[pose_key]
#             self.send_to_arduino(cached_joints['names'], cached_joints['positions'])
#             if done_callback:
#                 done_callback()
#             return
        
#         # Try different planning strategies in order of speed
#         planning_configs = [
#             # Fast attempt - tight constraints
#             {
#                 'time': 0.3,
#                 'attempts': 1,
#                 'tolerance': [0.02, 0.02, 0.02],
#                 'planner': 'RRTConnect'
#             },
#             # Medium attempt - relaxed constraints  
#             {
#                 'time': 0.8,
#                 'attempts': 3,
#                 'tolerance': [0.05, 0.05, 0.05],
#                 'planner': 'RRTConnect'
#             },
#             # Fallback - very relaxed
#             {
#                 'time': 2.0,
#                 'attempts': 5,
#                 'tolerance': [0.1, 0.1, 0.1],
#                 'planner': 'BiTRRT'
#             }
#         ]
        
#         self._try_planning_with_config(x, y, z, wrist_angle, planning_configs, 0, done_callback)

#     def _try_planning_with_config(self, x, y, z, wrist_angle, configs, config_index, done_callback):
#         if config_index >= len(configs):
#             self.get_logger().error('All planning attempts failed!')
#             return
        
#         config = configs[config_index]
        
#         pose_target = PoseStamped()
#         pose_target.header.frame_id = 'world'
#         pose_target.pose.position.x = x
#         pose_target.pose.position.y = y
#         pose_target.pose.position.z = z
#         pose_target.pose.orientation = self.quaternion_from_yaw(wrist_angle)

#         plan_request = MotionPlanRequest()
#         plan_request.group_name = 'arm'
#         plan_request.allowed_planning_time = config['time']
#         plan_request.num_planning_attempts = config['attempts']
#         plan_request.planner_id = config['planner']
        
#         # Current state for better planning
#         plan_request.start_state = RobotState()
#         plan_request.start_state.is_diff = True
        
#         # Create constraints with current tolerance
#         constraints = self._create_adaptive_constraints(pose_target, config['tolerance'])
#         plan_request.goal_constraints.append(constraints)
        
#         plan_request.max_velocity_scaling_factor = 0.5
#         plan_request.max_acceleration_scaling_factor = 0.5

#         move_goal = MoveGroup.Goal()
#         move_goal.request = plan_request
#         move_goal.planning_options.plan_only = False

#         self.get_logger().info(f'Planning attempt {config_index + 1}: ({x:.3f}, {y:.3f}, {z:.3f}) - {config["time"]}s timeout')
        
#         future = self.move_group_client.send_goal_async(move_goal)
#         future.add_done_callback(
#             lambda f: self._adaptive_goal_callback(f, x, y, z, wrist_angle, configs, config_index, done_callback)
#         )

#     def _adaptive_goal_callback(self, future, x, y, z, wrist_angle, configs, config_index, done_callback):
#         goal_handle = future.result()
#         if not goal_handle.accepted:
#             self.get_logger().warn(f'Planning attempt {config_index + 1} rejected, trying next...')
#             # Try next configuration
#             self._try_planning_with_config(x, y, z, wrist_angle, configs, config_index + 1, done_callback)
#             return

#         result_future = goal_handle.get_result_async()
#         result_future.add_done_callback(
#             lambda f: self._adaptive_execution_callback(f, x, y, z, wrist_angle, configs, config_index, done_callback)
#         )

#     def _adaptive_execution_callback(self, future, x, y, z, wrist_angle, configs, config_index, done_callback):
#         result = future.result().result
#         if result.error_code.val != 1:
#             self.get_logger().warn(f'Planning attempt {config_index + 1} failed, trying next...')
#             # Try next configuration
#             self._try_planning_with_config(x, y, z, wrist_angle, configs, config_index + 1, done_callback)
#             return

#         self.get_logger().info(f'Planning successful on attempt {config_index + 1}!')
#         trajectory = result.planned_trajectory.joint_trajectory
#         final_positions = trajectory.points[-1].positions
#         joint_names = trajectory.joint_names

#         # Cache successful pose for future use
#         pose_key = f"{x:.2f},{y:.2f},{z:.2f},{wrist_angle:.2f}"
#         if pose_key not in self.pose_cache:
#             self.pose_cache[pose_key] = {
#                 'names': joint_names,
#                 'positions': final_positions,
#                 'label': f'runtime_{pose_key}'
#             }

#         self.send_to_arduino(joint_names, final_positions)

#         if done_callback:
#             done_callback()

#     def _create_adaptive_constraints(self, pose_stamped, tolerance):
#         constraints = Constraints()
#         pos_constraint = PositionConstraint()
#         pos_constraint.header = pose_stamped.header
#         pos_constraint.link_name = 'ik_frame'
#         primitive = SolidPrimitive()
#         primitive.type = SolidPrimitive.BOX
#         primitive.dimensions = tolerance  # Use adaptive tolerance
#         pos_constraint.constraint_region.primitives.append(primitive)
#         pos_constraint.constraint_region.primitive_poses.append(pose_stamped.pose)
#         pos_constraint.weight = 1.0
#         constraints.position_constraints.append(pos_constraint)
#         return constraints

#     def send_to_arduino(self, joint_names, positions):
#         if not self.arduino or not self.arduino.is_open:
#             self.get_logger().warn('Arduino not connected, skipping send.')
#             return

#         joint_map = dict(zip(joint_names, positions))
#         joint_limits = [
#             {'name': 'joint_one', 'lower': -1.57, 'upper': 1.57, 'reverse': True},
#             {'name': 'joint_two', 'lower': -1.307, 'upper': 0.617, 'reverse': False},
#             {'name': 'joint_three', 'lower': -1.57, 'upper': 1.57, 'reverse': True},
#             {'name': 'joint_four', 'lower': -1.57, 'upper': 1.57, 'reverse': False},
#             {'name': 'joint_five', 'lower': -1.57, 'upper': 1.57, 'reverse': False},
#             {'name': 'joint_six', 'lower': 0, 'upper': 100, 'reverse': False},
#         ]

#         positions_out = []
#         joint_one_value = None

#         for joint in joint_limits:
#             name = joint['name']
#             if name == 'joint_six':
#                 positions_out.append(self.gripper_value)
#             elif name in joint_map:
#                 val = joint_map[name]
#                 if joint['reverse']:
#                     val = -val
#                 mapped = int((val - joint['lower']) * 100 / (joint['upper'] - joint['lower']))
#                 mapped = max(0, min(100, mapped))
#                 if name == 'joint_one':
#                     joint_one_value = mapped
#                 positions_out.append(mapped)
#             else:
#                 positions_out.append(0)

#         command = f"D,{','.join(str(v) for v in positions_out)},AX\n"
#         self.get_logger().info(f'Sending: {command.strip()}')

#         try:
#             self.arduino.write(command.encode())
#             self.arduino.flush()
#         except serial.SerialException as e:
#             self.get_logger().error(f'Serial error: {e}')

#     def send_gripper_command(self, value):
#         self.gripper_value = value
#         self.get_logger().info(f'Gripper command value set: {value}')

#     def compute_wrist_angle(self, x, y):
#         base_x, base_y = self.get_base_position()
#         dx, dy = x - base_x, y - base_y
#         return 0  # or math.atan2(dy, dx)

#     def get_base_position(self):
#         try:
#             trans = self.tf_buffer.lookup_transform('world', 'base_link', rclpy.time.Time())
#             return trans.transform.translation.x, trans.transform.translation.y
#         except (LookupException, ConnectivityException, ExtrapolationException):
#             return 0.0, 0.0

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








#!/usr/bin/env python3

import math
import rclpy
from rclpy.node import Node
import serial
import time

from geometry_msgs.msg import PoseStamped, Quaternion
from moveit_msgs.msg import MotionPlanRequest, Constraints, PositionConstraint
from moveit_msgs.action import MoveGroup
from rclpy.action import ActionClient
from cube_msgs.msg import ColorPoseStamped
from shape_msgs.msg import SolidPrimitive
from tf2_ros import Buffer, TransformListener, LookupException, ConnectivityException, ExtrapolationException

class MotionPlannerPickAndPlace(Node):
    def __init__(self):
        super().__init__('motion_planner_pick_and_place')

        self.move_group_client = ActionClient(self, MoveGroup, '/move_action')
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        try:
            self.arduino = serial.Serial('/dev/ttyACM0', 57600, timeout=1)
            time.sleep(2)
            self.arduino.write(b'DeskMod\n')
            time.sleep(0.1)
            self.get_logger().info("Connected to Arduino")
        except (serial.SerialException, OSError) as e:
            self.get_logger().error(f'Serial error: {e}')
            self.arduino = None

        self.gripper_value = 0
        self.last_pose = None
        self.move_group_client.wait_for_server()

        self.predefined_xyz_poses = {
            'red': {'x': -0.07348, 'y': 0.407},
            'green': {'x': 0.3, 'y': 0.5},
            'blue': {'x': -0.2, 'y': 0.4},
        }

        self.create_subscription(ColorPoseStamped, '/detected_color_pose', self.color_pose_callback, 10)
        self.get_logger().info('MotionPlannerPickAndPlace ready.')

        # State variables for current pick-and-place task
        self.pick_pose = None
        self.place_pose = None
        self.home_wrist_angle = 0.0
        self.pick_wrist_angle = 0.0
        self.place_wrist_angle = 0.0
        self.pick_z=0.03
        self.approach_z=0.20
        self.place_z=0.15
    def color_pose_callback(self, msg):
        color = msg.color.lower()
        if color not in self.predefined_xyz_poses:
            self.get_logger().warn(f'No predefined bin pose for {color}')
            return

        x, y = msg.pose.position.x, msg.pose.position.y
        bin_pose = self.predefined_xyz_poses[color]

        self.pick_pose = (x, y)
        self.place_pose = (bin_pose['x'], bin_pose['y'])
        self.home_wrist_angle = self.compute_wrist_angle(0.0, 0.0)
        self.pick_wrist_angle = self.compute_wrist_angle(x, y)
        self.place_wrist_angle = self.compute_wrist_angle(bin_pose['x'], bin_pose['y'])

        self.get_logger().info(f'Pick {color} cube at ({x:.3f}, {y:.3f})')

        self.plan_and_send(0.0, 0.0, self.approach_z, self.home_wrist_angle, self.on_move_home_done)

    def on_move_home_done(self):
        x, y = self.pick_pose
        self.plan_and_send(x, y, self.approach_z-0.12, self.pick_wrist_angle, self.on_approach_pick_done)

    def on_approach_pick_done(self):
        x, y = self.pick_pose
        self.plan_and_send(x, y, self.pick_z, self.pick_wrist_angle, self.on_pick_done)

    def on_pick_done(self):
        self.send_gripper_command(33)
        x, y = self.pick_pose
        self.plan_and_send(x, y, self.pick_z, self.pick_wrist_angle, self.on_pick_done_2)

    def on_pick_done_2(self):
        x, y = self.pick_pose
        self.plan_and_send(x, y, self.approach_z, self.pick_wrist_angle, self.on_lift_pick_done)

    def on_lift_pick_done(self):
        bin_x, bin_y = self.place_pose
        self.plan_and_send(bin_x, bin_y, self.approach_z, 0, self.on_approach_place_done)

    def on_approach_place_done(self):
        bin_x, bin_y = self.place_pose
        self.plan_and_send(bin_x, bin_y, self.place_z, 0, self.on_place_done)

    def on_place_done(self):
        self.send_gripper_command(0)
        bin_x, bin_y = self.place_pose
        self.plan_and_send(bin_x, bin_y, self.place_z, 0, self.on_place_done_2)

    def on_place_done_2(self):
        bin_x, bin_y = self.place_pose
        self.plan_and_send(bin_x, bin_y, self.approach_z, 0, self.on_retract_place_done)

    def on_retract_place_done(self):
        self.plan_and_send(0.0, 0.0, self.approach_z, self.home_wrist_angle)

    def plan_and_send(self, x, y, z, wrist_angle, done_callback=None):
        self.last_pose = (x, y, z, wrist_angle)
        pose_target = PoseStamped()
        pose_target.header.frame_id = 'world'
        pose_target.pose.position.x = x
        pose_target.pose.position.y = y
        pose_target.pose.position.z = z
        #pose_target.pose.orientation = self.quaternion_from_yaw(wrist_angle)

        plan_request = MotionPlanRequest()
        plan_request.group_name = 'arm'
        plan_request.allowed_planning_time = 1.0
        plan_request.num_planning_attempts = 2000
        plan_request.goal_constraints.append(self.create_pose_constraint(pose_target))
        plan_request.max_velocity_scaling_factor = 1.0
        plan_request.max_acceleration_scaling_factor = 1.0

        move_goal = MoveGroup.Goal()
        move_goal.request = plan_request
        move_goal.planning_options.plan_only = False

        self.get_logger().info(f'Move to ({x:.3f}, {y:.3f}, {z:.3f}) wrist: {math.degrees(wrist_angle):.1f} degrees...')
        future = self.move_group_client.send_goal_async(move_goal)
        future.add_done_callback(lambda f: self.goal_result_callback(f, done_callback,wrist_angle))

    def goal_result_callback(self, future, done_callback,wrist_angle):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error('MoveGroup goal rejected.')
            return

        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(lambda f: self.execution_callback(f, done_callback,wrist_angle))

    def execution_callback(self, future, done_callback,wrist_angle):
        result = future.result().result
        if result.error_code.val != 1:
            self.get_logger().error('Planning failed.')
            return

        self.get_logger().info('Plan successful.')
        trajectory = result.planned_trajectory.joint_trajectory
        final_positions = trajectory.points[-1].positions
        joint_names = trajectory.joint_names

        self.send_to_arduino(joint_names, final_positions,wrist_angle)

        if done_callback:
            done_callback()

    def send_to_arduino(self, joint_names, positions,wrist_angle):
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
        joint_one_value = None

        for joint in joint_limits:
            name = joint['name']
            if name == 'joint_six':
                positions_out.append(self.gripper_value)
            elif name == 'joint_five':
                wrist = int((wrist_angle - (-1.57)) * 100 / (1.57 +1.57))
                wrist = max(0, min(100, wrist))
                positions_out.append(wrist)
                self.get_logger().info(f'Move to {wrist:.1f} xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
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
        self.get_logger().info(f'Sending: {command.strip()}')

        try:
            self.arduino.write(command.encode())
            self.arduino.flush()
        except serial.SerialException as e:
            self.get_logger().error(f'Serial error: {e}')

    def send_gripper_command(self, value):
        self.gripper_value = value
        self.get_logger().info(f'Gripper command value set: {value}')

    def compute_wrist_angle(self, x, y):
        base_x, base_y = self.get_base_position()
        dx, dy = x - base_x, y - base_y
        return  math.atan2(dy, dx)

    def get_base_position(self):
        try:
            trans = self.tf_buffer.lookup_transform('world', 'base_link', rclpy.time.Time())
            return trans.transform.translation.x, trans.transform.translation.y
        except (LookupException, ConnectivityException, ExtrapolationException):
            return 0.0, 0.0

    def create_pose_constraint(self, pose_stamped):
        constraints = Constraints()
        pos_constraint = PositionConstraint()
        pos_constraint.header = pose_stamped.header
        pos_constraint.link_name = 'ik_frame'
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
    node = MotionPlannerPickAndPlace()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
