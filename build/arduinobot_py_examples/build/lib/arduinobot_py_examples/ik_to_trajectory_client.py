#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.task import Future
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from control_msgs.action import FollowJointTrajectory
from moveit_msgs.srv import GetPositionIK
from geometry_msgs.msg import PoseStamped
from builtin_interfaces.msg import Duration

class IKToTrajectoryClient(Node):
    def __init__(self):
        super().__init__('ik_to_trajectory_client')

        # IK Service Client
        self.ik_client = self.create_client(GetPositionIK, '/compute_ik')
        while not self.ik_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for /compute_ik service...')

        # Trajectory Action Client
        self.trajectory_client = ActionClient(
            self, FollowJointTrajectory, '/arm_controller/follow_joint_trajectory'
        )
        self.trajectory_client.wait_for_server()
        self.get_logger().info('/arm_controller/follow_joint_trajectory action server available.')

        # Call IK and send trajectory
        self.call_ik_service()

    def call_ik_service(self):
        request = GetPositionIK.Request()
        request.ik_request.group_name = 'arm'
        request.ik_request.ik_link_name = 'link_five'

        # Target pose
        pose_stamped = PoseStamped()
        pose_stamped.header.frame_id = 'world'
        pose_stamped.pose.position.x = 0.05
        pose_stamped.pose.position.y = 0.1
        pose_stamped.pose.position.z = 0.1
        pose_stamped.pose.orientation.x = 0.0
        pose_stamped.pose.orientation.y = 0.0
        pose_stamped.pose.orientation.z = 0.0
        pose_stamped.pose.orientation.w = 1.0

        request.ik_request.pose_stamped = pose_stamped
        request.ik_request.timeout.sec = 2

        self.get_logger().info('Calling IK service...')
        future = self.ik_client.call_async(request)
        future.add_done_callback(self.ik_response_callback)

    def ik_response_callback(self, future: Future):
        try:
            response = future.result()
            error_code = response.error_code.val
            if error_code != 1:
                self.get_logger().error(f'IK failed with error code {error_code}')
                return

            joint_state = response.solution.joint_state
            joint_names = joint_state.name
            joint_positions = joint_state.position

            self.get_logger().info(f'IK Solution: {dict(zip(joint_names, joint_positions))}')

            # Send trajectory goal
            self.send_trajectory_goal(joint_names, joint_positions)

        except Exception as e:
            self.get_logger().error(f'Failed to call IK service: {e}')

    def send_trajectory_goal(self, joint_names, joint_positions):
        goal_msg = FollowJointTrajectory.Goal()

        goal_msg.trajectory.joint_names = joint_names[:5]  # only send controlled joints

        point = JointTrajectoryPoint()
        point.positions = joint_positions[:5]  # same — only the 5 arm joints
        point.time_from_start = Duration(sec=2)

        goal_msg.trajectory.points.append(point)

        self.get_logger().info('Sending trajectory goal...')
        self.trajectory_client.send_goal_async(goal_msg, feedback_callback=self.feedback_callback)

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info(f'Feedback received.')

def main(args=None):
    rclpy.init(args=args)
    node = IKToTrajectoryClient()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
