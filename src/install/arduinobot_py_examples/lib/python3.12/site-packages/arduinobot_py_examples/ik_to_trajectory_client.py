# #!/usr/bin/env python3

# import rclpy
# from rclpy.node import Node

# from geometry_msgs.msg import PoseStamped
# from moveit_msgs.msg import MotionPlanRequest, Constraints, PositionConstraint, OrientationConstraint
# from moveit_msgs.action import MoveGroup
# from shape_msgs.msg import SolidPrimitive
# from builtin_interfaces.msg import Duration

# from rclpy.action import ActionClient


# class MoveGroupMotionPlanner(Node):
#     def __init__(self):
#         super().__init__('move_group_motion_planner_client')

#         self.action_client = ActionClient(self, MoveGroup, '/move_action')

#         # Wait for action server
#         self.get_logger().info('⏳ Waiting for /move_action server...')
#         self.action_client.wait_for_server()
#         self.get_logger().info('✅ /move_action server available.')

#         # Plan to this pose
#         target_pose = PoseStamped()
#         target_pose.header.frame_id = 'world'
#         target_pose.pose.position.x = 0.0
#         target_pose.pose.position.y = 0.25
#         target_pose.pose.position.z = 0.02
#         target_pose.pose.orientation.w = 1.0

#         self.plan_and_execute(target_pose)

#     def plan_and_execute(self, pose_stamped):
#         # Build constraints
#         goal_constraints = Constraints()

#         # Position constraint
#         pos_constraint = PositionConstraint()
#         pos_constraint.header.frame_id = 'world'
#         pos_constraint.link_name = 'ik_frame'
#         pos_constraint.constraint_region.primitives.append(
#             SolidPrimitive(type=SolidPrimitive.BOX, dimensions=[0.001, 0.001, 0.001])
#         )
#         pos_constraint.constraint_region.primitive_poses.append(pose_stamped.pose)
#         goal_constraints.position_constraints.append(pos_constraint)

#         # Optional: Orientation constraint
#         # ori_constraint = OrientationConstraint()
#         # ori_constraint.header.frame_id = 'world'
#         # ori_constraint.link_name = 'ik_frame'
#         # ori_constraint.orientation = pose_stamped.pose.orientation
#         # ori_constraint.absolute_x_axis_tolerance = 0.1
#         # ori_constraint.absolute_y_axis_tolerance = 0.1
#         # ori_constraint.absolute_z_axis_tolerance = 0.1
#         # ori_constraint.weight = 1.0
#         # goal_constraints.orientation_constraints.append(ori_constraint)

#         # Build motion plan request
#         plan_request = MotionPlanRequest()
#         plan_request.group_name = 'arm'
#         plan_request.allowed_planning_time = 3.0
#         plan_request.num_planning_attempts = 10
#         plan_request.goal_constraints.append(goal_constraints)
#         plan_request.max_velocity_scaling_factor = 1.0
#         plan_request.max_acceleration_scaling_factor = 1.0

#         # Build action goal
#         move_goal = MoveGroup.Goal()
#         move_goal.request = plan_request
#         move_goal.planning_options.plan_only = False  # Set True for planning only (no execution)
#         move_goal.planning_options.look_around = False
#         move_goal.planning_options.replan = False
#         move_goal.planning_options.replan_attempts = 0
        

#         # Send goal
#         self.get_logger().info('📡 Sending MoveGroup goal to move_action...')
#         send_goal_future = self.action_client.send_goal_async(move_goal)
#         rclpy.spin_until_future_complete(self, send_goal_future)

#         goal_handle = send_goal_future.result()
#         if not goal_handle.accepted:
#             self.get_logger().error('❌ MoveGroup goal was rejected by the server.')
#             return

#         self.get_logger().info('✅ MoveGroup goal accepted. Waiting for result...')
#         result_future = goal_handle.get_result_async()
#         rclpy.spin_until_future_complete(self, result_future)

