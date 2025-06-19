# #!/usr/bin/env python3

# import rclpy
# from rclpy.node import Node
# from rclpy.action import ActionClient
# from moveit_msgs.srv import GetMotionPlan
# from moveit_msgs.action import ExecuteTrajectory
# from control_msgs.action import FollowJointTrajectory
# from moveit_msgs.msg import (
#     MotionPlanRequest, WorkspaceParameters, RobotState, Constraints,
#     PositionConstraint, OrientationConstraint, BoundingVolume, RobotTrajectory
# )
# from sensor_msgs.msg import JointState
# from geometry_msgs.msg import Vector3, Point, Pose, Quaternion
# from shape_msgs.msg import SolidPrimitive
# from std_msgs.msg import Header
# from trajectory_msgs.msg import JointTrajectory
# from controller_manager_msgs.srv import ListControllers
# import time

# class MotionPlanningClient(Node):
#     def __init__(self):
#         super().__init__('motion_planning_client')
        
#         # Create service client for planning
#         self.plan_client = self.create_client(GetMotionPlan, '/plan_kinematic_path')
        
#         # Create multiple action clients for different execution methods
#         self.execute_client = ActionClient(self, ExecuteTrajectory, '/execute_trajectory')
#         self.follow_joint_traj_client = ActionClient(self, FollowJointTrajectory, '/arm/follow_joint_trajectory')
        
#         # Create publisher for direct trajectory execution
#         self.trajectory_pub = self.create_publisher(JointTrajectory, '/arm/joint_trajectory', 10)
        
#         # Create client to check controllers
#         self.controller_client = self.create_client(ListControllers, '/controller_manager/list_controllers')
        
#         # Wait for planning service
#         while not self.plan_client.wait_for_service(timeout_sec=1.0):
#             self.get_logger().info('Motion planning service not available, waiting...')

#     def check_controllers(self):
#         """Check if controllers are running properly"""
#         if not self.controller_client.wait_for_service(timeout_sec=2.0):
#             self.get_logger().warn('Controller manager service not available')
#             return True  # Continue anyway
            
#         request = ListControllers.Request()
#         future = self.controller_client.call_async(request)
#         rclpy.spin_until_future_complete(self, future)
        
#         if future.result() is None:
#             self.get_logger().error('Failed to get controller list')
#             return True  # Continue anyway
            
#         response = future.result()
        
#         # Check for active controllers
#         active_controllers = [c for c in response.controller if c.state == 'active']
        
#         self.get_logger().info(f'Active controllers: {[c.name for c in active_controllers]}')
        
#         # Look for arm controller
#         arm_controllers = [c for c in active_controllers if c.name in ['arm', 'arm_controller', 'joint_trajectory_controller']]
        
#         if not arm_controllers:
#             self.get_logger().warn('No active arm controller found!')
#             self.get_logger().info('Available controllers: ' + ', '.join([c.name for c in active_controllers]))
#         else:
#             self.get_logger().info(f'Found arm controller: {arm_controllers[0].name}')
        
#         return True

#     def plan_motion(self):
#         # Create the motion plan request
#         request = GetMotionPlan.Request()
        
#         # Set up workspace parameters
#         request.motion_plan_request.workspace_parameters = WorkspaceParameters(
#             header=Header(frame_id='base_link'),
#             min_corner=Vector3(x=-1.0, y=-1.0, z=-1.0),
#             max_corner=Vector3(x=1.0, y=1.0, z=1.0)
#         )
        
#         # Set up start state (current joint positions)
#         joint_state = JointState()
#         joint_state.name = [
#             'rotating_base_joint', 'shoulder_joint', 'elbow_joint', 
#             'forearm_joint', 'wrist_joint'
#         ]
#         joint_state.position = [
#             -1.48580983648533, 0.08469186593787745, -1.3653615677389317,
#             -0.39685258923023947, -1.0637781573360787
#         ]
        
#         request.motion_plan_request.start_state = RobotState(
#             joint_state=joint_state,
#             is_diff=False
#         )
        
