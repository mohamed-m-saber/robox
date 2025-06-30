# #!/usr/bin/env python3

# import rclpy
# from rclpy.node import Node
# from trajectory_msgs.msg import JointTrajectoryPoint
# from sensor_msgs.msg import JointState
# import serial
# import time
# from rclpy.qos import QoSProfile, QoSReliabilityPolicy

# class SerialNode(Node):
#     def __init__(self):
#         super().__init__('serial_node')
        
#         # Serial setup
#         self.arduino = None
#         self.setup_serial()
        
#         self.joint_order = [
#             'joint_one',
#             'joint_two',
#             'joint_three',
#             'joint_four',
#             'joint_five',
#             'joint_six'
#         ]
        
#         # QoS configuration
#         qos = QoSProfile(
#             reliability=QoSReliabilityPolicy.RELIABLE,
#             depth=10
#         )
        
#         # Subscribe to joint states
#         self.subscription = self.create_subscription(
#             JointState,
#             '/joint_states',
#             self.joint_state_callback,
#             qos
#         )
#         self.get_logger().info("Serial node initialized")

#         # Joint limits and reversal flags
#         self.joint_limits_rad = [
#             {'name': 'joint_one', 'lower': -1.57, 'upper': 1.220, 'reverse': True},
#             {'name': 'joint_two', 'lower': -1.307, 'upper': 0.617, 'reverse': False},
#             {'name': 'joint_three', 'lower': -1.57, 'upper': 1.57, 'reverse': True},   # <--- REVERSED
#             {'name': 'joint_four', 'lower': -1.57, 'upper': 1.57, 'reverse': False},
#             {'name': 'joint_five', 'lower': -1.57, 'upper': 1.570, 'reverse': False},
#             {'name': 'joint_six', 'lower': -1.221, 'upper': 0.097, 'reverse': False}
#         ]

#     def setup_serial(self):
#         try:
#             self.arduino = serial.Serial('/dev/ttyACM0', 57600, timeout=1)
#             time.sleep(3)  # Wait for Arduino reset
#             self.arduino.write(b'DeskMod\n')  # Set Arduino to serial mode
#             time.sleep(0.1)
#             self.get_logger().info('Connected to Arduino')
#         except (serial.SerialException, OSError) as e:
#             self.get_logger().error(f'Failed to connect to Arduino: {e}')

#     def joint_state_callback(self, msg):
#         self.get_logger().info(f"Received joint state: names={msg.name}, positions={msg.position}")
#         try:
#             joint_positions = dict(zip(msg.name, msg.position))
#             positions = []
#             for name in self.joint_order:
#                 if name in joint_positions:
#                     positions.append(joint_positions[name])
#                 else:
#                     self.get_logger().warn(f"Joint {name} not found, using 0.0")
#                     positions.append(0.0)

#             self.send_trajectory_to_arduino(positions)

#         except KeyError as e:
#             self.get_logger().error(f"Error mapping joints: {e}")

#     def send_trajectory_to_arduino(self, positions):
#         if not self.arduino or not self.arduino.is_open:
#             self.get_logger().warn("Arduino connection not open, attempting reconnect")
#             self.setup_serial()
#             return False

#         def map_value(value_rad, lower_rad, upper_rad):
#             if value_rad > upper_rad or value_rad < lower_rad:
#                 self.get_logger().warn(f"Value {value_rad} out of bounds [{lower_rad}, {upper_rad}]")
#             value_rad = max(min(value_rad, upper_rad), lower_rad)
#             return int((value_rad - lower_rad) * 100 / (upper_rad - lower_rad))

#         mapped_values = []
#         for joint, val in zip(self.joint_limits_rad, positions):
#             if joint['reverse']:
#                 self.get_logger().info(f"Inverting {joint['name']} position from {val} to {-val}")
#                 val = -val
#             mapped_values.append(map_value(val, joint['lower'], joint['upper']))

#         joint_commands = f"D,{','.join(str(v) for v in mapped_values)},AX\n"
        
#         self.get_logger().info(f"Sending command: {joint_commands}")
#         self.get_logger().info(f"Mapped gripper value: {mapped_values[5]}")

