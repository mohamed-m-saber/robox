# import rclpy

# from std_msgs.msg import String

# from rclpy.node import Node



# class SubscriberNode(Node):
#     def __init__(self):
#         super().__init__('subscriber_node')
#         self.subscription=self.create_subscription(String,'communication_topic',self.callBackFunction,15)

        


#     def callBackFunction(self,message):
        
     
#         self.get_logger().info(f"we received :{message.data}")



# def main():
#     rclpy.init()
#     node_subscriber=SubscriberNode()
#     rclpy.spin(node_subscriber)

#     node_subscriber.destroy_node()
#     rclpy.shutdown()


# if __name__ == '__main__':
#     main()

#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped, Pose
from arm_description.srv import GoToPose
import tf2_ros
import tf2_geometry_msgs

class RVizPosePublisher(Node):
    
    def __init__(self):
        super().__init__('rviz_pose_publisher')
        
        # Create service client
        self.go_to_pose_client = self.create_client(GoToPose, 'GoToPose')
        
        # Subscribe to RViz pose goals (2D Nav Goal or Pose Estimate)
        self.pose_subscriber = self.create_subscription(
            PoseStamped,
            '/move_base_simple/goal',  # RViz 2D Nav Goal topic
            self.pose_callback,
            10
        )
        
        # Also subscribe to pose estimate (if you want to use that)
        self.pose_estimate_subscriber = self.create_subscription(
            PoseStamped,
            '/initialpose',  # RViz Initial Pose topic
            self.pose_estimate_callback,
            10
        )
        
        # Subscribe to a custom target pose topic
        self.target_pose_subscriber = self.create_subscription(
            Pose,
            '/target_pose',
            self.target_pose_callback,
            10
        )
        
        # TF buffer for coordinate transformations
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)
        
        # Wait for service
        self.get_logger().info('🔍 Waiting for GoToPose service...')
        while not self.go_to_pose_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('   Service not available, waiting...')
        
        self.get_logger().info('✅ RViz Pose Publisher ready!')
        self.get_logger().info('📍 You can now:')
        self.get_logger().info('   • Use "2D Nav Goal" in RViz to send poses')
        self.get_logger().info('   • Use "Pose Estimate" in RViz to send poses')
        self.get_logger().info('   • Publish to /target_pose topic')
    
    def pose_callback(self, msg):
        """Handle pose from RViz 2D Nav Goal"""
        self.get_logger().info('🎯 Received pose from RViz 2D Nav Goal')
        self.send_pose_to_service(msg.pose, msg.header.frame_id)
    
    def pose_estimate_callback(self, msg):
        """Handle pose from RViz Initial Pose"""
        self.get_logger().info('🎯 Received pose from RViz Initial Pose')
        self.send_pose_to_service(msg.pose, msg.header.frame_id)
    
    def target_pose_callback(self, msg):
        """Handle pose from target_pose topic"""
        self.get_logger().info('🎯 Received pose from /target_pose topic')
        self.send_pose_to_service(msg, 'base_link')  # Assume base_link frame
    
    def send_pose_to_service(self, pose, frame_id='base_link'):
        """Send pose to the GoToPose service"""
        try:
            # Transform pose to base_link if needed
            if frame_id != 'base_link':
                pose = self.transform_pose(pose, frame_id, 'base_link')
            
            # Create service request
            request = GoToPose.Request()
            request.target_pose = pose
            
            self.get_logger().info(f'📤 Sending pose to service:')
            self.get_logger().info(f'   Position: x={pose.position.x:.3f}, y={pose.position.y:.3f}, z={pose.position.z:.3f}')
            self.get_logger().info(f'   Orientation: x={pose.orientation.x:.3f}, y={pose.orientation.y:.3f}, z={pose.orientation.z:.3f}, w={pose.orientation.w:.3f}')
            
            # Call service asynchronously
            future = self.go_to_pose_client.call_async(request)
            future.add_done_callback(self.service_response_callback)
            
        except Exception as e:
            self.get_logger().error(f'❌ Error sending pose to service: {str(e)}')
    
    def service_response_callback(self, future):
        """Handle service response"""
        try:
            response = future.result()
            if response.success:
                self.get_logger().info(f'✅ Service response: {response.message}')
            else:
                self.get_logger().error(f'❌ Service failed: {response.message}')
        except Exception as e:
            self.get_logger().error(f'❌ Service call failed: {str(e)}')
    
    def transform_pose(self, pose, from_frame, to_frame):
        """Transform pose between coordinate frames"""
        try:
            # Create PoseStamped message
            pose_stamped = PoseStamped()
            pose_stamped.header.frame_id = from_frame
            pose_stamped.header.stamp = self.get_clock().now().to_msg()
            pose_stamped.pose = pose
            
            # Transform the pose
            transform = self.tf_buffer.lookup_transform(
                to_frame, from_frame, rclpy.time.Time()
            )
            
            transformed_pose = tf2_geometry_msgs.do_transform_pose(pose_stamped, transform)
            return transformed_pose.pose
            
        except Exception as e:
            self.get_logger().warn(f'⚠️  Could not transform pose: {str(e)}')
            return pose  # Return original pose if transformation fails

def main(args=None):
    rclpy.init(args=args)
    
    node = RVizPosePublisher()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('👋 Shutting down RViz Pose Publisher')
    
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

