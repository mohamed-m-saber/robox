#rclpy is a python API for communication and interacting with ROS2 
#API stands for the Applicaion Programming Interface
#It is an interface between two programs
# import rclpy

# from std_msgs.msg import String

# from rclpy.node import Node


# class PublisherNode(Node):
#     def __init__(self):
#         super().__init__('publisher_node')
#         self.Publisher_=self.create_publisher(String,'communication_topic',15)

#         commRate=1.0    #i message per second
#         self.timer=self.create_timer(commRate,self.callBackFunction)
#         self.counter=0


#     def callBackFunction(self):
#         messagePublisher=String()
#         messagePublisher.data=f"Counter value: {self.counter}"
#         self.Publisher_.publish(messagePublisher)
#         self.get_logger().info(f"Publisher node is publishing:{messagePublisher.data}")
#         self.counter=self.counter+1


# def main():
#     rclpy.init()
#     node_publisher=PublisherNode()
#     rclpy.spin(node_publisher)
#     node_publisher.destroy_node()
#     rclpy.shutdown()


# if __name__ == '__main__':
#     main()

#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration
import math

class JointOffsetCalibrator(Node):
    def __init__(self):
        super().__init__('joint_offset_calibrator')
        
        # Subscriber for joint states
        self.joint_sub = self.create_subscription(
            JointState, '/joint_states', self.joint_callback, 10)
        
        # Publisher for joint commands
        self.traj_pub = self.create_publisher(
            JointTrajectory, '/joint_trajectory_controller/joint_trajectory', 10)
        
        self.current_joints = {}
        self.joint_offsets = {}
        
        # Your robot's joint names
        self.joint_names = [
            'rotating_base_joint',
            'shoulder_joint', 
            'elbow_joint',
            'forearm_joint',
            'wrist_joint'
        ]
        
        self.get_logger().info("Joint Offset Calibrator started")
        
    def joint_callback(self, msg):
        self.current_joints = dict(zip(msg.name, msg.position))
    
    def move_joint_to_position(self, joint_name, angle_degrees, duration=3.0):
        """Move a single joint to specified angle"""
        msg = JointTrajectory()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.joint_names = [joint_name]
        
        point = JointTrajectoryPoint()
        point.positions = [math.radians(angle_degrees)]
        point.time_from_start = Duration(sec=int(duration), nanosec=int((duration % 1) * 1e9))
        
        msg.points = [point]
        self.publisher.publish(msg)
        
    def calibrate_joint_zero(self, joint_name):
        """Find the zero position offset for a joint"""
        print(f"\n=== Calibrating {joint_name} ===")
        print("1. Manually move the robot's physical joint to its TRUE ZERO position")
        print("   (usually the position where the joint is at 0° mechanically)")
        print("2. Press Enter when the joint is at TRUE ZERO...")
        input()
        
        # Wait for joint state update
        rclpy.spin_once(self, timeout_sec=1.0)
        
        if joint_name in self.current_joints:
            hardware_zero = self.current_joints[joint_name]
            offset = -hardware_zero  # Offset needed to make this position read as 0
            self.joint_offsets[joint_name] = offset
            
            print(f"Hardware reads: {math.degrees(hardware_zero):.2f}° ({hardware_zero:.4f} rad)")
            print(f"Required offset: {math.degrees(offset):.2f}° ({offset:.4f} rad)")
            return offset
        else:
            print(f"ERROR: Joint {joint_name} not found in joint_states")
            return None
    
    def calibrate_joint_range(self, joint_name):
        """Calibrate the full range of a joint"""
        print(f"\n=== Range Calibration for {joint_name} ===")
        
        # Test minimum position
        print("Move joint to its MINIMUM physical limit")
        input("Press Enter when at minimum position...")
        rclpy.spin_once(self, timeout_sec=1.0)
        min_hw = self.current_joints.get(joint_name, 0)
        
        # Test maximum position  
        print("Move joint to its MAXIMUM physical limit")
        input("Press Enter when at maximum position...")
        rclpy.spin_once(self, timeout_sec=1.0)
        max_hw = self.current_joints.get(joint_name, 0)
        
        print(f"Hardware range: {math.degrees(min_hw):.1f}° to {math.degrees(max_hw):.1f}°")
        print(f"Hardware range: {min_hw:.3f} to {max_hw:.3f} rad")
        
        return min_hw, max_hw
    
    def test_calibration(self, joint_name, test_angles=[0, 45, 90, 135, 180]):
        """Test the calibration by commanding specific angles"""
        if joint_name not in self.joint_offsets:
            print(f"No offset calibrated for {joint_name}")
            return
            
        offset = self.joint_offsets[joint_name]
        print(f"\n=== Testing {joint_name} with offset {math.degrees(offset):.2f}° ===")
        
        for angle in test_angles:
            commanded_angle = math.radians(angle) + offset
            print(f"Commanding {angle}° (actual command: {math.degrees(commanded_angle):.2f}°)")
            
            # Send command
            msg = JointTrajectory()
            msg.header.stamp = self.get_clock().now().to_msg()
            msg.joint_names = [joint_name]
            
            point = JointTrajectoryPoint()
            point.positions = [commanded_angle]
            point.time_from_start = Duration(sec=2, nanosec=0)
            msg.points = [point]
            
            self.traj_pub.publish(msg)
            
            input(f"Press Enter to continue to next angle...")
    
    def generate_offset_config(self):
        """Generate the configuration file with offsets"""
        print("\n" + "="*50)
        print("CALIBRATION RESULTS")
        print("="*50)
        
        print("\nAdd these offsets to your controller configuration:")
        print("\n# In your ros2_controllers.yaml file:")
        print("joint_trajectory_controller:")
        print("  ros__parameters:")
        print("    joints:")
        for joint in self.joint_names:
            print(f"      - {joint}")
        
        print("\n    # Joint offsets (add these):")
        for joint, offset in self.joint_offsets.items():
            print(f"    {joint}:")
            print(f"      offset: {offset:.6f}  # {math.degrees(offset):.2f} degrees")
        
        print("\n" + "="*50)