#         # Set up goal constraints
#         constraints = Constraints()
        
#         # Position constraint for wrist_link
#         pos_constraint = PositionConstraint()
#         pos_constraint.header = Header(frame_id='base_link')
#         pos_constraint.link_name = 'wrist_link'
#         pos_constraint.target_point_offset = Vector3(x=0.0, y=0.0, z=0.0)
        
#         # Define target region as a small sphere
#         primitive = SolidPrimitive()
#         primitive.type = SolidPrimitive.SPHERE
#         primitive.dimensions = [0.01]  # 1cm radius
        
#         target_pose = Pose()
#         target_pose.position = Point(
#             x=-0.2437370260113022,
#             y=0.0417840349084948, 
#             z=0.18842959812130225
#         )
#         target_pose.orientation = Quaternion(x=0.0, y=0.0, z=0.0, w=1.0)
        
#         pos_constraint.constraint_region = BoundingVolume(
#             primitives=[primitive],
#             primitive_poses=[target_pose]
#         )
#         pos_constraint.weight = 1.0
        
#         # Orientation constraint for wrist_link
#         orient_constraint = OrientationConstraint()
#         orient_constraint.header = Header(frame_id='base_link')
#         orient_constraint.link_name = 'wrist_link'
#         orient_constraint.orientation = Quaternion(
#             x=0.4906173408438478, y=0.1067093485225761,
#             z=0.8637339908344014, w=0.04325890419444189
#         )
#         orient_constraint.absolute_x_axis_tolerance = 0.1
#         orient_constraint.absolute_y_axis_tolerance = 0.1  
#         orient_constraint.absolute_z_axis_tolerance = 0.1
#         orient_constraint.weight = 1.0
        
#         # Add constraints to the request
#         constraints.position_constraints = [pos_constraint]
#         constraints.orientation_constraints = [orient_constraint]
#         request.motion_plan_request.goal_constraints = [constraints]
        
#         # Set planning parameters with reduced velocity for safer execution
#         request.motion_plan_request.group_name = 'arm'
#         request.motion_plan_request.planner_id = 'RRTConnect'
#         request.motion_plan_request.num_planning_attempts = 10
#         request.motion_plan_request.allowed_planning_time = 5.0
#         request.motion_plan_request.max_velocity_scaling_factor = 0.2  # Very slow
#         request.motion_plan_request.max_acceleration_scaling_factor = 0.2  # Very slow
        
#         # Call the service
#         self.get_logger().info('Sending motion planning request...')
#         future = self.plan_client.call_async(request)
        
#         return future

#     def execute_trajectory_follow_joint(self, trajectory):
#         """Execute using FollowJointTrajectory action"""
#         if not self.follow_joint_traj_client.wait_for_server(timeout_sec=2.0):
#             self.get_logger().warn('FollowJointTrajectory action server not available')
#             return False
            
#         goal = FollowJointTrajectory.Goal()
#         goal.trajectory = trajectory.joint_trajectory
        
#         self.get_logger().info('Sending FollowJointTrajectory goal...')
        
#         send_goal_future = self.follow_joint_traj_client.send_goal_async(goal)
#         rclpy.spin_until_future_complete(self, send_goal_future)
        
#         goal_handle = send_goal_future.result()
#         if not goal_handle.accepted:
#             self.get_logger().error('FollowJointTrajectory goal rejected')
#             return False
            
#         self.get_logger().info('FollowJointTrajectory goal accepted, executing...')
        
#         get_result_future = goal_handle.get_result_async()
#         rclpy.spin_until_future_complete(self, get_result_future)
        
#         result = get_result_future.result().result
        
#         if result.error_code == 0:  # SUCCESSFUL
#             self.get_logger().info('✅ FollowJointTrajectory executed successfully!')
#             return True
#         else:
#             self.get_logger().error(f'❌ FollowJointTrajectory failed with error code: {result.error_code}')
#             return False

#     def execute_trajectory_direct(self, trajectory):
#         """Execute trajectory by publishing directly to controller topic"""
#         joint_trajectory = trajectory.joint_trajectory
        
