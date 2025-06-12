import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectoryPoint
from sensor_msgs.msg import JointState
import serial
import time
from rclpy.qos import QoSProfile, QoSReliabilityPolicy

class SerialNode(Node):
    def __init__(self):
        super().__init__('serial_node')
        
        # Serial setup
        self.arduino = None
        self.setup_serial()
        
        self.joint_order = [
            'rotating_base_joint',
            'shoulder_joint',
            'elbow_joint',
            'forearm_joint',
            'wrist_joint',
            'gripper_right_joint'
        ]
        
        # QoS configuration
        qos = QoSProfile(
            reliability=QoSReliabilityPolicy.RELIABLE,
            depth=10
        )
        
        # Subscribe to joint states
        self.subscription = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_state_callback,
            qos
        )
        self.get_logger().info("Serial node initialized")

    def setup_serial(self):
        try:
            self.arduino = serial.Serial('/dev/ttyACM0', 57600, timeout=1)
            time.sleep(3)  # Wait for Arduino reset
            self.arduino.write(b'DeskMod\n')  # Set Arduino to serial mode
            time.sleep(0.1)
            self.get_logger().info('Connected to Arduino')
        except (serial.SerialException, OSError) as e:
            self.get_logger().error(f'Failed to connect to Arduino: {e}')

    def joint_state_callback(self, msg):
        self.get_logger().info(f"Received joint state: names={msg.name}, positions={msg.position}")
        try:
            joint_positions = dict(zip(msg.name, msg.position))
            positions = []
            for name in self.joint_order:
                if name in joint_positions:
                    positions.append(joint_positions[name])
                else:
                    self.get_logger().warn(f"Joint {name} not found, using 0.0")
                    positions.append(0.0)

            #point = JointTrajectoryPoint()
            #point.positions = positions

            self.send_trajectory_to_arduino(positions)

        except KeyError as e:
            self.get_logger().error(f"Error mapping joints: {e}")


    def send_trajectory_to_arduino(self, positions):
        if not self.arduino or not self.arduino.is_open:
            self.get_logger().warn("Arduino connection not open, attempting reconnect")
            self.setup_serial()
            return False

        joint_limits_rad = [
            {'name': 'rotating_base_joint', 'lower': -1.57, 'upper': 1.220},
            {'name': 'shoulder_joint', 'lower': -1.308, 'upper': 0.610},
            {'name': 'elbow_joint', 'lower': -1.57, 'upper': 1.57},
            {'name': 'forearm_joint', 'lower': -1.57, 'upper': 1.57},
            {'name': 'wrist_joint', 'lower': -1.57, 'upper': 1.570},
            {'name': 'gripper_right_joint', 'lower': -1.221, 'upper': 0.097}  # Approx 20-95°
        ]

        def map_value(value_rad, lower_rad, upper_rad):
            if value_rad > upper_rad or value_rad < lower_rad:
                self.get_logger().warn(f"Value {value_rad} out of bounds [{lower_rad}, {upper_rad}]")
            value_rad = max(min(value_rad, upper_rad), lower_rad)
            return int((value_rad - lower_rad) * 100 / (upper_rad - lower_rad))

        mapped_values = []
        for joint, val in zip(joint_limits_rad, positions):
            mapped_values.append(map_value(val, joint['lower'], joint['upper']))

        joint_commands = f"D,{','.join(str(v) for v in mapped_values)},AX\n"
        
        self.get_logger().info(f"Sending command: {joint_commands}")
        self.get_logger().info(f"Mapped gripper value: {mapped_values[5]}")

        try:
            #self.arduino.reset_input_buffer()
            self.arduino.write(joint_commands.encode())
            self.get_logger().info(f"Sent: {joint_commands}")
            self.arduino.flush()
           
            return True  
        except serial.SerialException as e:
            self.get_logger().error(f"Serial write error: {e}")
            self.setup_serial()
            return False

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