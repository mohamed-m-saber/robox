# #!/usr/bin/env python3

# import rclpy
# from rclpy.node import Node
# from sensor_msgs.msg import JointState
# import serial
# import time


# class ArmSerialBridge(Node):
#     def __init__(self):
#         super().__init__('arm_serial_bridge')

#         # Connect to Arduino
#         self.arduino = None
#         self.setup_serial()

#         # Joint limits (updated to include joint_six)
#         self.joint_limits_rad = [
#             {'name': 'joint_one', 'lower': -1.57, 'upper': 1.57, 'reverse': True},
#             {'name': 'joint_two', 'lower': -1.307, 'upper': 0.617, 'reverse': False},
#             {'name': 'joint_three', 'lower': -1.57, 'upper': 1.57, 'reverse': True},
#             {'name': 'joint_four', 'lower': -1.57, 'upper': 1.57, 'reverse': False},
#             {'name': 'joint_five', 'lower': -1.57, 'upper': 1.57, 'reverse': False},
#             {'name': 'joint_six', 'lower': -1.57, 'upper': 1.57, 'reverse': False},
#         ]

#         # Subscribe to /joint_states
#         self.subscription = self.create_subscription(
#             JointState,
#             '/joint_states',
#             self.joint_state_callback,
#             10
#         )

#         self.get_logger().info("✅ ArmSerialBridge ready, subscribed to /joint_states")

#     def setup_serial(self):
#         try:
#             self.arduino = serial.Serial('/dev/ttyACM0', 57600, timeout=1)
#             time.sleep(3)
#             self.arduino.write(b'DeskMod\n')
#             time.sleep(0.1)
#             self.get_logger().info("✅ Connected to Arduino")
#         except (serial.SerialException, OSError) as e:
#             self.get_logger().error(f'Failed to connect to Arduino: {e}')

#     def joint_state_callback(self, msg):
#         name_to_position = dict(zip(msg.name, msg.position))

#         positions = []
#         joint_one_value = None

#         for joint in self.joint_limits_rad:
#             joint_name = joint['name']

#             if joint_name == 'joint_six':
#                 positions.append(0)  # Fixed value for joint_six

#             elif joint_name == 'joint_five':
#                 if joint_one_value is not None:
#                     positions.append((100-joint_one_value))
#                 else:
#                     positions.append(0)
#                     self.get_logger().warn("joint_one value not available when setting joint_five")

#             elif joint_name in name_to_position:
#                 val = name_to_position[joint_name]
#                 if joint['reverse']:
#                     val = -val
#                 mapped = self.map_value(val, joint['lower'], joint['upper'])

#                 if joint_name == 'joint_one':
#                     joint_one_value = mapped

#                 positions.append(mapped)
#             else:
#                 positions.append(0)
#                 self.get_logger().warn(f"Joint {joint_name} not found in /joint_states")

#         command = f"D,{','.join(str(v) for v in positions)},AX\n"
#         self.get_logger().info(f"Sending: {command.strip()}")

#         try:
#             if self.arduino and self.arduino.is_open:
#                 self.arduino.write(command.encode())
#                 self.arduino.flush()
#         except serial.SerialException as e:
#             self.get_logger().error(f"Serial write error: {e}")
#             self.setup_serial()

#     def map_value(self, value_rad, lower_rad, upper_rad):
#         value_rad = max(min(value_rad, upper_rad), lower_rad)
#         return int((value_rad - lower_rad) * 100 / (upper_rad - lower_rad))


# def main(args=None):
#     rclpy.init(args=args)
#     node = ArmSerialBridge()
#     try:
#         rclpy.spin(node)
#     except KeyboardInterrupt:
#         pass
#     finally:
#         if node.arduino and node.arduino.is_open:
#             node.arduino.close()
#         node.destroy_node()
#         rclpy.shutdown()


# if __name__ == '__main__':
#     main()











#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import serial
import time


class ArmSerialBridge(Node):
    def __init__(self):
        super().__init__('arm_serial_bridge')

        self.arduino = None
        self.setup_serial()

        self.joint_limits_rad = [
            {'name': 'joint_one', 'lower': -1.57, 'upper': 1.57, 'reverse': True},
            {'name': 'joint_two', 'lower': -1.307, 'upper': 0.617, 'reverse': False},
            {'name': 'joint_three', 'lower': -1.57, 'upper': 1.57, 'reverse': True},
            {'name': 'joint_four', 'lower': -1.57, 'upper': 1.57, 'reverse': False},
            {'name': 'joint_five', 'lower': -1.57, 'upper': 1.57, 'reverse': False},
            {'name': 'joint_six', 'lower': -1.57, 'upper': 1.57, 'reverse': False},
        ]

        self.subscription = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_state_callback,
            10
        )

        self.last_positions = None  # last sent mapped servo values
        self.get_logger().info("✅ ArmSerialBridge ready, subscribed to /joint_states")

    def setup_serial(self):
        try:
            self.arduino = serial.Serial('/dev/ttyACM1', 57600, timeout=1)
            time.sleep(3)
            self.arduino.write(b'DeskMod\n')
            time.sleep(0.1)
            self.get_logger().info("✅ Connected to Arduino")
        except (serial.SerialException, OSError) as e:
            self.get_logger().error(f'Failed to connect to Arduino: {e}')

    def joint_state_callback(self, msg):
        name_to_position = dict(zip(msg.name, msg.position))

        positions = []
        joint_one_value = None

        for joint in self.joint_limits_rad:
            joint_name = joint['name']

            if joint_name == 'joint_six':
                positions.append(0)

            elif joint_name == 'joint_five':
                if joint_one_value is not None:
                    positions.append(100 - joint_one_value)
                else:
                    positions.append(0)
                    self.get_logger().warn("joint_one value not available for joint_five")

            elif joint_name in name_to_position:
                val = name_to_position[joint_name]
                if joint['reverse']:
                    val = -val
                mapped = self.map_value(val, joint['lower'], joint['upper'])
                if joint_name == 'joint_one':
                    joint_one_value = mapped
                positions.append(mapped)
            else:
                positions.append(0)
                self.get_logger().warn(f"{joint_name} not found in /joint_states")

        # Check if positions have changed (with tolerance)
        if not self.positions_changed(positions, self.last_positions, tolerance=1):
            return  # skip redundant command

        self.last_positions = positions

        command = f"D,{','.join(str(v) for v in positions)},AX\n"
        self.get_logger().info(f"Sending: {command.strip()}")

        try:
            if self.arduino and self.arduino.is_open:
                self.arduino.write(command.encode())
                self.arduino.flush()
        except serial.SerialException as e:
            self.get_logger().error(f"Serial write error: {e}")
            self.setup_serial()

    def map_value(self, value_rad, lower_rad, upper_rad):
        value_rad = max(min(value_rad, upper_rad), lower_rad)
        return int((value_rad - lower_rad) * 100 / (upper_rad - lower_rad))

    def positions_changed(self, new_positions, last_positions, tolerance=1):
        if last_positions is None:
            return True
        for a, b in zip(new_positions, last_positions):
            if abs(a - b) >= tolerance:
                return True
        return False


def main(args=None):
    rclpy.init(args=args)
    node = ArmSerialBridge()
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
