#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose
from arm_description.srv import GoToPose
import math

class InteractiveGoToPoseClient(Node):

    def __init__(self):
        super().__init__('interactive_go_to_pose_client')
        self.client = self.create_client(GoToPose, 'GoToPose')
        
        # Wait for service to be available
        print("🔍 Waiting for GoToPose service...")
        while not self.client.wait_for_service(timeout_sec=1.0):
            print("   Service not available, waiting...")
        
        print("✅ GoToPose service is available!")
        
        # Define safe predefined poses (adjust these based on your robot's workspace)
        self.safe_poses = {
            'home': (0.0, 0.0, 0.3, 0.0, 0.0, 0.0, 1.0),
            'ready': (0.3, 0.0, 0.3, 0.0, 0.0, 0.0, 1.0),
            'forward': (0.4, 0.0, 0.3, 0.0, 0.0, 0.0, 1.0),
            'left': (0.3, 0.2, 0.3, 0.0, 0.0, 0.0, 1.0),
            'right': (0.3, -0.2, 0.3, 0.0, 0.0, 0.0, 1.0),
            'up': (0.3, 0.0, 0.5, 0.0, 0.0, 0.0, 1.0),
            'down': (0.3, 0.0, 0.2, 0.0, 0.0, 0.0, 1.0),
            'center': (0.2, 0.0, 0.4, 0.0, 0.0, 0.0, 1.0),
        }

    def normalize_quaternion(self, qx, qy, qz, qw):
        """Normalize quaternion to unit length"""
        norm = math.sqrt(qx*qx + qy*qy + qz*qz + qw*qw)
        if norm == 0:
            return 0.0, 0.0, 0.0, 1.0
        return qx/norm, qy/norm, qz/norm, qw/norm

    def send_pose(self, x, y, z, qx=0.0, qy=0.0, qz=0.0, qw=1.0):
        """Send a pose to the GoToPose service"""
        # Normalize quaternion
        qx, qy, qz, qw = self.normalize_quaternion(qx, qy, qz, qw)
        
        request = GoToPose.Request()
        
        request.target_pose = Pose()
        request.target_pose.position.x = float(x)
        request.target_pose.position.y = float(y)
        request.target_pose.position.z = float(z)
        request.target_pose.orientation.x = float(qx)
        request.target_pose.orientation.y = float(qy)
        request.target_pose.orientation.z = float(qz)
        request.target_pose.orientation.w = float(qw)
        
        print(f"🎯 Sending pose:")
        print(f"   Position: ({x:.3f}, {y:.3f}, {z:.3f})")
        print(f"   Orientation: ({qx:.3f}, {qy:.3f}, {qz:.3f}, {qw:.3f})")
        
        # Basic safety check
        distance = math.sqrt(x*x + y*y + z*z)
        if distance > 1.0:  # Adjust based on your robot's reach
            print(f"⚠️  Warning: Target distance ({distance:.3f}m) may be out of reach")
        
        if z < 0.1:  # Assuming robot can't go too low
            print(f"⚠️  Warning: Target height ({z:.3f}m) may be too low")
        
        future = self.client.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        
        try:
            response = future.result()
            if response.success:
                print(f"✅ {response.message}")
            else:
                print(f"❌ {response.message}")
                print("💡 Try using a predefined safe pose (type 'safe' to see list)")
            return response.success
        except Exception as e:
            print(f"❌ Service call failed: {str(e)}")
            return False

    def send_predefined_pose(self, pose_name):
        """Send a predefined safe pose"""
        if pose_name in self.safe_poses:
            x, y, z, qx, qy, qz, qw = self.safe_poses[pose_name]
            print(f"🎯 Using predefined pose '{pose_name}'")
            return self.send_pose(x, y, z, qx, qy, qz, qw)
        else:
            print(f"❌ Unknown predefined pose: {pose_name}")
            return False

    def run_interactive_mode(self):
        """Run interactive mode for pose input"""
        print("\n🤖 Enhanced Interactive GoToPose Client")
        print("=" * 50)
        print("Enter pose coordinates or use predefined commands:")
        print("  • Type 'quit' or 'exit' to stop")
        print("  • Type 'safe' to see safe predefined poses")
        print("  • Type 'help' for more commands")
        print("  • Enter: x y z (e.g., 0.3 0.0 0.4)")
        print("  • Enter: x y z qx qy qz qw (for full pose)")
        print("-" * 50)
        
        while True:
            try:
                user_input = input("\n🎮 Enter pose > ").strip().lower()
                
                if user_input in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                elif user_input == 'help':
                    self.show_help()
                
                elif user_input == 'safe':
                    self.show_safe_poses()
                
                elif user_input in self.safe_poses:
                    self.send_predefined_pose(user_input)
                
                # Legacy predefined poses (keeping for compatibility)
                elif user_input == 'home':
                    self.send_pose(0.0, 0.0, 0.5)
                
                elif user_input == 'forward':
                    self.send_pose(0.4, 0.0, 0.3)
                
                elif user_input == 'left':
                    self.send_pose(0.2, 0.3, 0.4)
                
                elif user_input == 'right':
                    self.send_pose(0.2, -0.3, 0.4)
                
                elif user_input == 'up':
                    self.send_pose(0.2, 0.0, 0.6)
                
                elif user_input == 'down':
                    self.send_pose(0.2, 0.0, 0.2)
                
                else:
                    # Parse coordinates
                    coords = user_input.split()
                    
                    if len(coords) == 3:
                        x, y, z = map(float, coords)
                        self.send_pose(x, y, z)
                    
                    elif len(coords) == 7:
                        x, y, z, qx, qy, qz, qw = map(float, coords)
                        self.send_pose(x, y, z, qx, qy, qz, qw)
                    
                    else:
                        print("❌ Invalid input. Use 'help' for usage information.")
                        
            except ValueError:
                print("❌ Invalid numbers. Please enter valid coordinates.")
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except EOFError:
                print("\n👋 Goodbye!")
                break

    def show_safe_poses(self):
        """Show predefined safe poses"""
        print("\n🛡️  Safe Predefined Poses:")
        for name, (x, y, z, qx, qy, qz, qw) in self.safe_poses.items():
            print(f"    {name:8} - Position: ({x:5.2f}, {y:5.2f}, {z:5.2f})")
        print("\n💡 Type any pose name to use it (e.g., 'ready', 'center')")

    def show_help(self):
        """Show help information"""
        print("\n📖 Available Commands:")
        print("  Safe predefined poses (type 'safe' to see list):")
        for name in self.safe_poses.keys():
            print(f"    {name}")
        
        print("\n  Legacy poses:")
        print("    home    - Move to home position (0.0, 0.0, 0.5)")
        print("    forward - Move forward (0.4, 0.0, 0.3)")
        print("    left    - Move left (0.2, 0.3, 0.4)")
        print("    right   - Move right (0.2, -0.3, 0.4)")
        print("    up      - Move up (0.2, 0.0, 0.6)")
        print("    down    - Move down (0.2, 0.0, 0.2)")
        
        print("\n  Custom poses:")
        print("    x y z           - Position only (orientation = no rotation)")
        print("    x y z qx qy qz qw - Full pose with orientation")
        
        print("\n  Control:")
        print("    help, safe, quit, exit")
        
        print("\n💡 Tips:")
        print("  - Start with safe predefined poses")
        print("  - Keep positions within robot's reach (~1.0m)")
        print("  - Keep z-values above 0.1m")

def main(args=None):
    rclpy.init(args=args)
    
    client = InteractiveGoToPoseClient()
    
    try:
        client.run_interactive_mode()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    
    client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()