#         result = result_future.result().result
#         if result.error_code.val == 1:
#             self.get_logger().info('✅ Trajectory planned and executed successfully.')
#         else:
#             self.get_logger().error(f'❌ Motion planning failed with error code: {result.error_code.val}')


# def main(args=None):
#     rclpy.init(args=args)
#     node = MoveGroupMotionPlanner()
#     node.destroy_node()
#     rclpy.shutdown()


# if __name__ == '__main__':
#     main()



# #!/usr/bin/env python3

# import math
# import rclpy
# from rclpy.node import Node

# from geometry_msgs.msg import PoseStamped
# from moveit_msgs.msg import MotionPlanRequest, Constraints, PositionConstraint
# from moveit_msgs.action import MoveGroup
# from shape_msgs.msg import SolidPrimitive
# from builtin_interfaces.msg import Duration
# from trajectory_msgs.msg import JointTrajectoryPoint
# from control_msgs.action import FollowJointTrajectory

# from rclpy.action import ActionClient

# from tf2_ros import Buffer, TransformListener, LookupException, ConnectivityException, ExtrapolationException


# class MoveGroupMotionPlanner(Node):
#     def __init__(self):
#         super().__init__('move_group_motion_planner_client')

#         self.move_group_client = ActionClient(self, MoveGroup, '/move_action')
#         self.trajectory_client = ActionClient(self, FollowJointTrajectory, '/arm_controller/follow_joint_trajectory')

#         # TF2 buffer and listener
#         self.tf_buffer = Buffer()
#         self.tf_listener = TransformListener(self.tf_buffer, self)

#         self.get_logger().info('⏳ Waiting for /move_action server...')
#         self.move_group_client.wait_for_server()
#         self.get_logger().info('✅ /move_action server available.')

#         self.get_logger().info('⏳ Waiting for /follow_joint_trajectory server...')
#         self.trajectory_client.wait_for_server()
#         self.get_logger().info('✅ /follow_joint_trajectory server available.')

#         # Target position (cube position)
#         x_target, y_target, z_target = 0.0, 0.0, 0.02
#         approach_height = 0.15  # height above cube

#         # Plan to approach pose first
#         self.plan_and_execute(x_target, y_target, approach_height)

#         # Then move down to grasp pose
#         self.plan_and_execute(x_target, y_target, z_target)

#     def get_base_position(self):
#         try:
#             trans = self.tf_buffer.lookup_transform('world', 'base_link', rclpy.time.Time())
#             base_x = trans.transform.translation.x
#             base_y = trans.transform.translation.y
#             self.get_logger().info(f'📍 Base position in world: ({base_x:.3f}, {base_y:.3f})')
#         except (LookupException, ConnectivityException, ExtrapolationException):
#             self.get_logger().warn('⚠️ Could not get transform from world to base_link. Assuming (0,0)')
#             base_x, base_y = 0.0, 0.0
#         return base_x, base_y

#     def compute_wrist_angle(self, cube_x, cube_y, cube_yaw):
#         base_x, base_y = self.get_base_position()

#         # Angle from base to cube position
#         dx = cube_x - base_x
#         dy = cube_y - base_y
#         approach_angle = math.atan2(dy, dx)

#         # Snap approach angle to nearest 0° or 90° (cube symmetries)
#         snapped_approach_angle = round(approach_angle / (math.pi / 2)) * (math.pi / 2)

#         # Final wrist angle = snapped approach angle + cube yaw
#         wrist_angle = snapped_approach_angle + cube_yaw

#         # Normalize to [-pi, pi] for safety
#         wrist_angle = (wrist_angle + math.pi) % (2 * math.pi) - math.pi

#         self.get_logger().info(f'🔄 Base→Cube angle: {math.degrees(approach_angle):.1f}°, snapped: {math.degrees(snapped_approach_angle):.1f}°, '
#                             f'cube yaw: {math.degrees(cube_yaw):.1f}° → wrist: {math.degrees(wrist_angle):.1f}°')

