import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy,JointState
import math
import serial
import time

class SerialNode(Node):
    def __init__(self):
        super().__init__('serial')

        # Setup serial
        try:
            self.arduino = serial.Serial('/dev/ttyACM0', 57600, timeout=1)
            time.sleep(2)
            self.get_logger().info('Connected to Arduino on /dev/ttyACM0')
        except serial.SerialException as e:
            self.get_logger().error(f'Failed to connect to Arduino: {e}')
            self.arduino = None

        # Subscribe to joystick topic
        #self.subscription = self.create_subscription(Joy, 'joy', self.joy_callback, 10)

        self.subscription = self.create_subscription(JointState, '/joint_states', self.joint_state_callback, 10)


    def joint_state_callback(self, msg):
        if not self.arduino or not self.arduino.is_open:
            self.get_logger().warn("Arduino connection not open")
            return

        def to_angle_int(rad_angle, min_deg, max_deg):
        # Map radians [-1.57, 1.57] to degrees [0, 180]
            deg = ((rad_angle + 1.57) / 3.14) * 180  # Shift [-1.57, 1.57] to [0, 3.14], normalize, scale to [0, 180]
        # Log raw radian and mapped degree for debugging
            self.get_logger().info(f"Rad: {rad_angle:.2f}, Mapped Deg: {deg:.2f}")
        # Clamp to joint-specific degree range
            deg = max(min_deg, min(max_deg, deg))
        # Map to 0-100 for serial command
            mapped = int((deg - min_deg) / (max_deg - min_deg) * 100) if max_deg != min_deg else 0
            self.get_logger().info(f"Clamped Deg: {deg:.2f}, Serial Value: {mapped}")
            return mapped

        j1 = to_angle_int(msg.position[0], 0, 160)
        j2 = to_angle_int(msg.position[1], 15, 125)
        j3 = to_angle_int(msg.position[2], 0, 180)
        j4 = to_angle_int(msg.position[3], 0, 180)
        j5 = to_angle_int(msg.position[4], 0, 180)
        j6 = to_angle_int(msg.position[5], 20, 95)

        joint_commands = f"D,{j1},{j2},{j3},{j4},{j5},{j6},A" + "X"  # ends with 'X'

        try:
            self.arduino.write(joint_commands.encode())
            self.get_logger().info(f"Sent: {joint_commands}")
        except serial.SerialException as e:
            self.get_logger().error(f"Serial write error: {e}")

        # Gripper toggle state
        #self.prev_gripper_button = 0
        #self.gripper_state = 0  # 0 = off, 1 = on

    # def joy_callback(self, msg):
    #     if not self.arduino or not self.arduino.is_open:
    #         self.get_logger().warn("Arduino connection not open")
    #         return

    #     # Digital joint control
    #     j1 = self.get_joint_from_buttons(msg.buttons[1], msg.buttons[3])  # btn2, btn4
    #     j2 = self.get_joint_from_buttons(msg.buttons[0], msg.buttons[2])  # btn1, btn3
    #     j5 = self.get_joint_from_buttons(msg.buttons[4], msg.buttons[5])  # btn5, btn6
    #     j6 = self.get_joint_from_buttons(msg.buttons[6], msg.buttons[7])  # btn7, btn8

    #     # Analog axes for joints 3 & 4
    #     j3 = self.axis_to_command(msg.axes[1])  # left stick vertical
    #     j4 = self.axis_to_command(msg.axes[0])  # left stick horizontal

    #     # Gripper toggle using button 9 (index 8)
    #     gripper_button = msg.buttons[8] if len(msg.buttons) > 8 else 0
    #     send_gripper_toggle = False

    #     if gripper_button == 1 and self.prev_gripper_button == 0:
    #         # Button pressed (rising edge)
    #         self.gripper_state = 0 if self.gripper_state == 1 else 1
    #         send_gripper_toggle = True

    #     self.prev_gripper_button = gripper_button

    #     # Only send 'G' once when toggled, otherwise 'g' (idle gripper command)
    #     gripper_cmd = b'G' if send_gripper_toggle else b'g'

    #     # Combine all into aJoy 7-byte command
    #     joint_commands = bytearray([j1, j2, j3, j4, j5, j6]) + gripper_cmd

    #     try:
    #         self.arduino.write(joint_commands)
    #         self.get_logger().info(f"Sent: {list(joint_commands)}")
    #     except serial.SerialException as e:
    #         self.get_logger().error(f"Serial write error: {e}")

    # def get_joint_from_buttons(self, backwa    # def joy_callback(self, msg):





def main(args=None):
    rclpy.init(args=args)
    node = SerialNode()
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

    