#         try:
#             self.arduino.write(joint_commands.encode())
#             self.get_logger().info(f"Sent: {joint_commands}")
#             self.arduino.flush()
#             return True  
#         except serial.SerialException as e:
#             self.get_logger().error(f"Serial write error: {e}")
#             self.setup_serial()
#             return False

# def main(args=None):
#     rclpy.init(args=args)
#     node = SerialNode()
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
















# #!/usr/bin/env python3

# import rclpy
# from rclpy.node import Node
# from std_msgs.msg import Float64MultiArray
# import serial
# import time
# from rclpy.qos import QoSProfile, QoSReliabilityPolicy

# class SerialBridgeNode(Node):
#     def __init__(self):
#         super().__init__('serial_bridge_node')

#         self.declare_parameter('serial_port', '/dev/ttyACM0')
#         self.declare_parameter('baudrate', 57600)

#         self.arduino = None
#         self.setup_serial()

#         qos = QoSProfile(
#             reliability=QoSReliabilityPolicy.RELIABLE,
#             depth=10
#         )

#         self.joint_positions = [0.0] * 5
#         self.gripper_position = 50.0  # default gripper midpoint

#         self.create_subscription(
#             Float64MultiArray,
#             '/final_joint_positions',
#             self.final_positions_callback,
#             qos
#         )

#         self.create_subscription(
#             Float64MultiArray,
#             '/gripper_position',
#             self.gripper_position_callback,
#             qos
#         )

#         self.get_logger().info("Serial Bridge Node with handshake and gripper support ready.")

#         def setup_serial(self):
#             port = self.get_parameter('serial_port').get_parameter_value().string_value
#             baud = self.get_parameter('baudrate').get_parameter_value().integer_value
#             try:
#                 self.arduino = serial.Serial(port, baud, timeout=1)
#                 time.sleep(3)

#                 self.get_logger().info("Waiting for Arduino to become READY...")
#                 while True:
#                     line = self.arduino.readline().decode(errors='ignore').strip()
#                     if line == "READY":
#                         break
#                 self.get_logger().info("Arduino is READY.")

#                 # Flush input/output buffers so no old data is waiting
#                 self.arduino.reset_input_buffer()
#                 self.arduino.reset_output_buffer()
#                 time.sleep(0.5)

#                 self.arduino.write(b'DeskMod\n')
#                 time.sleep(0.2)
#                 self.get_logger().info(f'Connected to Arduino on {port} at {baud} baud.')

#             except (serial.SerialException, OSError) as e:
#                 self.get_logger().error(f'Failed to connect to Arduino: {e}')


#     def final_positions_callback(self, msg):
#         if len(msg.data) != 5:
#             self.get_logger().error(f"Expected 5 joint positions, got {len(msg.data)}")
#             return

#         self.joint_positions = list(msg.data)
#         self.send_command_to_arduino()

#     def gripper_position_callback(self, msg):
#         if len(msg.data) != 1:
#             self.get_logger().warn(f"Expected single value for gripper, got {len(msg.data)}")
#             return
#         self.gripper_position = msg.data[0]

#     def send_command_to_arduino(self):
#         if not self.arduino or not self.arduino.is_open:
#             self.get_logger().error("Serial port not open")
#             self.setup_serial()
#             return

#         joint_limits = [
#             {'lower': -1.57, 'upper': 1.22, 'reverse': True},   # joint 1
#             {'lower': -1.307, 'upper': 0.617, 'reverse': False}, # joint 2
#             {'lower': -1.57, 'upper': 1.57, 'reverse': True},    # joint 3
#             {'lower': -1.57, 'upper': 1.57, 'reverse': False},   # joint 4
#             {'lower': -1.57, 'upper': 1.57, 'reverse': False},   # joint 5
#         ]

#         mapped_positions = []
#         for i in range(5):
#             lower = joint_limits[i]['lower']
#             upper = joint_limits[i]['upper']
#             val = max(min(self.joint_positions[i], upper), lower)

