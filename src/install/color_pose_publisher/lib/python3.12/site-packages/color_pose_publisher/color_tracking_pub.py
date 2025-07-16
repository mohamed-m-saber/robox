# import rclpy
# from rclpy.node import Node
# from cube_msgs.msg import ColorPoseStamped
# from geometry_msgs.msg import Pose
# import cv2
# from color_pose_publisher.calibration_utils import load_calibration, undistort_image
# from color_pose_publisher.vision_utils import find_workspace

# from color_pose_publisher.color_detection import detect_single_closest_cube

# from ament_index_python.packages import get_package_share_directory
# import os



# class ColorPosePublisher(Node):
#     def __init__(self):
#         super().__init__('color_pose_publisher')

#         # Publisher for pose + color messages
#         self.publisher_ = self.create_publisher(ColorPoseStamped, 'detected_color_pose', 10)

#         # Load camera calibration data
#         package_share_dir = get_package_share_directory('color_pose_publisher')
#         calibration_file = os.path.join(package_share_dir, 'assets', 'camera_calibration_data.npz')
#         self.camera_matrix, self.dist_coeffs = load_calibration(calibration_file)        # Open webcam
#         self.cap = cv2.VideoCapture(2)
#         if not self.cap.isOpened():
#             self.get_logger().error("❌ Could not open camera.")
#             rclpy.shutdown()

#         self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
#         self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

#         # Initialize detection data structures
#         self.detected_cubes = {'Red': [], 'Green': [], 'Blue': []}
#         self.pos_x, self.pos_y = [], []
#         self.color_track=1


#         self.detect_workspace()

#         # Run detection every 0.033s (~30 FPS)
#         self.create_timer(0.033, self.detect_and_process)


#     def detect_workspace(self):
#         """Capture frame and detect workspace region."""
#         ret, frame = self.cap.read()
#         if not ret:
#             self.get_logger().error("❌ Failed to read frame for workspace detection.")
#             rclpy.shutdown()

#         undistorted, _, _ = undistort_image(frame, self.camera_matrix, self.dist_coeffs)
#         ws_data = find_workspace(undistorted)

#         if ws_data:
#             self.workspace_data = ws_data
#             self.get_logger().info("✅ Workspace detected successfully.")
#         else:
#             self.get_logger().error("❌ Could not find workspace at startup.")
#             rclpy.shutdown()




#     def detect_and_process(self):
#         """Capture frame, detect cube in workspace, and send goal if available."""
      

#         ret, frame = self.cap.read()
#         if not ret:
#             self.get_logger().warning("❌ Failed to read frame.")
#             return

#         undistorted, _, _ = undistort_image(frame, self.camera_matrix, self.dist_coeffs)

#         if self.workspace_data:
#             x, y, w, h, px_per_mm = self.workspace_data
#             roi = undistorted[y:y + h, x:x + w]

#             result = detect_single_closest_cube(roi, px_per_mm, x, y)

#             if result :
#                 x_mm, y_mm, theta_deg, color = result
#                 if color=='Blue' and self.color_track==1:
                    
#                     self.publish_pose(x_mm, y_mm, theta_deg, color)
                

#         # Show detection image
#         cv2.imshow("Detection Output", undistorted)

#         key = cv2.waitKey(1) & 0xFF
#         if key == ord('q'):
#             self.shutdown()
#         elif key == ord('r'):
#             self.get_logger().info("🔄 Recalibrating workspace...")
#             self.detect_workspace()

#     def publish_pose(self, x_mm, y_mm, theta_deg, color):
#         """Publish a detected cube position and color."""
#         msg = ColorPoseStamped()
#         msg.header.stamp = self.get_clock().now().to_msg()
#         msg.header.frame_id = "world"
      
#         msg.pose.position.x = round((y_mm) / 1000.0 ,5) # convert mm to meters,    x,y of the robot are reversed 
#         msg.pose.position.y = round((x_mm) / 1000.0,5)
#         msg.pose.position.z = 0.0
#         msg.pose.orientation.x = 0.0
#         msg.pose.orientation.y = 0.0
#         msg.pose.orientation.z = 0.0
#         msg.pose.orientation.w = 1.0

#         msg.color = color

#         self.publisher_.publish(msg)
#         self.get_logger().info(f"📤 Published {color} cube at X={x_mm:.1f}mm Y={y_mm:.1f}mm")

# def main(args=None):
#     rclpy.init(args=args)
#     node = ColorPosePublisher()
#     rclpy.spin(node)

# if __name__ == '__main__':
#     main()




















