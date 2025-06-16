# import rclpy
# from rclpy.node import Node
# from rclpy.action import ActionClient
# from rclpy.callback_groups import ReentrantCallbackGroup
# from sensor_msgs.msg import JointState
# from moveit_msgs.action import MoveGroup
# from moveit_msgs.msg import (
#     MotionPlanRequest,
#     PlanningOptions,
#     Constraints,
#     JointConstraint
# )
# from std_msgs.msg import Header
# import time

# class SimpleMoveItClient(Node):
#     def __init__(self):
#         super().__init__('simple_moveit_client')
#         self.callback_group = ReentrantCallbackGroup()
        
#         # Create action client for MoveGroup
#         self._action_client = ActionClient(self, MoveGroup, '/move_action')
        
#         # Joint states subscriber
#         self.joint_states = None
#         self.joint_sub = self.create_subscription(
#             JointState,
#             '/joint_states',
#             self.joint_state_callback,
#             10,
#             callback_group=self.callback_group
#         )
        
#         self.get_logger().info("Waiting for MoveGroup action server...")
#         self._action_client.wait_for_server()
#         self.get_logger().info("MoveGroup action server found!")
        
#         # Wait for joint states
#         self.get_logger().info("Waiting for joint states...")
#         timeout = 5.0
#         start_time = time.time()
#         while self.joint_states is None and time.time() - start_time < timeout:
#             rclpy.spin_once(self, timeout_sec=0.1)
#         if self.joint_states is None:
#             self.get_logger().error("No joint states received. Using default joint name.")
        
#         # Set up timer to send goal
#         self.timer = self.create_timer(3.0, self.send_goal)
        
#     def joint_state_callback(self, msg):
#         self.joint_states = msg
#         #self.get_logger().info(f"Received joint states for: {msg.name}")
        
#     def send_goal(self):
#         self.timer.cancel()  # Only send once
        
#         # Create motion plan request
#         goal_msg = MoveGroup.Goal()
        
#         # Set up the request
#         goal_msg.request = MotionPlanRequest()
#         goal_msg.request.group_name = "arm"  # Your planning group name
#         goal_msg.request.num_planning_attempts = 10
#         goal_msg.request.allowed_planning_time = 10.0
#         goal_msg.request.start_state.is_diff = True
        
#         # Create constraints
#         constraints = Constraints()
#         constraints.name = "joint_constraint"
        
#         # Joint constraint
#         joint_constraint = JointConstraint()
#         # Select joint name
#         if self.joint_states and self.joint_states.name:
#             joint_constraint.joint_name = self.joint_states.name[0]  # Use first joint
#             current_position = self.joint_states.position[0]
#             self.get_logger().info(f"Selected joint: {joint_constraint.joint_name}, "
#                                   f"current position: {current_position}")
#             # Set small movement within limits
#             joint_constraint.position = current_position + 0.1  # Small increment
#         else:
#             joint_constraint.joint_name = "joint1"  # Fallback
#             joint_constraint.position = 0.1
#             self.get_logger().warn("Using fallback joint name: joint1")
        
#         joint_constraint.tolerance_above = 0.01
#         joint_constraint.tolerance_below = 0.01
#         joint_constraint.weight = 1.0
        
#         # Log joint constraint
#         self.get_logger().info(f"Joint constraint: joint={joint_constraint.joint_name}, "
#                               f"position={joint_constraint.position}, "
#                               f"tolerance_above={joint_constraint.tolerance_above}, "
#                               f"tolerance_below={joint_constraint.tolerance_below}")
        
#         constraints.joint_constraints = [joint_constraint]
#         goal_msg.request.goal_constraints = [constraints]
        
#         # Planning options
#         goal_msg.planning_options = PlanningOptions()
#         goal_msg.planning_options.plan_only = False
        
#         self.get_logger().info("Sending goal to MoveGroup...")
        
#         # Send goal
#         try:
#             self._send_goal_future = self._action_client.send_goal_async(
#                 goal_msg,
#                 feedback_callback=self.feedback_callback
#             )
#             self._send_goal_future.add_done_callback(self.goal_response_callback)
#         except Exception as e:
#             self.get_logger().error(f"Failed to send goal: {e}")
        
#     def goal_response_callback(self, future):
#         try:
#             goal_handle = future.result()
#             if not goal_handle.accepted:
#                 self.get_logger().info('Goal rejected')
#                 return
#             self.get_logger().info('Goal accepted')
#             self._get_result_future = goal_handle.get_result_async()
#             self._get_result_future.add_done_callback(self.get_result_callback)
#         except Exception as e:
#             self.get_logger().error(f"Goal response error: {e}")
    