#             if joint_limits[i]['reverse']:
#                 val = -val

#             mapped_val = int((val - lower) * 100 / (upper - lower))
#             mapped_positions.append(mapped_val)

#         gripper_val = int(self.gripper_position)
#         mapped_positions.append(gripper_val)

#         command = f"D,{','.join(map(str, mapped_positions))},AX\n"
#         self.get_logger().info(f"Sending: {command.strip()}")

#         try:
#             self.arduino.write(command.encode())
#             self.arduino.flush()
#             self.get_logger().info("Command sent to Arduino.")
#             time.sleep(0.4)
#         except serial.SerialException as e:
#             self.get_logger().error(f'Serial write error: {e}')

# def main(args=None):
#     rclpy.init(args=args)
#     node = SerialBridgeNode()
#     try:
#         rclpy.spin(node)
#     except KeyboardInterrupt:
#         node.get_logger().info("Shutting down serial bridge.")
#     finally:
#         if node.arduino and node.arduino.is_open:
#             node.arduino.close()
#         node.destroy_node()
#         rclpy.shutdown()

# if __name__ == '__main__':
#     main()










# #!/usr/bin/env python3

# import rclpy
# from rclpy.node import Node
# from std_msgs.msg import Float64MultiArray
# import serial
# import time
# from rclpy.qos import QoSProfile, QoSReliabilityPolicy


# class SerialBridgeNode(Node):
#     def __init__(self):
#         super().__init__('serial_bridge_node')

#         self.declare_parameter('serial_port', '/dev/ttyACM0')
#         self.declare_parameter('baudrate', 57600)

#         self.arduino = None
#         self.setup_serial()

#         qos = QoSProfile(
#             reliability=QoSReliabilityPolicy.RELIABLE,
#             depth=10
#         )

#         self.joint_positions = [0.0] * 5
#         self.gripper_position = 0.0

#         self.create_subscription(
#             Float64MultiArray,
#             '/final_joint_positions',
#             self.final_positions_callback,
#             qos
#         )

#         self.create_subscription(
#             Float64MultiArray,
#             '/gripper_position',
#             self.gripper_position_callback,
#             qos
#         )

#         self.get_logger().info("Serial Bridge Node ready — sending dummy zero pose.")
#         self.send_dummy_zero_pose()

#     def setup_serial(self):
#         port = self.get_parameter('serial_port').get_parameter_value().string_value
#         baud = self.get_parameter('baudrate').get_parameter_value().integer_value
#         try:
#             self.arduino = serial.Serial(port, baud, timeout=1)
#             time.sleep(3)

#             self.get_logger().info("Waiting for Arduino to become READY...")
#             while True:
#                 line = self.arduino.readline().decode(errors='ignore').strip()
#                 if "READY" in line:
#                     break
#             self.get_logger().info("Arduino is READY.")
#             time.sleep(0.1)

#             self.get_logger().info(f'Connected to Arduino on {port} at {baud} baud.')

#         except (serial.SerialException, OSError) as e:
#             self.get_logger().error(f'Failed to connect to Arduino: {e}')

#     def send_dummy_zero_pose(self):
#         if not self.arduino or not self.arduino.is_open:
#             self.get_logger().error("Serial port not open")
#             return

#         zero_positions = [50, 68, 50, 50, 50, 0]  # 5 joints + gripper
#         command = f"D,{','.join(map(str, zero_positions))},AX\n"
#         self.get_logger().info(f"Sending dummy: {command.strip()}")
#         try:
#             self.arduino.write(command.encode())
#             self.arduino.flush()
#             time.sleep(0.5)
#         except serial.SerialException as e:
#             self.get_logger().error(f'Serial write error: {e}')

#     def final_positions_callback(self, msg):
#         if len(msg.data) != 5:
#             self.get_logger().error(f"Expected 5 joint positions, got {len(msg.data)}")
#             return

#         self.joint_positions = list(msg.data)
#         self.send_command_to_arduino()

#     def gripper_position_callback(self, msg):
#         if len(msg.data) != 1:
#             self.get_logger().warn(f"Expected single value for gripper, got {len(msg.data)}")
#             return
#         self.gripper_position = msg.data[0]