#         return wrist_angle



#     def plan_and_execute(self, x, y, z):
#         # Target pose
#         pose_stamped = PoseStamped()
#         pose_stamped.header.frame_id = 'world'
#         pose_stamped.pose.position.x = x
#         pose_stamped.pose.position.y = y
#         pose_stamped.pose.position.z = z
#         pose_stamped.pose.orientation.w = 1.0

#         # Position constraint
#         goal_constraints = Constraints()
#         pos_constraint = PositionConstraint()
#         pos_constraint.header.frame_id = 'world'
#         pos_constraint.link_name = 'ik_frame'
#         pos_constraint.constraint_region.primitives.append(
#             SolidPrimitive(type=SolidPrimitive.BOX, dimensions=[0.001, 0.001, 0.001])
#         )
#         pos_constraint.constraint_region.primitive_poses.append(pose_stamped.pose)
#         goal_constraints.position_constraints.append(pos_constraint)

#         # Motion plan request
#         plan_request = MotionPlanRequest()
#         plan_request.group_name = 'arm'
#         plan_request.allowed_planning_time = 5.0
#         plan_request.num_planning_attempts = 20
#         plan_request.goal_constraints.append(goal_constraints)
#         plan_request.max_velocity_scaling_factor = 1.0
#         plan_request.max_acceleration_scaling_factor = 1.0

#         # MoveGroup goal
#         move_goal = MoveGroup.Goal()
#         move_goal.request = plan_request
#         move_goal.planning_options.plan_only = False  # Plan only
#         move_goal.planning_options.look_around = False
#         move_goal.planning_options.replan = False

#         self.get_logger().info(f'📡 Planning to ({x:.3f}, {y:.3f}, {z:.3f})...')
#         send_goal_future = self.move_group_client.send_goal_async(move_goal)
#         rclpy.spin_until_future_complete(self, send_goal_future)

#         goal_handle = send_goal_future.result()
#         if not goal_handle.accepted:
#             self.get_logger().error('❌ MoveGroup goal was rejected.')
#             return

#         self.get_logger().info('✅ Plan goal accepted. Waiting for result...')
#         result_future = goal_handle.get_result_async()
#         rclpy.spin_until_future_complete(self, result_future)

#         result = result_future.result().result
#         if result.error_code.val != 1:
#             self.get_logger().error(f'❌ Planning failed with error code: {result.error_code.val}')
#             return

#         self.get_logger().info('✅ Plan computed successfully. Adjusting wrist angle...')

#         # Retrieve planned trajectory
#         trajectory = result.planned_trajectory.joint_trajectory
#         joint_names = trajectory.joint_names

#         try:
#             joint5_idx = joint_names.index('joint_five')
#         except ValueError:
#             self.get_logger().error("❌ 'joint_five' not found in trajectory.")
#             return

#         # Compute wrist angle
#         wrist_angle = self.compute_wrist_angle(x, y,math.radians(0))

#         # Adjust joint 5 in all points
#         for point in trajectory.points:
#             point.positions = list(point.positions)
#             point.positions[joint5_idx] = wrist_angle

#         self.get_logger().info('✅ Wrist angle set for all trajectory points.')

#         # Send to trajectory controller
#         traj_goal = FollowJointTrajectory.Goal()
#         traj_goal.trajectory = trajectory
#         traj_goal.goal_time_tolerance = Duration(sec=1)

#         self.get_logger().info('📡 Sending trajectory to controller...')
#         send_traj_future = self.trajectory_client.send_goal_async(traj_goal)
#         rclpy.spin_until_future_complete(self, send_traj_future)

#         traj_goal_handle = send_traj_future.result()
#         if not traj_goal_handle.accepted:
#             self.get_logger().error('❌ Trajectory goal was rejected.')
#             return

