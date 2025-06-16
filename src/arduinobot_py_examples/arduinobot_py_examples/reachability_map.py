#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from visualization_msgs.msg import Marker, MarkerArray
from geometry_msgs.msg import Point
import math

class ReachabilityMap(Node):
    def __init__(self):
        super().__init__('reachability_map')
        self.marker_pub = self.create_publisher(MarkerArray, 'reachability_map', 10)
        self.timer = self.create_timer(0.5, self.publish_map)

        # Define reachability grid resolution and limits
        self.resolution = 0.05  # 5 cm
        self.x_range = (-0.2, 0.2)
        self.y_range = (-0.2, 0.2)
        self.z_range = (0.0, 0.4)
        self.reach_radius = 0.25  # Max reach distance from base_link

    def publish_map(self):
        marker_array = MarkerArray()
        marker_id = 0

        for x in self.frange(self.x_range[0], self.x_range[1], self.resolution):
            for y in self.frange(self.y_range[0], self.y_range[1], self.resolution):
                for z in self.frange(self.z_range[0], self.z_range[1], self.resolution):
                    distance = math.sqrt(x**2 + y**2 + z**2)
                    marker = Marker()
                    marker.header.frame_id = 'base_link'
                    marker.header.stamp = self.get_clock().now().to_msg()
                    marker.ns = "reachability"
                    marker.id = marker_id
                    marker.type = Marker.SPHERE
                    marker.action = Marker.ADD
                    marker.pose.position.x = x
                    marker.pose.position.y = y
                    marker.pose.position.z = z
                    marker.pose.orientation.w = 1.0
                    marker.scale.x = 0.015
                    marker.scale.y = 0.015
                    marker.scale.z = 0.015

                    # Color based on reachability
                    if distance <= self.reach_radius:
                        marker.color.r = 0.0
                        marker.color.g = 1.0
                        marker.color.b = 0.0
                        marker.color.a = 0.5
                    else:
                        marker.color.r = 1.0
                        marker.color.g = 0.0
                        marker.color.b = 0.0
                        marker.color.a = 0.2

                    marker.lifetime.sec = 2
                    marker_array.markers.append(marker)
                    marker_id += 1

        self.marker_pub.publish(marker_array)

    def frange(self, start, stop, step):
        while start <= stop:
            yield start
            start += step

def main(args=None):
    rclpy.init(args=args)
    node = ReachabilityMap()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