#     def send_command_to_arduino(self):
#         if not self.arduino or not self.arduino.is_open:
#             self.get_logger().error("Serial port not open")
#             return

#         joint_limits = [
#             {'lower': -1.57, 'upper': 1.57, 'reverse': True},   # joint 1
#             {'lower': -1.307, 'upper': 0.617, 'reverse': False}, # joint 2
#             {'lower': -1.57, 'upper': 1.57, 'reverse': True},   # joint 3
#             {'lower': -1.57, 'upper': 1.57, 'reverse': False},  # joint 4
#             {'lower': -1.57, 'upper': 1.57, 'reverse': False},  # joint 5 (will use joint 2 value)
#         ]

#         mapped_positions = []
#         for i in range(5):
#             lower = joint_limits[i]['lower']
#             upper = joint_limits[i]['upper']

#             if i == 4:
#                 val =  self.joint_positions[0]  # joint 5 takes joint 2 value
#             else:
#                 val = self.joint_positions[i]

#             val = max(min(val, upper), lower)
#             if joint_limits[i]['reverse']:
#                 val = -val
#             mapped_val = int((val - lower) * 100 / (upper - lower))
#             mapped_positions.append(mapped_val)

#         gripper_val = int(self.gripper_position)
#         mapped_positions.append(gripper_val)

#         command = f"D,{','.join(map(str, mapped_positions))},AX\n"
#         self.get_logger().info(f"Sending: {command.strip()}")

#         try:
#             self.arduino.write(command.encode())
#             self.arduino.flush()
#             time.sleep(0.4)
#             self.get_logger().info("Command sent to Arduino.")
#         except serial.SerialException as e:
#             self.get_logger().error(f'Serial write error: {e}')


# def main(args=None):
#     rclpy.init(args=args)
#     node = SerialBridgeNode()
#     try:
#         rclpy.spin(node)
#     except KeyboardInterrupt:
#         node.get_logger().info("Shutting down serial bridge.")
#     finally:
#         if node.arduino and node.arduino.is_open:
#             node.arduino.close()
#         node.destroy_node()
#         rclpy.shutdown()


# if __name__ == '__main__':
#     main()









# #!/usr/bin/env python3

# import rclpy
# from rclpy.node import Node
# from std_msgs.msg import Float64MultiArray, Float64
# import serial
# import time
# from rclpy.qos import QoSProfile, QoSReliabilityPolicy
# from sensor_msgs.msg import JointState

# class SerialBridgeNode(Node):
#     def __init__(self):
#         super().__init__('serial_bridge_node')

#         self.declare_parameter('serial_port', '/dev/ttyACM0')
#         self.declare_parameter('baudrate', 57600)

#         self.arduino = None
#         self.setup_serial()

#         qos = QoSProfile(
#             reliability=QoSReliabilityPolicy.RELIABLE,
#             depth=10
#         )

#         self.joint_positions = [0.0] * 5
#         self.gripper_position = 0.0

#         self.create_subscription(
#             JointState,
#             '/joint_states',
#             self.final_positions_callback,
#             qos
#         )

#         # Updated to subscribe to Float64 instead of Float64MultiArray
#         self.create_subscription(
#             Float64,
#             '/gripper_position',
#             self.gripper_position_callback,
#             qos
#         )

#         self.get_logger().info("Serial Bridge Node ready — sending dummy zero pose.")
#         self.send_dummy_zero_pose()

#     def setup_serial(self):
#         port = self.get_parameter('serial_port').get_parameter_value().string_value
#         baud = self.get_parameter('baudrate').get_parameter_value().integer_value
#         try:
#             self.arduino = serial.Serial(port, baud, timeout=1)
#             time.sleep(3)

#             self.get_logger().info("Waiting for Arduino to become READY...")
#             while True:
#                 line = self.arduino.readline().decode(errors='ignore').strip()
#                 if "READY" in line:
#                     break
#             self.get_logger().info("Arduino is READY.")
#             time.sleep(0.1)