#         self.get_logger().info('✅ Trajectory goal accepted. Waiting for result...')
#         result_future = traj_goal_handle.get_result_async()
#         rclpy.spin_until_future_complete(self, result_future)

#         traj_result = result_future.result().result
#         self.get_logger().info(f'✅ Execution finished with error code: {traj_result.error_code}')


# def main(args=None):
#     rclpy.init(args=args)
#     node = MoveGroupMotionPlanner()
#     node.destroy_node()
#     rclpy.shutdown()


# if __name__ == '__main__':
#     main()



# #!/usr/bin/env python3

# import math
# import rclpy
# from rclpy.node import Node

# from geometry_msgs.msg import PoseStamped
# from moveit_msgs.msg import MotionPlanRequest, Constraints, JointConstraint
# from moveit_msgs.action import MoveGroup
# from builtin_interfaces.msg import Duration
# from trajectory_msgs.msg import JointTrajectoryPoint
# from control_msgs.action import FollowJointTrajectory
# from rclpy.action import ActionClient
# from tf2_ros import Buffer, TransformListener


# class MoveGroupMotionPlanner(Node):
#     def __init__(self):
#         super().__init__('move_group_motion_planner_client')

#         self.move_group_client = ActionClient(self, MoveGroup, '/move_action')
#         self.trajectory_client = ActionClient(self, FollowJointTrajectory, '/arm_controller/follow_joint_trajectory')

#         self.tf_buffer = Buffer()
#         self.tf_listener = TransformListener(self.tf_buffer, self)

#         self.get_logger().info('⏳ Waiting for /move_action server...')
#         self.move_group_client.wait_for_server()
#         self.get_logger().info('✅ /move_action server available.')

#         self.get_logger().info('⏳ Waiting for /follow_joint_trajectory server...')
#         self.trajectory_client.wait_for_server()
#         self.get_logger().info('✅ /follow_joint_trajectory server available.')

#         x_target, y_target = 0.105, 0.125
#         z_approach = 0.18
#         z_pick = 0.04

#         # Move to approach position
#         self.plan_and_execute(x_target, y_target, z_approach)

#         # Move to pick position
#         self.plan_and_execute(x_target, y_target, z_pick)

#     def plan_and_execute(self, x, y, z):
#         pose_target = PoseStamped()
#         pose_target.header.frame_id = 'world'
#         pose_target.pose.position.x = x
#         pose_target.pose.position.y = y
#         pose_target.pose.position.z = z
#         pose_target.pose.orientation.w = 1.0

#         goal_constraints = Constraints()
#         goal_constraints.name = 'pose_goal_constraint'

#         # OPTIONAL: Add joint constraint for wrist alignment if needed
#         # joint_constraint = JointConstraint()
#         # joint_constraint.joint_name = 'joint_five'
#         # joint_constraint.position = -math.pi/2
#         # joint_constraint.tolerance_above = 0.01
#         # joint_constraint.tolerance_below = 0.01
#         # joint_constraint.weight = 1.0
#         # goal_constraints.joint_constraints.append(joint_constraint)

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
#         move_goal.planning_options.look_around = False
#         move_goal.planning_options.replan = False

#         self.get_logger().info(f'📡 Planning to ({x:.3f}, {y:.3f}, {z:.3f})...')
#         send_goal_future = self.move_group_client.send_goal_async(move_goal)
#         rclpy.spin_until_future_complete(self, send_goal_future)
#         goal_handle = send_goal_future.result()

#         if not goal_handle.accepted:
#             self.get_logger().error('❌ MoveGroup goal was rejected.')
#             return

#         self.get_logger().info('✅ Plan goal accepted. Waiting for result...')
#         result_future = goal_handle.get_result_async()
#         rclpy.spin_until_future_complete(self, result_future)
#         result = result_future.result().result