import rclpy
from rclpy.node import Node
from cube_msgs.msg import ColorPoseStamped
from geometry_msgs.msg import Pose
import cv2
from color_pose_publisher.calibration_utils import load_calibration, undistort_image
from color_pose_publisher.vision_utils import find_workspace
from color_pose_publisher.color_detection import detect_single_closest_cube
from ament_index_python.packages import get_package_share_directory
import os


class ColorPosePublisher(Node):
    def __init__(self):
        super().__init__('color_pose_publisher')

        # Publisher for pose + color messages
        self.publisher_ = self.create_publisher(ColorPoseStamped, 'detected_color_pose', 10)

        # Load camera calibration data
        package_share_dir = get_package_share_directory('color_pose_publisher')
        calibration_file = os.path.join(package_share_dir, 'assets', 'camera_calibration_data.npz')
        self.camera_matrix, self.dist_coeffs = load_calibration(calibration_file)

        # Open webcam
        self.cap = cv2.VideoCapture(2)
        if not self.cap.isOpened():
            self.get_logger().error("❌ Could not open camera.")
            rclpy.shutdown()

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        # Color tracking configuration
        self.color_track = 1  # Track blue only (as per your earlier logic)
        self.tracking_blue = False  # Flag to know if we're already tracking a blue cube

        self.detect_workspace()

        # Run detection every 0.033s (~30 FPS)
        self.create_timer(0.033, self.detect_and_process)

    def detect_workspace(self):
        """Capture frame and detect workspace region."""
        ret, frame = self.cap.read()
        if not ret:
            self.get_logger().error("❌ Failed to read frame for workspace detection.")
            rclpy.shutdown()

        undistorted, _, _ = undistort_image(frame, self.camera_matrix, self.dist_coeffs)
        ws_data = find_workspace(undistorted)

        if ws_data:
            self.workspace_data = ws_data
            self.get_logger().info("✅ Workspace detected successfully.")
        else:
            self.get_logger().error("❌ Could not find workspace at startup.")
            rclpy.shutdown()

    def detect_and_process(self):
        """Capture frame, detect cube in workspace, and track its pose."""
        ret, frame = self.cap.read()
        if not ret:
            self.get_logger().warning("❌ Failed to read frame.")
            return

        undistorted, _, _ = undistort_image(frame, self.camera_matrix, self.dist_coeffs)

        if self.workspace_data:
            x, y, w, h, px_per_mm = self.workspace_data
            roi = undistorted[y:y + h, x:x + w]

            result = detect_single_closest_cube(roi, px_per_mm, x, y)

            if result:
                x_mm, y_mm, theta_deg, color = result

                if color == 'Blue' and self.color_track == 1:
                    if not self.tracking_blue:
                        # First blue cube detected — start tracking
                        self.tracking_blue = True
                        self.get_logger().info("🎯 Started tracking blue cube.")
                    
                    # Continue tracking the same cube
                    if self.tracking_blue:
                        self.publish_pose(x_mm, y_mm, theta_deg, color)

            else:
                # No blue cube found
                if self.tracking_blue:
                    self.get_logger().info("❌ Lost blue cube — stopped tracking.")
                    self.tracking_blue = False

        # Show detection image
        cv2.imshow("Detection Output", undistorted)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            self.shutdown()
        elif key == ord('r'):
            self.get_logger().info("🔄 Recalibrating workspace...")
            self.detect_workspace()
        elif key == ord('c'):
            self.get_logger().info("🔄 Resetting blue cube tracking.")
            self.tracking_blue = False

    def publish_pose(self, x_mm, y_mm, theta_deg, color):
        """Publish a detected cube position and color."""
        msg = ColorPoseStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "world"

        # Convert mm to meters and swap x/y axes to match robot world
        msg.pose.position.x = round(y_mm / 1000.0, 5)
        msg.pose.position.y = round(x_mm / 1000.0, 5)
        msg.pose.position.z = 0.0

        msg.pose.orientation.x = 0.0
        msg.pose.orientation.y = 0.0
        msg.pose.orientation.z = 0.0
        msg.pose.orientation.w = 1.0

        msg.color = color

        self.publisher_.publish(msg)
        self.get_logger().info(f"📤 Published {color} cube at X={x_mm:.1f}mm Y={y_mm:.1f}mm")

    def shutdown(self):
        """Graceful shutdown."""
        self.cap.release()
        cv2.destroyAllWindows()
        rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)
    node = ColorPosePublisher()
    rclpy.spin(node)


if __name__ == '__main__':
    main()