#             self.get_logger().info(f'Connected to Arduino on {port} at {baud} baud.')

#         except (serial.SerialException, OSError) as e:
#             self.get_logger().error(f'Failed to connect to Arduino: {e}')

#     def send_dummy_zero_pose(self):
#         if not self.arduino or not self.arduino.is_open:
#             self.get_logger().error("Serial port not open")
#             return

#         zero_positions = [50, 68, 50, 50, 50, 0]  # 5 joints + gripper (50 = closed)
#         command = f"D,{','.join(map(str, zero_positions))},AX\n"
#         self.get_logger().info(f"Sending dummy: {command.strip()}")
#         try:
#             self.arduino.write(command.encode())
#             self.arduino.flush()
#             time.sleep(0.5)
#         except serial.SerialException as e:
#             self.get_logger().error(f'Serial write error: {e}')

#     def final_positions_callback(self, msg):
#         # Create a mapping of joint name -> position from the incoming message
#         joint_position_map = dict(zip(msg.name, msg.position))

#         # Extract positions for expected joints, or log an error if missing
#         joint_positions = []
#         for joint_name in self.expected_joints:
#             if joint_name not in joint_position_map:
#                 self.get_logger().error(f"Joint '{joint_name}' not found in /joint_states message.")
#                 return
#             joint_positions.append(joint_position_map[joint_name])

#         self.joint_positions = joint_positions
#         self.send_command_to_arduino()

#     def gripper_position_callback(self, msg):
#         # Map gripper values: 0 -> 50 (closed), 1 -> 0 (open)
#         if msg.data == 0.0:
#             self.gripper_position = 80  # Close gripper
#             self.get_logger().info("🔒 Gripper command: CLOSE (0 -> 50)")
#         elif msg.data == 1.0:
#             self.gripper_position = 0   # Open gripper
#             self.get_logger().info("🔓 Gripper command: OPEN (1 -> 0)")
#         else:
#             self.get_logger().warn(f"Unexpected gripper value: {msg.data}, using as-is")
#             self.gripper_position = int(msg.data)
        
#         # Send command immediately when gripper position changes
#         self.send_gripper_command()

#     def send_gripper_command(self):
#         """Send only gripper command without changing joint positions"""
#         if not self.arduino or not self.arduino.is_open:
#             self.get_logger().error("Serial port not open")
#             return

#         # Use current joint positions and new gripper position
#         joint_limits = [
#             {'lower': -1.57, 'upper': 1.57, 'reverse': True},   # joint 1
#             {'lower': -1.307, 'upper': 0.617, 'reverse': False}, # joint 2
#             {'lower': -1.57, 'upper': 1.57, 'reverse': True},   # joint 3
#             {'lower': -1.57, 'upper': 1.57, 'reverse': False},  # joint 4
#             {'lower': -1.57, 'upper': 1.57, 'reverse': False},  # joint 5 (will use joint 2 value)
#         ]

#         mapped_positions = []
#         for i in range(5):
#             lower = joint_limits[i]['lower']
#             upper = joint_limits[i]['upper']

          

#             val = max(min(val, upper), lower)
#             if joint_limits[i]['reverse']:
#                 val = -val
#             mapped_val = int((val - lower) * 100 / (upper - lower))
#             mapped_positions.append(mapped_val)

#         # Add mapped gripper position
#         mapped_positions.append(int(self.gripper_position))

#         command = f"D,{','.join(map(str, mapped_positions))},AX\n"
#         self.get_logger().info(f"Sending gripper command: {command.strip()}")

#         try:
#             self.arduino.write(command.encode())
#             self.arduino.flush()
#             time.sleep(0.4)
#             self.get_logger().info("Gripper command sent to Arduino.")
#         except serial.SerialException as e:
#             self.get_logger().error(f'Serial write error: {e}')

#     def send_command_to_arduino(self):
#         if not self.arduino or not self.arduino.is_open:
#             self.get_logger().error("Serial port not open")
#             return

