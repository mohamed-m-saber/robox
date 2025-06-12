import rclpy 
from rclpy.node import Node
from rclpy.action import ActionServer
from arm_msgs import act 
import time


class Taskserver(Node):
    def __init__(self):
        super().__init__("Task_server")
        self.get_logger().info("starting the server")
        self.action_server=ActionServer(self, act, "task_server", self.goalCallback)


    def goalCallback(self,goal_handle):
        self.get_logger().info("Received goal request with order %d" % goal_handle.request.order)

        feedback_msg=Taskserver.Feedback()
        