#         if result.error_code.val != 1:
#             self.get_logger().error(f'❌ Planning failed with error code: {result.error_code.val}')
#             return

#         self.get_logger().info('✅ Plan computed successfully.')

#         trajectory = result.planned_trajectory.joint_trajectory

#         traj_goal = FollowJointTrajectory.Goal()
#         traj_goal.trajectory = trajectory
#         traj_goal.goal_time_tolerance = Duration(sec=1)

#         self.get_logger().info('📡 Sending trajectory to controller...')
#         send_traj_future = self.trajectory_client.send_goal_async(traj_goal)
#         rclpy.spin_until_future_complete(self, send_traj_future)
#         traj_goal_handle = send_traj_future.result()

#         if not traj_goal_handle.accepted:
#             self.get_logger().error('❌ Trajectory goal was rejected.')
#             return

#         self.get_logger().info('✅ Trajectory goal accepted. Waiting for result...')
#         result_future = traj_goal_handle.get_result_async()
#         rclpy.spin_until_future_complete(self, result_future)
#         traj_result = result_future.result().result

#         self.get_logger().info(f'✅ Execution finished with error code: {traj_result.error_code}')

#     def create_pose_constraint(self, pose_stamped):
#         from moveit_msgs.msg import PositionConstraint, OrientationConstraint, Constraints
#         from shape_msgs.msg import SolidPrimitive

#         constraints = Constraints()

#         # Position constraint (small region around desired pose — adjust size as you like)
#         pos_constraint = PositionConstraint()
#         pos_constraint.header = pose_stamped.header
#         pos_constraint.link_name = 'ik_frame'
#         pos_constraint.target_point_offset.x = 0.0
#         pos_constraint.target_point_offset.y = 0.0
#         pos_constraint.target_point_offset.z = 0.0
#         primitive = SolidPrimitive()
#         primitive.type = SolidPrimitive.BOX
#         primitive.dimensions = [0.01, 0.01, 0.01]
#         pos_constraint.constraint_region.primitives.append(primitive)
#         pos_constraint.constraint_region.primitive_poses.append(pose_stamped.pose)
#         pos_constraint.weight = 1.0
#         constraints.position_constraints.append(pos_constraint)

#         # Orientation constraint (optional — lock orientation if needed)
#         # orient_constraint = OrientationConstraint()
#         # orient_constraint.header = pose_stamped.header
#         # orient_constraint.link_name = 'ik_frame'
#         # orient_constraint.orientation = pose_stamped.pose.orientation
#         # orient_constraint.absolute_x_axis_tolerance = 0.1
#         # orient_constraint.absolute_y_axis_tolerance = 0.1
#         # orient_constraint.absolute_z_axis_tolerance = 0.1
#         # orient_constraint.weight = 1.0
#         # constraints.orientation_constraints.append(orient_constraint)

#         return constraints


# def main(args=None):
#     rclpy.init(args=args)
#     node = MoveGroupMotionPlanner()
#     node.destroy_node()
#     rclpy.shutdown()


# if __name__ == '__main__':
#     main()











#!/usr/bin/env python3

import math
import rclpy
from rclpy.node import Node

from geometry_msgs.msg import PoseStamped, Quaternion
from moveit_msgs.msg import MotionPlanRequest, Constraints, PositionConstraint
from moveit_msgs.action import MoveGroup
from builtin_interfaces.msg import Duration
from trajectory_msgs.msg import JointTrajectoryPoint
from control_msgs.action import FollowJointTrajectory
from rclpy.action import ActionClient
from tf2_ros import Buffer, TransformListener, LookupException, ConnectivityException, ExtrapolationException
from shape_msgs.msg import SolidPrimitive