#         # Update header with current timestamp
#         joint_trajectory.header.stamp = self.get_clock().now().to_msg()
        
#         self.get_logger().info('Publishing trajectory directly to /arm/joint_trajectory...')
#         self.trajectory_pub.publish(joint_trajectory)
        
#         # Calculate expected execution time
#         if joint_trajectory.points:
#             last_point = joint_trajectory.points[-1]
#             total_time = last_point.time_from_start.sec + last_point.time_from_start.nanosec * 1e-9
            
#             self.get_logger().info(f'Waiting {total_time:.2f} seconds for execution...')
#             time.sleep(total_time + 1.0)  # Add buffer time
            
#             self.get_logger().info('✅ Direct trajectory execution completed')
#             return True
        
#         return False

#     def execute_trajectory(self, trajectory):
#         """Execute the planned trajectory using multiple methods"""
        
#         # Method 1: Try FollowJointTrajectory action (most common for ros2_control)
#         self.get_logger().info('Attempting FollowJointTrajectory action...')
#         success = self.execute_trajectory_follow_joint(trajectory)
#         if success:
#             return True
        
#         # Method 2: Try MoveIt ExecuteTrajectory action
#         if self.execute_client.wait_for_server(timeout_sec=2.0):
#             self.get_logger().info('Attempting MoveIt ExecuteTrajectory action...')
            
#             goal = ExecuteTrajectory.Goal()
#             goal.trajectory = trajectory
            
#             send_goal_future = self.execute_client.send_goal_async(goal)
#             rclpy.spin_until_future_complete(self, send_goal_future)
            
#             goal_handle = send_goal_future.result()
#             if goal_handle and goal_handle.accepted:
#                 self.get_logger().info('MoveIt ExecuteTrajectory goal accepted, executing...')
                
#                 get_result_future = goal_handle.get_result_async()
#                 rclpy.spin_until_future_complete(self, get_result_future)
                
#                 result = get_result_future.result().result
                
#                 if result.error_code.val == 1:  # SUCCESS
#                     self.get_logger().info('✅ MoveIt ExecuteTrajectory executed successfully!')
#                     return True
        
#         # Method 3: Try direct topic publication
#         self.get_logger().info('Attempting direct trajectory publication...')
#         return self.execute_trajectory_direct(trajectory)

#     def plan_and_execute(self):
#         """Plan and execute motion in sequence"""
#         # Check controllers
#         self.check_controllers()
        
#         # Step 1: Plan the motion
#         plan_future = self.plan_motion()
#         rclpy.spin_until_future_complete(self, plan_future)
        
#         if plan_future.result() is None:
#             self.get_logger().error('Planning service call failed')
#             return False
            
#         response = plan_future.result()
        
#         # Check if planning was successful
#         if response.motion_plan_response.error_code.val != 1:  # Not SUCCESS
#             self.get_logger().error(f'Motion planning failed with error code: {response.motion_plan_response.error_code.val}')
#             return False
            
#         # Print planning results
#         self.print_trajectory(response)
        
#         # Step 2: Execute the planned trajectory
#         trajectory = response.motion_plan_response.trajectory
#         success = self.execute_trajectory(trajectory)
        
#         return success

#     def print_trajectory(self, response):
#         """Print the planned trajectory details"""
#         if response.motion_plan_response.error_code.val == 1:  # SUCCESS
#             trajectory = response.motion_plan_response.trajectory.joint_trajectory
            
#             print(f"\n✅ Motion planning SUCCESS!")
#             print(f"Planning time: {response.motion_plan_response.planning_time:.3f} seconds")
#             print(f"Trajectory points: {len(trajectory.points)}")
#             print(f"Joint names: {trajectory.joint_names}")
            
#             # Show first and last waypoints
#             if len(trajectory.points) > 0:
#                 first_point = trajectory.points[0]
#                 last_point = trajectory.points[-1]
                
#                 print(f"\nStart position: {[f'{p:.3f}' for p in first_point.positions]}")
#                 print(f"End position: {[f'{p:.3f}' for p in last_point.positions]}")
                
