import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
import serial
import time

class JoystickHandler(Node):
    def __init__(self):
        super().__init__('joystick_handler')

        # Setup serial
        try:
            self.arduino = serial.Serial('/dev/ttyACM0', 57600, timeout=1)
            time.sleep(2)
            self.get_logger().info('Connected to Arduino on /dev/ttyACM0')
        except serial.SerialException as e:
            self.get_logger().error(f'Failed to connect to Arduino: {e}')
            self.arduino = None

        # Subscribe to joystick topic
        self.subscription = self.create_subscription(Joy, 'joy', self.joy_callback, 10)

        # Gripper toggle state
        self.prev_gripper_button = 0
        self.gripper_state = 0  # 0 = off, 1 = on

    def joy_callback(self, msg):
        if not self.arduino or not self.arduino.is_open:
            self.get_logger().warn("Arduino connection not open")
            return

        # Digital joint control
        j1 = self.get_joint_from_buttons(msg.buttons[1], msg.buttons[3])  # btn2, btn4
        j2 = self.get_joint_from_buttons(msg.buttons[0], msg.buttons[2])  # btn1, btn3
        j5 = self.get_joint_from_buttons(msg.buttons[4], msg.buttons[5])  # btn5, btn6
        j6 = self.get_joint_from_buttons(msg.buttons[6], msg.buttons[7])  # btn7, btn8

        # Analog axes for joints 3 & 4
        j3 = self.axis_to_command(msg.axes[1])  # left stick vertical
        j4 = self.axis_to_command(msg.axes[0])  # left stick horizontal

        # Gripper toggle using button 9 (index 8)
        gripper_button = msg.buttons[8] if len(msg.buttons) > 8 else 0
        send_gripper_toggle = False

        if gripper_button == 1 and self.prev_gripper_button == 0:
            # Button pressed (rising edge)
            self.gripper_state = 0 if self.gripper_state == 1 else 1
            send_gripper_toggle = True

        self.prev_gripper_button = gripper_button

        # Only send 'G' once when toggled, otherwise 'g' (idle gripper command)
        gripper_cmd = b'G' if send_gripper_toggle else b'g'

        # Combine all into a 7-byte command
        joint_commands = bytearray([j1, j2, j3, j4, j5, j6]) + gripper_cmd

        try:
            self.arduino.write(joint_commands)
            self.get_logger().info(f"Sent: {list(joint_commands)}")
        except serial.SerialException as e:
            self.get_logger().error(f"Serial write error: {e}")

    def get_joint_from_buttons(self, backward, forward):
        """Returns 0 for back, 2 for forward, 1 for stop"""
        if forward == 1 and backward == 0:
            return 2
        elif backward == 1 and forward == 0:
            return 0
        else:
            return 1  # stop

    def axis_to_command(self, val):
        """Converts analog axis to stepper command"""
        if val > 0.5:
            return 2
        elif val < -0.5:
            return 0
        else:
            return 1

def main(args=None):
    rclpy.init(args=args)
    node = JoystickHandler()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if node.arduino and node.arduino.is_open:
            node.arduino.close()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