class MoveGroupMotionPlanner(Node):
    def __init__(self):
        super().__init__('move_group_motion_planner_client')

        self.move_group_client = ActionClient(self, MoveGroup, '/move_action')
        self.trajectory_client = ActionClient(self, FollowJointTrajectory, '/arm_controller/follow_joint_trajectory')

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.get_logger().info(' Waiting for /move_action server...')
        self.move_group_client.wait_for_server()
        self.get_logger().info(' /move_action server available.')

        self.get_logger().info(' Waiting for /follow_joint_trajectory server...')
        self.trajectory_client.wait_for_server()
        self.get_logger().info(' /follow_joint_trajectory server available.')

        # Example target position
        x_target, y_target = 0.105, 0.125
        cube_yaw = 0.0

        z_approach = 0.18
        z_pick = 0.015

        # Compute wrist angle continuously based on base→cube vector and cube yaw
        wrist_angle = self.compute_wrist_angle(x_target, y_target, cube_yaw)

        # Move to approach pose
        self.plan_and_execute(x_target, y_target, z_approach, wrist_angle)

        # Move to pick pose
        self.plan_and_execute(x_target, y_target, z_pick, wrist_angle)

    def plan_and_execute(self, x, y, z, wrist_angle):
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
        move_goal.planning_options.look_around = False
        move_goal.planning_options.replan = False

        self.get_logger().info(f' Planning to ({x:.3f}, {y:.3f}, {z:.3f}) with wrist {math.degrees(wrist_angle):.1f}°...')
        send_goal_future = self.move_group_client.send_goal_async(move_goal)
        rclpy.spin_until_future_complete(self, send_goal_future)
        goal_handle = send_goal_future.result()

        if not goal_handle.accepted:
            self.get_logger().error(' MoveGroup goal was rejected.')
            return

        self.get_logger().info(' Plan goal accepted. Waiting for result...')
        result_future = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(self, result_future)
        result = result_future.result().result

        if result.error_code.val != 1:
            self.get_logger().error(f' Planning failed with error code: {result.error_code.val}')
            return

        self.get_logger().info(' Plan computed successfully.')

        trajectory = result.planned_trajectory.joint_trajectory

        traj_goal = FollowJointTrajectory.Goal()
        traj_goal.trajectory = trajectory
        traj_goal.goal_time_tolerance = Duration(sec=1)

        self.get_logger().info(' Sending trajectory to controller...')
        send_traj_future = self.trajectory_client.send_goal_async(traj_goal)
        rclpy.spin_until_future_complete(self, send_traj_future)
        traj_goal_handle = send_traj_future.result()

        if not traj_goal_handle.accepted:
            self.get_logger().error(' Trajectory goal was rejected.')
            return

        self.get_logger().info(' Trajectory goal accepted. Waiting for result...')
        result_future = traj_goal_handle.get_result_async()
        rclpy.spin_until_future_complete(self, result_future)
        traj_result = result_future.result().result

        self.get_logger().info(f' Execution finished with error code: {traj_result.error_code}')

    def compute_wrist_angle(self, cube_x, cube_y, cube_yaw):
        base_x, base_y = self.get_base_position()

        # Angle from base to cube position
        dx = cube_x - base_x
        dy = cube_y - base_y
        approach_angle = math.atan2(dy, dx)

        # No snapping — allow continuous angles for flexibility
        offset = 0  # 90° because gripper closes along Y-axis

        # Final wrist angle
        wrist_angle = approach_angle + cube_yaw + offset

        # Normalize to [-pi, pi]
        wrist_angle = (wrist_angle + math.pi) % (2 * math.pi) - math.pi

        self.get_logger().info(
            f' Base→Cube angle: {math.degrees(approach_angle):.1f}°, '
            f'cube yaw: {math.degrees(cube_yaw):.1f}°, offset: 90° → wrist: {math.degrees(wrist_angle):.1f}°'
        )

        return wrist_angle





    def get_base_position(self):
        try:
            trans = self.tf_buffer.lookup_transform('world', 'base_link', rclpy.time.Time())
            base_x = trans.transform.translation.x
            base_y = trans.transform.translation.y
            self.get_logger().info(f' Base position in world: ({base_x:.3f}, {base_y:.3f})')
        except (LookupException, ConnectivityException, ExtrapolationException):
            self.get_logger().warn(' Could not get transform from world to base_link. Assuming (0,0)')
            base_x, base_y = 0.0, 0.0
        return base_x, base_y

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