#         joint_limits = [
#             {'lower': -1.57, 'upper': 1.57, 'reverse': True},   # joint 1
#             {'lower': -1.307, 'upper': 0.617, 'reverse': False}, # joint 2
#             {'lower': -1.57, 'upper': 1.57, 'reverse': True},   # joint 3
#             {'lower': -1.57, 'upper': 1.57, 'reverse': False},  # joint 4
#             {'lower': -1.57, 'upper': 1.57, 'reverse': False},  # joint 5 (will use joint 1 value)
#         ]

#         mapped_positions = []
#         for i in range(5):
#             lower = joint_limits[i]['lower']
#             upper = joint_limits[i]['upper']

#             if i == 4:
#                 val = self.joint_positions[0]  # joint 5 takes joint 1 value  
#             else:
#                 val = self.joint_positions[i]

#             val = max(min(val, upper), lower)
#             if joint_limits[i]['reverse']:
#                 val = -val
#             mapped_val = int((val - lower) * 100 / (upper - lower))
#             mapped_positions.append(mapped_val)

#         # Add current gripper position (already mapped)
#         mapped_positions.append(int(self.gripper_position))

#         command = f"D,{','.join(map(str, mapped_positions))},AX\n"
#         self.get_logger().info(f"Sending joint command: {command.strip()}")

#         try:
#             self.arduino.write(command.encode())
#             self.arduino.flush()
#             time.sleep(0.4)
#             self.get_logger().info("Joint command sent to Arduino.")
#         except serial.SerialException as e:
#             self.get_logger().error(f'Serial write error: {e}')


# def main(args=None):
#     rclpy.init(args=args)
#     node = SerialBridgeNode()
#     try:
#         rclpy.spin(node)
#     except KeyboardInterrupt:
#         node.get_logger().info("Shutting down serial bridge.")
#     finally:
#         if node.arduino and node.arduino.is_open:
#             node.arduino.close()
#         node.destroy_node()
#         rclpy.shutdown()


# if __name__ == '__main__':
#     main()













# #!/usr/bin/env python3

# import rclpy
# from rclpy.node import Node
# from trajectory_msgs.msg import JointTrajectory
# import serial
# import time
# from rclpy.qos import QoSProfile, QoSReliabilityPolicy


# class SerialNode(Node):
#     def __init__(self):
#         super().__init__('serial_node')

#         # Serial setup
#         self.arduino = None
#         self.setup_serial()

#         # QoS configuration
#         qos = QoSProfile(
#             reliability=QoSReliabilityPolicy.RELIABLE,
#             depth=10
#         )

#         # Subscribe to joint trajectory topic published by MoveIt/ros2_control
#         self.create_subscription(
#             JointTrajectory,
#             '/arm_controller/joint_trajectory',
#             self.trajectory_callback,
#             qos
#         )

#         self.get_logger().info("Serial node initialized and subscribed to /arm_controller/joint_trajectory")

#         # Joint limits and reversal flags
#         self.joint_limits_rad = [
#             {'name': 'joint_one', 'lower': -1.57, 'upper': 1.220, 'reverse': True},
#             {'name': 'joint_two', 'lower': -1.307, 'upper': 0.617, 'reverse': False},
#             {'name': 'joint_three', 'lower': -1.57, 'upper': 1.57, 'reverse': True},
#             {'name': 'joint_four', 'lower': -1.57, 'upper': 1.57, 'reverse': False},
#             {'name': 'joint_five', 'lower': -1.57, 'upper': 1.570, 'reverse': False},
#             {'name': 'joint_six', 'lower': -1.221, 'upper': 0.097, 'reverse': False}
#         ]

#     def setup_serial(self):
#         try:
#             self.arduino = serial.Serial('/dev/ttyACM0', 57600, timeout=1)
#             time.sleep(3)
#             self.arduino.write(b'DeskMod\n')
#             time.sleep(0.1)
#             self.get_logger().info('Connected to Arduino')
#         except (serial.SerialException, OSError) as e:
#             self.get_logger().error(f'Failed to connect to Arduino: {e}')

#     def trajectory_callback(self, msg):
#         """Callback when a new joint trajectory is published"""
#         self.get_logger().info(f"Received trajectory for joints: {msg.joint_names}")

