#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseArray, Pose
from visualization_msgs.msg import Marker, MarkerArray
from std_msgs.msg import ColorRGBA
import math


class CubePosePublisher(Node):
    def __init__(self):
        super().__init__('cube_pose_publisher_fixed')

        self.pose_pub = self.create_publisher(PoseArray, 'cube_poses', 10)
        self.marker_pub = self.create_publisher(MarkerArray, 'cube_markers', 10)

        self.timer = self.create_timer(2.0, self.publish_fixed_cubes)

        self.get_logger().info('✅ Fixed Cube Pose and Marker Publisher running...')

        self.cube_size = 0.04  # 4cm cube

    def publish_fixed_cubes(self):
        pose_array = PoseArray()
        pose_array.header.frame_id = 'world'
        pose_array.header.stamp = self.get_clock().now().to_msg()

        marker_array = MarkerArray()
        timestamp = self.get_clock().now().to_msg()

        # Define 6 fixed cube poses (X, Y, Z, Yaw in radians)
        fixed_cubes = [
            (0.0, 0.0, 0.02, math.radians(0)),
            # (0.15, 0.05, 0.02, math.radians(45)),
            # (0.10, 0.10, 0.02, math.radians(90)),
            # (0.18, 0.22, 0.02, math.radians(135)),
            # (0.20, 0.12, 0.02, math.radians(-45)),
            # (0.05, 0.22, 0.02, math.radians(60)),
        ]

        for i, (x, y, z, yaw) in enumerate(fixed_cubes):
            pose = Pose()
            pose.position.x = x
            pose.position.y = y
            pose.position.z = z
            pose.orientation.z = math.sin(yaw / 2.0)
            pose.orientation.w = math.cos(yaw / 2.0)
            pose_array.poses.append(pose)

            marker = Marker()
            marker.header.frame_id = 'world'
            marker.header.stamp = timestamp
            marker.ns = 'cubes'
            marker.id = i
            marker.type = Marker.CUBE
            marker.action = Marker.ADD
            marker.pose = pose
            marker.scale.x = self.cube_size
            marker.scale.y = self.cube_size
            marker.scale.z = self.cube_size
            marker.color = ColorRGBA(
                r=0.9,
                g=0.4,
                b=0.2,
                a=1.0
            )
            marker_array.markers.append(marker)

        self.pose_pub.publish(pose_array)
        self.marker_pub.publish(marker_array)
        self.get_logger().info(f'📦 Published {len(fixed_cubes)} fixed cube poses and markers.')


def main(args=None):
    rclpy.init(args=args)
    node = CubePosePublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