#                 total_time = last_point.time_from_start.sec + last_point.time_from_start.nanosec * 1e-9
#                 print(f"Total execution time: {total_time:.3f} seconds")
                
#         else:
#             print(f"\n❌ Motion planning FAILED with error code: {response.motion_plan_response.error_code.val}")

# def main():
#     rclpy.init()
    
#     # Create the motion planning client
#     client_node = MotionPlanningClient()
    
#     try:
#         # Plan and execute the motion
#         success = client_node.plan_and_execute()
        
#         if success:
#             print("\n🎉 Motion completed successfully!")
#         else:
#             print("\n💥 Motion failed!")
            
#     except KeyboardInterrupt:
#         print("\nShutting down...")
#     finally:
#         client_node.destroy_node()
#         rclpy.shutdown()

# if __name__ == '__main__':
#     main()



#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from moveit_msgs.srv import GetMotionPlan, GetPositionIK
from moveit_msgs.action import ExecuteTrajectory
from control_msgs.action import FollowJointTrajectory
from moveit_msgs.msg import (
    MotionPlanRequest, WorkspaceParameters, RobotState, Constraints,
    PositionConstraint, OrientationConstraint, BoundingVolume, RobotTrajectory,
    JointConstraint
)
from sensor_msgs.msg import JointState
from geometry_msgs.msg import Vector3, Point, Pose, Quaternion
from shape_msgs.msg import SolidPrimitive
from std_msgs.msg import Header
from trajectory_msgs.msg import JointTrajectory
from controller_manager_msgs.srv import ListControllers
import time