#         # Take the first point (or loop over points if you want real-time streaming)
#         if not msg.points:
#             self.get_logger().warn("Received empty trajectory")
#             return

#         point = msg.points[0]  # You can process all points sequentially if needed
#         positions = point.positions

#         if len(positions) != 6:
#             self.get_logger().warn(f"Expected 6 positions, got {len(positions)}. Ignoring message.")
#             return

#         self.send_trajectory_to_arduino(positions)

#     def send_trajectory_to_arduino(self, positions):
#         if not self.arduino or not self.arduino.is_open:
#             self.get_logger().warn("Arduino connection not open, attempting reconnect")
#             self.setup_serial()
#             return False

#         def map_value(value_rad, lower_rad, upper_rad):
#             if value_rad > upper_rad or value_rad < lower_rad:
#                 self.get_logger().warn(f"Value {value_rad:.2f} rad out of bounds [{lower_rad:.2f}, {upper_rad:.2f}]")
#             value_rad = max(min(value_rad, upper_rad), lower_rad)
#             return int((value_rad - lower_rad) * 100 / (upper_rad - lower_rad))

#         mapped_values = []
#         for joint, val in zip(self.joint_limits_rad, positions):
#             if joint['reverse']:
#                 val = -val
#             mapped_values.append(map_value(val, joint['lower'], joint['upper']))

#         joint_commands = f"D,{','.join(str(v) for v in mapped_values)},AX\n"
#         self.get_logger().info(f"Sending command: {joint_commands.strip()}")

#         try:
#             self.arduino.write(joint_commands.encode())
#             self.arduino.flush()
#             return True
#         except serial.SerialException as e:
#             self.get_logger().error(f"Serial write error: {e}")
#             self.setup_serial()
#             return False


# def main(args=None):
#     rclpy.init(args=args)
#     node = SerialNode()
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












# #!/usr/bin/env python3

# import rclpy
# from rclpy.node import Node
# from control_msgs.action import FollowJointTrajectory
# from rclpy.action import ActionServer, GoalResponse, CancelResponse
# from trajectory_msgs.msg import JointTrajectoryPoint
# import serial
# import time
# from rclpy.qos import QoSProfile, QoSReliabilityPolicy


# class ArmSerialActionServer(Node):
#     def __init__(self):
#         super().__init__('arm_serial_action_server')

#         # Serial setup
#         self.arduino = None
#         self.setup_serial()

#         # Action server for /arm_controller/follow_joint_trajectory
#         self._action_server = ActionServer(
#             self,
#             FollowJointTrajectory,
#             '/arm_controller/follow_joint_trajectory',
#             execute_callback=self.execute_callback,
#             goal_callback=self.goal_callback,
#             cancel_callback=self.cancel_callback
#         )

#         self.get_logger().info("🚀 ArmSerialActionServer ready on /arm_controller/follow_joint_trajectory")

#     def setup_serial(self):
#         try:
#             self.arduino = serial.Serial('/dev/ttyACM0', 57600, timeout=1)
#             time.sleep(3)
#             self.arduino.write(b'DeskMod\n')
#             time.sleep(0.1)
#             self.get_logger().info("✅ Connected to Arduino")
#         except (serial.SerialException, OSError) as e:
#             self.get_logger().error(f'Failed to connect to Arduino: {e}')

#     def goal_callback(self, goal_request):
#         self.get_logger().info(f"Received new goal with {len(goal_request.trajectory.points)} points.")
#         return GoalResponse.ACCEPT

#     def cancel_callback(self, goal_handle):
#         self.get_logger().info("Received cancel request.")
#         return CancelResponse.ACCEPT

#     async def execute_callback(self, goal_handle):
#         self.get_logger().info("Executing trajectory goal...")

#         joint_names = goal_handle.request.trajectory.joint_names
#         points = goal_handle.request.trajectory.points

#         for point in points:
#             positions = point.positions

#             if len(positions) != 5:
#                 self.get_logger().warn(f"Expected 6 joint values, got {len(positions)} — skipping point")
#                 continue