# from geometry_msgs.msg import PoseStamped
# from moveit_msgs.msg import MotionPlanRequest, Constraints, PositionConstraint, JointConstraint
# from moveit_msgs.action import MoveGroup
# from builtin_interfaces.msg import Duration
# from control_msgs.action import FollowJointTrajectory
# from rclpy.action import ActionClient
# from tf2_ros import Buffer, TransformListener, LookupException, ConnectivityException, ExtrapolationException
# from shape_msgs.msg import SolidPrimitive


# class MoveGroupMotionPlanner(Node):
#     def __init__(self):
#         super().__init__('move_group_motion_planner_client')

#         self.move_group_client = ActionClient(self, MoveGroup, '/move_action')
#         self.trajectory_client = ActionClient(self, FollowJointTrajectory, '/arm_controller/follow_joint_trajectory')

#         self.tf_buffer = Buffer()
#         self.tf_listener = TransformListener(self.tf_buffer, self)

#         self.get_logger().info('✅ Waiting for /move_action server...')
#         self.move_group_client.wait_for_server()
#         self.get_logger().info('✅ /move_action server available.')

#         self.get_logger().info('✅ Waiting for /follow_joint_trajectory server...')
#         self.trajectory_client.wait_for_server()
#         self.get_logger().info('✅ /follow_joint_trajectory server available.')

#         # Example target position
#         x_target, y_target = 0.105, 0.125
#         cube_yaw = 0.0

#         z_approach = 0.18
#         z_pick = 0.015

#         # Compute wrist angle based on base to cube position
#         wrist_angle = self.compute_wrist_angle(x_target, y_target, cube_yaw)

#         # Move to approach pose
#         self.plan_and_execute(x_target, y_target, z_approach, wrist_angle)

#         # Move to pick pose
#         self.plan_and_execute(x_target, y_target, z_pick, wrist_angle)

#     def plan_and_execute(self, x, y, z, wrist_angle):
#         # Build plan request
#         plan_request = MotionPlanRequest()
#         plan_request.group_name = 'arm'
#         plan_request.allowed_planning_time = 5.0
#         plan_request.num_planning_attempts = 20
#         plan_request.max_velocity_scaling_factor = 1.0
#         plan_request.max_acceleration_scaling_factor = 1.0

#         # Add position constraint
#         plan_request.goal_constraints.append(self.create_position_constraint(x, y, z, wrist_angle))

#         # Send to MoveGroup
#         move_goal = MoveGroup.Goal()
#         move_goal.request = plan_request
#         move_goal.planning_options.plan_only = False

#         self.get_logger().info(f'🚀 Planning to ({x:.3f}, {y:.3f}, {z:.3f}) with wrist {math.degrees(wrist_angle):.1f}°...')
#         send_goal_future = self.move_group_client.send_goal_async(move_goal)
#         rclpy.spin_until_future_complete(self, send_goal_future)
#         goal_handle = send_goal_future.result()

#         if not goal_handle.accepted:
#             self.get_logger().error('❌ MoveGroup goal was rejected.')
#             return

#         self.get_logger().info('✅ Plan goal accepted. Waiting for result...')
#         result_future = goal_handle.get_result_async()
#         rclpy.spin_until_future_complete(self, result_future)
#         result = result_future.result().result

#         if result.error_code.val != 1:
#             self.get_logger().error(f'❌ Planning failed with error code: {result.error_code.val}')
#             return

#         self.get_logger().info('✅ Plan computed successfully.')