#     def get_result_callback(self, future):
#         try:
#             result = future.result().result
#             self.get_logger().info(f'Motion planning result: {result.error_code.val}')
#             if result.error_code.val == 1:
#                 self.get_logger().info('Motion completed successfully!')
#             else:
#                 self.get_logger().error(f'Motion failed with error code: {result.error_code.val}')
#         except Exception as e:
#             self.get_logger().error(f"Result callback error: {e}")
    
#     def feedback_callback(self, feedback_msg):
#         try:
#             feedback = feedback_msg.feedback
#             self.get_logger().info(f'Planning state: {feedback.state}')
#         except Exception as e:
#             self.get_logger().error(f"Feedback error: {e}")

# def main(args=None):
#     rclpy.init(args=args)
    
#     try:
#         node = SimpleMoveItClient()
#         rclpy.spin(node)
#     except KeyboardInterrupt:
#         pass
#     except Exception as e:
#         print(f"Error: {e}")
#     finally:
#         if 'node' in locals():
#             node.destroy_node()
#         rclpy.shutdown()

# if __name__ == '__main__':
#     main()



# import rclpy
# from rclpy.node import Node
# from geometry_msgs.msg import PoseStamped, Pose
# from moveit_msgs.action import MoveGroup
# from moveit_msgs.msg import MotionPlanRequest, Constraints, PositionConstraint, OrientationConstraint, BoundingVolume
# from moveit_msgs.msg import RobotState, PlanningOptions
# from shape_msgs.msg import SolidPrimitive
# from visualization_msgs.msg import Marker
# from rclpy.action import ActionClient
# from sensor_msgs.msg import JointState
# import time

# class MoveIt2Planner(Node):
#     def __init__(self):
#         super().__init__('simple_moveit_client')
        
#         # Action client for MoveGroup
#         self._action_client = ActionClient(self, MoveGroup, 'move_action')
#         self.get_logger().info("Waiting for MoveGroup action server...")
#         self._action_client.wait_for_server()
#         self.get_logger().info("MoveGroup action server found!")
        
#         # Publisher for visualization
#         self.marker_pub = self.create_publisher(Marker, 'workspace_visualization', 10)
        
#         # Wait a bit for everything to initialize
#         time.sleep(2.0)
#         self.send_pose_goal()

#     def send_pose_goal(self):
#         # ========== Simple Target Pose ==========
#         target_pose = PoseStamped()
#         target_pose.header.stamp = self.get_clock().now().to_msg()
#         target_pose.header.frame_id = "world"
        
#         # Conservative target within reach
#         target_pose.pose.position.x = 0.12
#         target_pose.pose.position.y = 0.0
#         target_pose.pose.position.z = 0.18
        
#         # Simple downward orientation (like RViz default)
#         target_pose.pose.orientation.x = -1.5
#         target_pose.pose.orientation.y = -1.5
#         target_pose.pose.orientation.z = -1.5
#         target_pose.pose.orientation.w = 0.0
        
#         self.visualize_target(target_pose)
#         self.get_logger().info(f"Target pose: x={target_pose.pose.position.x}, y={target_pose.pose.position.y}, z={target_pose.pose.position.z}")

#         # ========== Simple MotionPlanRequest ==========
#         request = MotionPlanRequest()
#         request.group_name = "arm"
#         request.num_planning_attempts = 10
#         request.allowed_planning_time = 10.0
#         request.max_velocity_scaling_factor = 0.1
#         request.max_acceleration_scaling_factor = 0.1
        
#         # Use current state as start (this is key!)
#         request.start_state.is_diff = True

#         # ========== Simple Goal Constraint ==========
#         # This mimics what RViz does - simple position and orientation constraints
#         constraints = Constraints()
        
#         # Position constraint with reasonable tolerance
#         pos_constraint = PositionConstraint()
#         pos_constraint.header = target_pose.header
#         pos_constraint.link_name = "wrist_link"
        
#         # Create bounding box instead of sphere (sometimes works better)
#         box = SolidPrimitive()
#         box.type = SolidPrimitive.BOX
#         box.dimensions = [0.02, 0.02, 0.02]  # 2cm tolerance in each direction

#         bounding_volume = BoundingVolume()
#         bounding_volume.primitives.append(box)
#         bounding_volume.primitive_poses.append(target_pose.pose)
        
#         pos_constraint.constraint_region = bounding_volume
#         pos_constraint.weight = 1.0

#         # Orientation constraint
#         ori_constraint = OrientationConstraint()
#         ori_constraint.header = target_pose.header
#         ori_constraint.link_name = "wrist_link"
#         ori_constraint.orientation = target_pose.pose.orientation
        