#             self.send_trajectory_to_arduino(positions)

#             # Optional: publish feedback
#             feedback_msg = FollowJointTrajectory.Feedback()
#             feedback_msg.actual = JointTrajectoryPoint(positions=positions)
#             goal_handle.publish_feedback(feedback_msg)

#             # Simulate movement duration
#             await rclpy.sleep(0.5)  # sleep point-by-point (replace with actual duration if needed)

#         goal_handle.succeed()

#         result = FollowJointTrajectory.Result()
#         result.error_code = FollowJointTrajectory.Result.SUCCESSFUL
#         self.get_logger().info("✅ Trajectory execution completed.")
#         return result

#     def send_trajectory_to_arduino(self, positions):
#         if not self.arduino or not self.arduino.is_open:
#             self.get_logger().warn("Arduino not open, trying reconnect...")
#             self.setup_serial()
#             return False

#         # Map and reverse positions
#         joint_limits_rad = [
#             {'lower': -1.57, 'upper': 1.220, 'reverse': True},
#             {'lower': -1.307, 'upper': 0.617, 'reverse': False},
#             {'lower': -1.57, 'upper': 1.57, 'reverse': True},
#             {'lower': -1.57, 'upper': 1.57, 'reverse': False},
#             {'lower': -1.57, 'upper': 1.570, 'reverse': False},
#             # {'lower': -1.221, 'upper': 0.097, 'reverse': False}
#         ]

#         def map_value(value, lower, upper):
#             value = max(min(value, upper), lower)
#             return int((value - lower) * 100 / (upper - lower))

#         mapped_values = []
#         for joint, val in zip(joint_limits_rad, positions):
#             if joint['reverse']:
#                 val = -val
#             mapped_values.append(map_value(val, joint['lower'], joint['upper']))

#         command = f"D,{','.join(str(v) for v in mapped_values)},AX\n"
#         self.get_logger().info(f"Sending: {command.strip()}")
#         try:
#             self.arduino.write(command.encode())
#             self.arduino.flush()
#         except serial.SerialException as e:
#             self.get_logger().error(f"Serial write error: {e}")
#             self.setup_serial()

# def main(args=None):
#     rclpy.init(args=args)
#     node = ArmSerialActionServer()
#     try:
#         rclpy.spin(node)
#     except KeyboardInterrupt:
#         node.get_logger().info("Shutting down")
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

        # Connect to Arduino
        self.arduino = None
        self.setup_serial()

        # Joint limits
        self.joint_limits_rad = [
            {'name': 'joint_one', 'lower': -1.57, 'upper': 1.220, 'reverse': True},
            {'name': 'joint_two', 'lower': -1.307, 'upper': 0.617, 'reverse': False},
            {'name': 'joint_three', 'lower': -1.57, 'upper': 1.57, 'reverse': True},
            {'name': 'joint_four', 'lower': -1.57, 'upper': 1.57, 'reverse': False},
            {'name': 'joint_five', 'lower': -1.57, 'upper': 1.570, 'reverse': False},
        ]

        # Subscribe to /joint_states
        self.subscription = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_state_callback,
            10
        )

        self.get_logger().info("✅ ArmSerialBridge ready, subscribed to /joint_states")

    def setup_serial(self):
        try:
            self.arduino = serial.Serial('/dev/ttyACM0', 57600, timeout=1)
            time.sleep(3)
            self.arduino.write(b'DeskMod\n')
            time.sleep(0.1)
            self.get_logger().info("✅ Connected to Arduino")
        except (serial.SerialException, OSError) as e:
            self.get_logger().error(f'Failed to connect to Arduino: {e}')

    def joint_state_callback(self, msg):
        name_to_position = dict(zip(msg.name, msg.position))

        positions = []
        for joint in self.joint_limits_rad:
            joint_name = joint['name']
            if joint_name in name_to_position:
                val = name_to_position[joint_name]
                if joint['reverse']:
                    val = -val
                mapped = self.map_value(val, joint['lower'], joint['upper'])
                positions.append(mapped)
            else:
                positions.append(0)

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
