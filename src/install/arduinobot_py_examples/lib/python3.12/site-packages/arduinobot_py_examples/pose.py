#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
import time

class PosePublisher(Node):
    def __init__(self):
        super().__init__('pose_publisher')
        self.publisher_ = self.create_publisher(PoseStamped, 'target_pose', 10)

        # Declare delay parameter (seconds)
        self.declare_parameter('delay_seconds', 5.0)
        self.delay_seconds = self.get_parameter('delay_seconds').value

        self.get_logger().info(f'PosePublisher started. Publishing poses every {self.delay_seconds} seconds.')

        # List of target positions (x, y, z)
        self.poses = [
            (0.105, 0.125, 0.02)

        ]

        self.publish_poses()

    def publish_poses(self):
        for i, (x, y, z) in enumerate(self.poses):
            pose_stamped = PoseStamped()
            pose_stamped.header.frame_id = 'world'
            pose_stamped.header.stamp = self.get_clock().now().to_msg()
            pose_stamped.pose.position.x = x
            pose_stamped.pose.position.y = y
            pose_stamped.pose.position.z = z
            pose_stamped.pose.orientation.x = 0.0
            pose_stamped.pose.orientation.y = 0.0
            pose_stamped.pose.orientation.z = 0.0
            pose_stamped.pose.orientation.w = 1.0

            self.publisher_.publish(pose_stamped)
            self.get_logger().info(f'Published pose {i+1}: {pose_stamped.pose}')

            time.sleep(self.delay_seconds)

        self.get_logger().info('All poses published. Shutting down node gracefully.')
        rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    node = PosePublisher()
    rclpy.spin(node)

if __name__ == '__main__':
    main()










