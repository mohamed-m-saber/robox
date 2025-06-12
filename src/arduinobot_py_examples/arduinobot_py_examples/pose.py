import rclpy
from rclpy.node import Node
from arduinobot_py_examples.srv import GoToPose  # Your custom service
from geometry_msgs.msg import Pose

class GoToPoseClient(Node):

    def __init__(self):
        super().__init__('go_to_pose_client')
        self.cli = self.create_client(GoToPose, 'go_to_pose')

        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for go_to_pose service...')

        self.get_logger().info('Service is available.')

    def send_goal(self, pose):
        request = GoToPose.Request()
        request.target_pose = pose

        future = self.cli.call_async(request)
        rclpy.spin_until_future_complete(self, future)

        if future.result() is not None:
            result = future.result()
            if result.success:
                self.get_logger().info(f"Success: {result.message}")
            else:
                self.get_logger().warn(f"Failed: {result.message}")
        else:
            self.get_logger().error("Service call failed.")

def main(args=None):
    rclpy.init(args=args)
    client_node = GoToPoseClient()

    # Create a pose message
    target_pose = Pose()
    target_pose.position.x = 0.4
    target_pose.position.y = 0.1
    target_pose.position.z = 0.5
    target_pose.orientation.w = 1.0  # neutral rotation

    client_node.send_goal(target_pose)

    client_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