def main():
    rclpy.init()
    calibrator = JointOffsetCalibrator()
    
    print("="*60)
    print("JOINT OFFSET CALIBRATION TOOL")
    print("="*60)
    print("\nThis tool will help you find the offset between your")
    print("URDF's zero positions and your hardware's zero positions.")
    print("\nMake sure your robot is powered and you can move it manually!")
    
    try:
        while True:
            print("\n" + "-"*40)
            print("OPTIONS:")
            print("1. Calibrate individual joint zero position")
            print("2. Calibrate joint range")
            print("3. Test calibrated joint")
            print("4. Generate configuration file")
            print("5. Exit")
            
            choice = input("\nEnter choice (1-5): ").strip()
            
            if choice == '1':
                print("\nAvailable joints:")
                for i, joint in enumerate(calibrator.joint_names):
                    print(f"  {i+1}. {joint}")
                joint_idx = int(input("Select joint number: ")) - 1
                if 0 <= joint_idx < len(calibrator.joint_names):
                    calibrator.calibrate_joint_zero(calibrator.joint_names[joint_idx])
                    
            elif choice == '2':
                print("\nAvailable joints:")
                for i, joint in enumerate(calibrator.joint_names):
                    print(f"  {i+1}. {joint}")
                joint_idx = int(input("Select joint number: ")) - 1
                if 0 <= joint_idx < len(calibrator.joint_names):
                    calibrator.calibrate_joint_range(calibrator.joint_names[joint_idx])
                    
            elif choice == '3':
                print("\nCalibrated joints:")
                calibrated = [j for j in calibrator.joint_names if j in calibrator.joint_offsets]
                for i, joint in enumerate(calibrated):
                    print(f"  {i+1}. {joint}")
                if calibrated:
                    joint_idx = int(input("Select joint number: ")) - 1
                    if 0 <= joint_idx < len(calibrated):
                        calibrator.test_calibration(calibrated[joint_idx])
                        
            elif choice == '4':
                calibrator.generate_offset_config()
                
            elif choice == '5':
                break
                
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Error: {e}")
    finally:
        calibrator.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()