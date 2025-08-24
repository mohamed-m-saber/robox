import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy, JointState
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

        # Initialize joint positions to zero
        self.joint_positions = [0.0] * 6
        self.speed=0.0
        
        # Joint names for publishing to RViz - UPDATE THESE TO MATCH YOUR URDF
        self.joint_names = ['joint_one', 'joint_two', 'joint_three', 
                           'joint_four', 'joint_five', 'joint_six']
        
        # Alternative common joint names (uncomment if needed):
        # self.joint_names = ['joint_1', 'joint_2', 'joint_3', 'joint_4', 'joint_5', 'joint_6']
        # self.joint_names = ['base_joint', 'shoulder_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']

        # Flag to control whether to use feedback from joint_states
        self.use_joint_feedback = False
        
        # Last command time to detect when joystick is active
        self.last_command_time = time.time()

        # Subscribe to joystick topic
        self.create_subscription(Joy, 'joy', self.joy_callback, 10)

        # Subscribe to robot joint states feedback (separate topic to avoid conflicts)
        self.create_subscription(JointState, 'robot_joint_states', self.robot_joint_state_callback, 10)
        
        # Publisher for joint states (for RViz visualization)
        self.joint_state_publisher = self.create_publisher(JointState, 'joint_states', 10)
        
        # Timer for regular joint state publishing
        self.create_timer(0.05, self.publish_joint_states)  # 20 Hz for smooth visualization

    def joy_callback(self, msg):
        self.last_command_time = time.time()
        


        # Get incremental changes from joystick

        speed=self.get_speed(msg.buttons[10], msg.buttons[11])


        delta_j1 = self.get_joint_from_buttons(msg.buttons[1], msg.buttons[3],speed)
        delta_j2 = self.get_joint_from_buttons(msg.buttons[0], msg.buttons[4],speed)
        delta_j3 = self.get_joint_from_buttons(msg.buttons[8], msg.buttons[9],speed)
        delta_j4 = self.axis_to_command(msg.axes[7],speed)
        delta_j5 = self.axis_to_command(msg.axes[6],speed)
        delta_j6 = self.get_joint_from_buttons(msg.buttons[6], msg.buttons[7],speed)
        # Apply incremental changes to current positions
        new_positions = [
            self.joint_positions[0] + delta_j1,
            self.joint_positions[1] + delta_j2,
            self.joint_positions[2] + delta_j3,
            self.joint_positions[3] + delta_j4,
            self.joint_positions[4] + delta_j5,
            self.joint_positions[5] + delta_j6
        ]

        # Apply joint limits
        joint_limits = [
            {'lower': -1.57, 'upper': 1.57},  # joint_one
            {'lower': -1.307, 'upper': 0.617},  # joint_two
            {'lower': -1.57, 'upper': 1.57},  # joint_three
            {'lower': -1.57, 'upper': 1.57},  # joint_four
            {'lower': -1.57, 'upper': 1.57},  # joint_five
            {'lower': -1.57, 'upper': 1.57},  # joint_six
        ]
        
        # Clamp positions to joint limits
        for i, (pos, limits) in enumerate(zip(new_positions, joint_limits)):
            new_positions[i] = max(limits['lower'], min(limits['upper'], pos))

        # Update internal joint positions
        self.joint_positions = new_positions

        # Send to Arduino
        joint_map = {
            'joint_one': self.joint_positions[0], 
            'joint_two': self.joint_positions[1], 
            'joint_three': self.joint_positions[2],
            'joint_four': self.joint_positions[3], 
            'joint_five': self.joint_positions[4], 
            'joint_six': self.joint_positions[5]
        }
        
        self.send_to_arduino(joint_map)
        
        # Log the command for debugging
        self.get_logger().info(f'🎮 Joystick command: {[f"{pos:.3f}" for pos in self.joint_positions]}')

    def robot_joint_state_callback(self, msg):
        """Handle joint state feedback from the actual robot (optional)"""
        # Only use robot feedback if we haven't received joystick commands recently
        time_since_last_command = time.time() - self.last_command_time
        
        if self.use_joint_feedback and time_since_last_command > 1.0:  # 1 second timeout
            if len(msg.position) >= 6:
                self.joint_positions = list(msg.position[:6])
                self.get_logger().info(f"🤖 Using robot feedback: {[f'{pos:.3f}' for pos in self.joint_positions]}")

    def publish_joint_states(self):
        """Publish current joint positions to RViz"""
        joint_state_msg = JointState()
        joint_state_msg.header.stamp = self.get_clock().now().to_msg()
        joint_state_msg.header.frame_id = 'base_link'  # Use your robot's base frame
        joint_state_msg.name = self.joint_names
        joint_state_msg.position = self.joint_positions
        joint_state_msg.velocity = [0.0] * 6  # No velocity info
        joint_state_msg.effort = [0.0] * 6    # No effort info
        
        self.joint_state_publisher.publish(joint_state_msg)


    def get_speed(self,forward,backward):
        if forward == 1 and backward == 0:
            if self.speed<0.1:
                self.speed+=0.01
        elif backward == 1 and forward == 0:
            if self.speed>0.0:
                self.speed-=0.01
        return self.speed    
      
    def get_joint_from_buttons(self, backward, forward,speed):
        """Returns 0.01 for forward, -0.01 for backward, 0 for stop"""
        if forward == 1 and backward == 0:
            return  speed
        elif backward == 1 and forward == 0:
            return -speed
        else:
            return 0.0

    def axis_to_command(self, val,speed):
        """Converts analog axis to incremental command"""
        if val ==1:
            return speed
        elif val ==-1:
            return -speed
        else:
            return 0.0

    def send_to_arduino(self, joint_map):
        if not self.arduino or not self.arduino.is_open:
            self.get_logger().warn('⚠️ Arduino not connected, skipping send.')
            return

        joint_limits = [
            {'name': 'joint_one', 'lower': -1.57, 'upper': 1.57, 'reverse': True},
            {'name': 'joint_two', 'lower': -1.307, 'upper': 0.617, 'reverse': False},
            {'name': 'joint_three', 'lower': -1.57, 'upper': 1.57, 'reverse': True},
            {'name': 'joint_four', 'lower': -1.57, 'upper': 1.57, 'reverse': False},
            {'name': 'joint_five', 'lower': -1.57, 'upper': 1.57, 'reverse': False},
            {'name': 'joint_six', 'lower': -1.57, 'upper': 1.57, 'reverse': False},
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