class MotionPlanningClient(Node):
    def __init__(self):
        super().__init__('motion_planning_client')
        
        # Initialize joint state
        self.current_joint_state = None
        self.joint_state_sub = self.create_subscription(
            JointState, '/joint_states', self.joint_state_callback, 10)
        
        # Create service and action clients
        self.plan_client = self.create_client(GetMotionPlan, '/plan_kinematic_path')
        self.ik_client = self.create_client(GetPositionIK, '/compute_ik')
        self.execute_client = ActionClient(self, ExecuteTrajectory, '/execute_trajectory')
        self.follow_joint_traj_client = ActionClient(self, FollowJointTrajectory, '/arm/follow_joint_trajectory')
        self.trajectory_pub = self.create_publisher(JointTrajectory, '/arm/joint_trajectory', 10)
        self.controller_client = self.create_client(ListControllers, '/controller_manager/list_controllers')
        
        # Wait for services
        while not self.plan_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Motion planning service not available, waiting...')
        while not self.ik_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('IK service not available, waiting...')

    def joint_state_callback(self, msg):
        expected_joints = ['rotating_base_joint', 'shoulder_joint', 'elbow_joint', 'forearm_joint', 'wrist_joint']
        if all(j in msg.name for j in expected_joints):
            self.current_joint_state = JointState()
            self.current_joint_state.name = expected_joints
            self.current_joint_state.position = [msg.position[msg.name.index(j)] for j in expected_joints]
            self.get_logger().info(f'Received valid joint state: {self.current_joint_state.position}')
        else:
            self.get_logger().warn(f'Received joint state with unexpected joint names: {msg.name}')

    def check_controllers(self):
        if not self.controller_client.wait_for_service(timeout_sec=2.0):
            self.get_logger().warn('Controller manager service not available')
            return True
        request = ListControllers.Request()
        future = self.controller_client.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        if future.result() is None:
            self.get_logger().error('Failed to get controller list')
            return True
        response = future.result()
        active_controllers = [c for c in response.controller if c.state == 'active']
        self.get_logger().info(f'Active controllers: {[c.name for c in active_controllers]}')
        arm_controllers = [c for c in active_controllers if c.name in ['arm', 'arm_controller', 'joint_trajectory_controller']]
        if not arm_controllers:
            self.get_logger().warn('No active arm controller found!')
        else:
            self.get_logger().info(f'Found arm controller: {arm_controllers[0].name}')
        return True

    def validate_pose(self, target_pose, avoid_collisions=True):
        request = GetPositionIK.Request()
        request.ik_request.group_name = 'arm'
        joint_state = JointState()
        joint_state.name = [
            'rotating_base_joint', 'shoulder_joint', 'elbow_joint', 
            'forearm_joint', 'wrist_joint'
        ]
        
        # Try multiple seed states
        seed_states = [
            self.current_joint_state.position if self.current_joint_state else
            [-1.48580983648533, 0.08469186593787745, -1.3653615677389317,
             -0.39685258923023947, -1.0637781573360787],
            [0.0, 0.0, 0.0, 0.0, 0.0],  # Neutral position
            [-1.0, 0.3, -1.0, 0.0, 0.0],  # Alternative configuration
            [-1.48580983648533, 0.08469186593787745, -1.3653615677389317,
             -0.39685258923023947, -1.0637781573360787]  # Original start state
        ]
        
        for seed in seed_states:
            joint_state.position = seed
            request.ik_request.robot_state = RobotState(joint_state=joint_state)
            request.ik_request.pose_stamped.header.frame_id = 'base_link'
            request.ik_request.pose_stamped.pose = target_pose
            request.ik_request.avoid_collisions = avoid_collisions
            future = self.ik_client.call_async(request)
            rclpy.spin_until_future_complete(self, future)
            if future.result() and future.result().error_code.val == 1:
                self.get_logger().info(f'Target pose is feasible with seed {seed}')
                return True
            else:
                error_code = future.result().error_code.val if future.result() else "No result"
                self.get_logger().error(f'IK failed for seed {seed}: error code {error_code}')
        self.get_logger().error('Target pose is not feasible after trying multiple seeds')
        return False

    def plan_motion(self, target_pose=None, target_joints=None):
        request = GetMotionPlan.Request()
        request.motion_plan_request.workspace_parameters = WorkspaceParameters(
            header=Header(frame_id='base_link'),
            min_corner=Vector3(x=-0.4, y=-0.4, z=-0.4),
            max_corner=Vector3(x=0.4, y=0.4, z=0.4)
        )
        joint_state = JointState()
        joint_state.name = [
            'rotating_base_joint', 'shoulder_joint', 'elbow_joint', 
            'forearm_joint', 'wrist_joint'
        ]
        joint_state.position = (
            self.current_joint_state.position if self.current_joint_state else
            [-1.48580983648533, 0.08469186593787745, -1.3653615677389317,
             -0.39685258923023947, -1.0637781573360787]
        )
        request.motion_plan_request.start_state = RobotState(
            joint_state=joint_state,
            is_diff=False
        )
        constraints = Constraints()
        if target_pose:
            if target_pose is None:
                target_pose = Pose()
                target_pose.position = Point(x=-0.243737, y=0.041784, z=0.1884296)
                target_pose.orientation = Quaternion(x=0.4906173, y=0.1067093, z=0.863734, w=0.0432589)
            pos_constraint = PositionConstraint()
            pos_constraint.header = Header(frame_id='base_link')
            pos_constraint.link_name = 'wrist_link'
            pos_constraint.target_point_offset = Vector3(x=0.0, y=0.0, z=0.0)
            primitive = SolidPrimitive()
            primitive.type = SolidPrimitive.SPHERE
            primitive.dimensions = [0.05]  # 5cm radius
            pos_constraint.constraint_region = BoundingVolume(
                primitives=[primitive],
                primitive_poses=[target_pose]
            )
            pos_constraint.weight = 1.0
            orient_constraint = OrientationConstraint()
            orient_constraint.header = Header(frame_id='base_link')
            orient_constraint.link_name = 'wrist_link'
            orient_constraint.orientation = target_pose.orientation
            orient_constraint.absolute_x_axis_tolerance = 0.5
            orient_constraint.absolute_y_axis_tolerance = 0.5
            orient_constraint.absolute_z_axis_tolerance = 0.5
            orient_constraint.weight = 1.0
            constraints.position_constraints = [pos_constraint]
            constraints.orientation_constraints = [orient_constraint]
        elif target_joints:
            for name, pos in zip(joint_state.name, target_joints):
                jc = JointConstraint()
                jc.joint_name = name
                jc.position = pos
                jc.tolerance_above = 0.1
                jc.tolerance_below = 0.1
                jc.weight = 1.0
                constraints.joint_constraints.append(jc)
        request.motion_plan_request.goal_constraints = [constraints]
        request.motion_plan_request.group_name = 'arm'
        request.motion_plan_request.planner_id = 'RRTConnect'
        request.motion_plan_request.num_planning_attempts = 20
        request.motion_plan_request.allowed_planning_time = 10.0
        request.motion_plan_request.max_velocity_scaling_factor = 0.3
        request.motion_plan_request.max_acceleration_scaling_factor = 0.3
        self.get_logger().info('Sending motion planning request...')
        future = self.plan_client.call_async(request)
        return future

    def execute_trajectory_follow_joint(self, trajectory):
        if not self.follow_joint_traj_client.wait_for_server(timeout_sec=2.0):
            self.get_logger().warn('FollowJointTrajectory action server not available')
            return False
        goal = FollowJointTrajectory.Goal()
        goal.trajectory = trajectory.joint_trajectory
        self.get_logger().info('Sending FollowJointTrajectory goal...')
        send_goal_future = self.follow_joint_traj_client.send_goal_async(goal)
        rclpy.spin_until_future_complete(self, send_goal_future)
        goal_handle = send_goal_future.result()
        if not goal_handle.accepted:
            self.get_logger().error('FollowJointTrajectory goal rejected')
            return False
        self.get_logger().info('FollowJointTrajectory goal accepted, executing...')
        get_result_future = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(self, get_result_future)
        result = get_result_future.result().result
        if result.error_code == 0:
            self.get_logger().info('✅ FollowJointTrajectory executed successfully!')
            return True
        self.get_logger().error(f'❌ FollowJointTrajectory failed with error code: {result.error_code}')
        return False

    def execute_trajectory_direct(self, trajectory):
        joint_trajectory = trajectory.joint_trajectory
        joint_trajectory.header.stamp = self.get_clock().now().to_msg()
        self.get_logger().info('Publishing trajectory directly to /arm/joint_trajectory...')
        self.trajectory_pub.publish(joint_trajectory)
        if joint_trajectory.points:
            last_point = joint_trajectory.points[-1]
            total_time = last_point.time_from_start.sec + last_point.time_from_start.nanosec * 1e-9
            self.get_logger().info(f'Waiting {total_time:.2f} seconds for execution...')
            time.sleep(total_time + 1.0)
            self.get_logger().info('✅ Direct trajectory execution completed')
            return True
        return False

    def execute_trajectory(self, trajectory):
        self.get_logger().info('Attempting FollowJointTrajectory action...')
        success = self.execute_trajectory_follow_joint(trajectory)
        if success:
            return True
        if self.execute_client.wait_for_server(timeout_sec=2.0):
            self.get_logger().info('Attempting MoveIt ExecuteTrajectory action...')
            goal = ExecuteTrajectory.Goal()
            goal.trajectory = trajectory
            send_goal_future = self.execute_client.send_goal_async(goal)
            rclpy.spin_until_future_complete(self, send_goal_future)
            goal_handle = send_goal_future.result()
            if goal_handle and goal_handle.accepted:
                self.get_logger().info('MoveIt ExecuteTrajectory goal accepted, executing...')
                get_result_future = goal_handle.get_result_async()
                rclpy.spin_until_future_complete(self, get_result_future)
                result = get_result_future.result().result
                if result.error_code.val == 1:
                    self.get_logger().info('✅ MoveIt ExecuteTrajectory executed successfully!')
                    return True
        self.get_logger().info('Attempting direct trajectory publication...')
        return self.execute_trajectory_direct(trajectory)

    def print_trajectory(self, response):
        error_codes = {
            1: "SUCCESS",
            -1: "PLANNING_FAILED",
            -2: "INVALID_MOTION_PLAN",
            -3: "MOTION_PLAN_INVALIDATED_BY_ENVIRONMENT_CHANGE",
            -4: "CONTROL_FAILED",
            -5: "UNABLE_TO_AQUIRE_SENSOR_DATA",
            -6: "TIMEOUT",
            -7: "PREEMPTED",
            -10: "START_STATE_IN_COLLISION",
            -11: "START_STATE_VIOLATES_PATH_CONSTRAINTS",
            -12: "GOAL_IN_COLLISION",
            -13: "GOAL_VIOLATES_PATH_CONSTRAINTS",
            -14: "GOAL_CONSTRAINTS_VIOLATED",
            -15: "INVALID_GROUP",
            -16: "INVALID_GOAL_CONSTRAINTS",
            -17: "INVALID_ROBOT_STATE",
            -18: "INVALID_LINK_NAME",
            -21: "INVALID_OBJECT_NAME",
            -22: "FRAME_TRANSFORM_FAILURE",
            -23: "COLLISION_CHECKING_UNAVAILABLE",
            -24: "ROBOT_STATE_STALE",
            -25: "SENSOR_INFO_STALE",
            -31: "NO_IK_SOLUTION"
        }
        if response.motion_plan_response.error_code.val == 1:
            trajectory = response.motion_plan_response.trajectory.joint_trajectory
            print(f"\n✅ Motion planning SUCCESS!")
            print(f"Planning time: {response.motion_plan_response.planning_time:.3f} seconds")
            print(f"Trajectory points: {len(trajectory.points)}")
            print(f"Joint names: {trajectory.joint_names}")
            if len(trajectory.points) > 0:
                first_point = trajectory.points[0]
                last_point = trajectory.points[-1]
                print(f"\nStart position: {[f'{p:.3f}' for p in first_point.positions]}")
                print(f"End position: {[f'{p:.3f}' for p in last_point.positions]}")
                total_time = last_point.time_from_start.sec + last_point.time_from_start.nanosec * 1e-9
                print(f"Total execution time: {total_time:.3f} seconds")
        else:
            error_msg = error_codes.get(
                response.motion_plan_response.error_code.val,
                f"Unknown error code {response.motion_plan_response.error_code.val}"
            )
            print(f"\n❌ Motion planning FAILED: {error_msg}")

    def plan_and_execute(self, target_pose=None, target_joints=None):
        self.check_controllers()
        if target_pose:
            # Try with collisions first
            if not self.validate_pose(target_pose, avoid_collisions=True):
                self.get_logger().warn('Retrying IK without collision checking...')
                if not self.validate_pose(target_pose, avoid_collisions=False):
                    self.get_logger().error('Aborting due to infeasible target pose')
                    return False
        plan_future = self.plan_motion(target_pose, target_joints)
        rclpy.spin_until_future_complete(self, plan_future)
        if plan_future.result() is None:
            self.get_logger().error('Planning service call failed')
            return False
        response = plan_future.result()
        self.print_trajectory(response)
        if response.motion_plan_response.error_code.val != 1:
            self.get_logger().error(f'Planning failed with error code: {response.motion_plan_response.error_code.val}')
            return False
        trajectory = response.motion_plan_response.trajectory
        success = self.execute_trajectory(trajectory)
        return success

def main():
    rclpy.init()
    client_node = MotionPlanningClient()
    try:
        # Test with a new, likely reachable pose
        new_pose = Pose()
        new_pose.position = Point(x=-0.15, y=0.0, z=0.15)  # Adjusted to negative x
        new_pose.orientation = Quaternion(x=0.0, y=0.0, z=0.0, w=1.0)
        # Alternatively, test with a joint goal
        # target_joints = [0.0, 0.3, -0.5, 0.0, 0.0]
        success = client_node.plan_and_execute(target_pose=new_pose)
        # success = client_node.plan_and_execute(target_joints=target_joints)
        if success:
            print("\n🎉 Motion completed successfully!")
        else:
            print("\n💥 Motion failed!")
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        client_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
















