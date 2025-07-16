#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import serial
import time

from geometry_msgs.msg import PoseStamped
from moveit_msgs.srv import GetPositionIK
from cube_msgs.msg import ColorPoseStamped
from shape_msgs.msg import SolidPrimitive
from moveit_msgs.msg import Constraints, PositionConstraint

class FastIKPickAndPlace(Node):
    def __init__(self):
        super().__init__('fast_ik_pick_and_place')

        # IK Service Client
        self.ik_client = self.create_client(GetPositionIK, '/compute_ik')
        while not self.ik_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for /compute_ik service...')

        # Serial to Arduino
        try:
            self.arduino = serial.Serial('/dev/ttyACM0', 57600, timeout=1)
            time.sleep(2)
            self.arduino.write(b'DeskMod\n')
            time.sleep(0.1)
            self.get_logger().info("✅ Connected to Arduino")
        except (serial.SerialException, OSError) as e:
            self.get_logger().error(f'❌ Serial error: {e}')
            self.arduino = None

        # Pose subscription
        self.create_subscription(ColorPoseStamped, '/detected_color_pose', self.color_pose_callback, 10)
        

        self.approach_z = 0.20
        self.last_pose = None

        self.get_logger().info('📡 FastIKPickAndPlace ready.')

    def color_pose_callback(self, msg):
        x, y = msg.pose.position.x, msg.pose.position.y

        # Debounce redundant requests
        if self.last_pose == (x, y):
            return

        self.last_pose = (x, y)
        self.get_logger().info(f'📦 Getting IK for ({x:.3f}, {y:.3f}, {self.approach_z:.3f})')

        # Prepare IK request
        ik_request = GetPositionIK.Request()
        ik_request.ik_request.group_name = 'arm'
        ik_request.ik_request.ik_link_name = 'ik_frame'
        ik_request.ik_request.timeout.sec = 1

        pose = PoseStamped()
        pose.header.frame_id = 'world'
        pose.pose.position.x = x
        pose.pose.position.y = y
        pose.pose.position.z = self.approach_z
        pose.pose.orientation.w = 1.0

        ik_request.ik_request.pose_stamped = pose

        future = self.ik_client.call_async(ik_request)
        future.add_done_callback(self.handle_ik_result)

    def handle_ik_result(self, future):
        try:
            response = future.result()
            if response.error_code.val != 1:
                self.get_logger().error(f'❌ IK failed with code {response.error_code.val}')
                return

            joint_state = response.solution.joint_state
            self.get_logger().info(f'✅ IK success: {joint_state.position}')

            self.send_to_arduino(joint_state.name, joint_state.position)

        except Exception as e:
            self.get_logger().error(f'IK service call failed: {e}')

    def send_to_arduino(self, joint_names, positions):
        if not self.arduino or not self.arduino.is_open:
            self.get_logger().warn('⚠️ Arduino not connected, skipping send.')
            return

        joint_map = dict(zip(joint_names, positions))
        joint_limits = [
            {'name': 'joint_one', 'lower': -1.57, 'upper': 1.57, 'reverse': True},
            {'name': 'joint_two', 'lower': -1.307, 'upper': 0.617, 'reverse': False},
            {'name': 'joint_three', 'lower': -1.57, 'upper': 1.57, 'reverse': True},
            {'name': 'joint_four', 'lower': -1.57, 'upper': 1.57, 'reverse': False},
            {'name': 'joint_five', 'lower': -1.57, 'upper': 1.57, 'reverse': False},
            {'name': 'joint_six', 'lower': 0, 'upper': 100, 'reverse': False},
        ]

        positions_out = []
        for joint in joint_limits:
            name = joint['name']
            if name in joint_map:
                val = joint_map[name]
                if joint['reverse']:
                    val = -val
                mapped = int((val - joint['lower']) * 100 / (joint['upper'] - joint['lower']))
                mapped = max(0, min(100, mapped))
                positions_out.append(mapped)
            else:
                positions_out.append(0)

        command = f"D,{','.join(str(v) for v in positions_out)},AX\n"
        self.get_logger().info(f'📡 Sending: {command.strip()}')

        try:
            self.arduino.write(command.encode())
            self.arduino.flush()
        except serial.SerialException as e:
            self.get_logger().error(f'Serial error: {e}')

def main(args=None):
    rclpy.init(args=args)
    node = FastIKPickAndPlace()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