#         # Send trajectory to controller
#         trajectory = result.planned_trajectory.joint_trajectory
#         traj_goal = FollowJointTrajectory.Goal()
#         traj_goal.trajectory = trajectory
#         traj_goal.goal_time_tolerance = Duration(sec=1)

#         self.get_logger().info('📤 Sending trajectory to controller...')
#         send_traj_future = self.trajectory_client.send_goal_async(traj_goal)
#         rclpy.spin_until_future_complete(self, send_traj_future)
#         traj_goal_handle = send_traj_future.result()

#         if not traj_goal_handle.accepted:
#             self.get_logger().error('❌ Trajectory goal was rejected.')
#             return

#         self.get_logger().info('✅ Trajectory goal accepted. Waiting for result...')
#         result_future = traj_goal_handle.get_result_async()
#         rclpy.spin_until_future_complete(self, result_future)
#         traj_result = result_future.result().result

#         self.get_logger().info(f'🎉 Execution finished with error code: {traj_result.error_code}')

#     def compute_wrist_angle(self, cube_x, cube_y, cube_yaw):
#         base_x, base_y = self.get_base_position()
#         dx = cube_x - base_x
#         dy = cube_y - base_y
#         approach_angle = math.atan2(dy, dx)
#         offset = 0
#         wrist_angle = (approach_angle + cube_yaw + offset + math.pi) % (2 * math.pi) - math.pi

#         self.get_logger().info(
#             f'🧭 Base→Cube angle: {math.degrees(approach_angle):.1f}°, '
#             f'cube yaw: {math.degrees(cube_yaw):.1f}°, offset: 0° → wrist: {math.degrees(wrist_angle):.1f}°'
#         )
#         return wrist_angle

#     def get_base_position(self):
#         try:
#             trans = self.tf_buffer.lookup_transform('world', 'base_link', rclpy.time.Time())
#             base_x = trans.transform.translation.x
#             base_y = trans.transform.translation.y
#             self.get_logger().info(f'📍 Base position in world: ({base_x:.3f}, {base_y:.3f})')
#         except (LookupException, ConnectivityException, ExtrapolationException):
#             self.get_logger().warn('⚠️ Could not get transform from world to base_link. Assuming (0,0)')
#             base_x, base_y = 0.0, 0.0
#         return base_x, base_y

#     def create_position_constraint(self, x, y, z, wrist_angle):
#         constraints = Constraints()

#         pos_constraint = PositionConstraint()
#         pos_constraint.header.frame_id = 'world'
#         pos_constraint.link_name = 'ik_frame'
#         pos_constraint.target_point_offset.x = 0.0
#         pos_constraint.target_point_offset.y = 0.0
#         pos_constraint.target_point_offset.z = 0.0

#         primitive = SolidPrimitive()
#         primitive.type = SolidPrimitive.BOX
#         primitive.dimensions = [0.04, 0.04, 0.04]  # relaxed region
#         pos_constraint.constraint_region.primitives.append(primitive)

#         pose = PoseStamped()
#         pose.header.frame_id = 'world'
#         pose.pose.position.x = x
#         pose.pose.position.y = y
#         pose.pose.position.z = z
#         pos_constraint.constraint_region.primitive_poses.append(pose.pose)
#         pos_constraint.weight = 1.0
#         constraints.position_constraints.append(pos_constraint)

#         # Optional wrist joint constraint
#         joint_constraint = JointConstraint()
#         joint_constraint.joint_name = 'joint_five'
#         joint_constraint.position = wrist_angle
#         joint_constraint.tolerance_above = math.radians(8)
#         joint_constraint.tolerance_below = math.radians(8)
#         joint_constraint.weight = 1.0
#         constraints.joint_constraints.append(joint_constraint)

#         return constraints


# def main(args=None):
#     rclpy.init(args=args)
#     node = MoveGroupMotionPlanner()
#     node.destroy_node()
#     rclpy.shutdown()


# if __name__ == '__main__':
#     main()