#         # Reasonable orientation tolerances (about 17 degrees each axis)
#         ori_constraint.absolute_x_axis_tolerance = 0.3
#         ori_constraint.absolute_y_axis_tolerance = 0.3
#         ori_constraint.absolute_z_axis_tolerance = 0.3
#         ori_constraint.weight = 1.0

#         constraints.position_constraints.append(pos_constraint)
#         constraints.orientation_constraints.append(ori_constraint)
#         request.goal_constraints.append(constraints)

#         # ========== Planning Options ==========
#         planning_options = PlanningOptions()
#         planning_options.plan_only = False
#         planning_options.look_around = False
#         planning_options.replan = True
#         planning_options.replan_attempts = 3
#         planning_options.replan_delay = 1.0

#         # ========== Action Goal ==========
#         goal_msg = MoveGroup.Goal()
#         goal_msg.request = request
#         goal_msg.planning_options = planning_options

#         # ========== Send Goal ==========
#         self.get_logger().info("Sending simplified pose goal to MoveGroup...")
#         send_goal_future = self._action_client.send_goal_async(goal_msg, feedback_callback=self.feedback_cb)
#         send_goal_future.add_done_callback(self.goal_response_cb)

#     def send_alternative_goal(self):
#         """Alternative approach using a very simple request"""
#         self.get_logger().info("Trying alternative simple approach...")
        
#         # Even simpler request
#         request = MotionPlanRequest()
#         request.group_name = "arm"
#         request.num_planning_attempts = 5
#         request.allowed_planning_time = 5.0
        
#         # Just use current state
#         request.start_state.is_diff = True
        
#         # Single position constraint only
#         constraints = Constraints()
#         pos_constraint = PositionConstraint()
#         pos_constraint.header.frame_id = "world"
#         pos_constraint.header.stamp = self.get_clock().now().to_msg()
#         pos_constraint.link_name = "wrist_link"
        
#         # Large sphere for easy planning
#         sphere = SolidPrimitive()
#         sphere.type = SolidPrimitive.SPHERE
#         sphere.dimensions = [0.1]  # 10cm tolerance
        
#         target_pose = Pose()
#         target_pose.position.x = 0.1
#         target_pose.position.y = 0.0
#         target_pose.position.z = 0.15
#         target_pose.orientation.w = 1.0
        
#         bounding_volume = BoundingVolume()
#         bounding_volume.primitives.append(sphere)
#         bounding_volume.primitive_poses.append(target_pose)
        
#         pos_constraint.constraint_region = bounding_volume
#         pos_constraint.weight = 1.0
        
#         constraints.position_constraints.append(pos_constraint)
#         request.goal_constraints.append(constraints)
        
#         goal_msg = MoveGroup.Goal()
#         goal_msg.request = request
#         goal_msg.planning_options.plan_only = False
        
#         send_goal_future = self._action_client.send_goal_async(goal_msg, feedback_callback=self.feedback_cb)
#         send_goal_future.add_done_callback(self.goal_response_cb)

#     def visualize_target(self, pose):
#         marker = Marker()
#         marker.header.frame_id = pose.header.frame_id
#         marker.header.stamp = self.get_clock().now().to_msg()
#         marker.ns = "target_pose"
#         marker.id = 0
#         marker.type = Marker.SPHERE
#         marker.action = Marker.ADD
#         marker.pose = pose.pose
#         marker.scale.x = 0.05
#         marker.scale.y = 0.05
#         marker.scale.z = 0.05
#         marker.color.a = 1.0
#         marker.color.r = 1.0
#         marker.color.g = 0.0
#         marker.color.b = 0.0
#         self.marker_pub.publish(marker)

#     def goal_response_cb(self, future):
#         goal_handle = future.result()
#         if not goal_handle.accepted:
#             self.get_logger().error("Goal rejected.")
#             return
#         self.get_logger().info("Goal accepted")
#         self._get_result_future = goal_handle.get_result_async()
#         self._get_result_future.add_done_callback(self.get_result_cb)

#     def feedback_cb(self, feedback_msg):
#         state = feedback_msg.feedback.state
#         self.get_logger().info(f"Planning state: {state}")

#     def get_result_cb(self, future):
#         result = future.result().result
#         code = result.error_code.val
#         self.get_logger().info(f"Motion planning result code: {code}")

#         if code == result.error_code.SUCCESS:
#             self.get_logger().info("Motion plan succeeded!")
#         else:
#             self.get_logger().error(f"Motion planning failed with error code: {code}")
#             # Try the alternative approach
#             time.sleep(1.0)
#             self.send_alternative_goal()

# def main(args=None):
#     rclpy.init(args=args)
#     node = MoveIt2Planner()
#     rclpy.spin(node)
#     node.destroy_node()
#     rclpy.shutdown()

# if __name__ == '__main__':
#     main()



# test_moveit.py












