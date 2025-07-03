import rclpy
from rclpy.node import Node
from cube_msgs.msg import ColorPoseStamped
from geometry_msgs.msg import Pose
import cv2
from color_pose_publisher.calibration_utils import load_calibration, undistort_image
from color_pose_publisher.color_detection import detect_and_log_cubes
from color_pose_publisher.vision_utils import find_workspace
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
        self.camera_matrix, self.dist_coeffs = load_calibration(calibration_file)        # Open webcam
        self.cap = cv2.VideoCapture(2)
        if not self.cap.isOpened():
            self.get_logger().error("❌ Could not open camera.")
            rclpy.shutdown()

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        # Initialize detection data structures
        self.detected_cubes = {'Red': [], 'Green': [], 'Blue': []}
        self.pos_x, self.pos_y = [], []

        # Run detection every 0.033s (~30 FPS)
        self.create_timer(0.033, self.detect_and_publish)

    def detect_and_publish(self):
        ret, frame = self.cap.read()
        if not ret:
            self.get_logger().warning("❌ Failed to read frame.")
            return

        undistorted, _, _ = undistort_image(frame, self.camera_matrix, self.dist_coeffs)

        workspace_data = find_workspace(undistorted)
        if workspace_data:
            x, y, w, h, px_per_mm = workspace_data
            roi = undistorted[y:y + h, x:x + w]

            # Process ROI, detect cubes and publish new detections
            processed = detect_and_log_cubes(
                roi, px_per_mm, x, y, self.detected_cubes, self.pos_x, self.pos_y, self.publish_pose
            )

            undistorted[y:y + h, x:x + w] = processed

        cv2.imshow("Detection Output", undistorted)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.cap.release()
            cv2.destroyAllWindows()
            self.get_logger().info("✅ Program ended.")
            rclpy.shutdown()

    def publish_pose(self, x_mm, y_mm, theta_deg, color):
        """Publish a detected cube position and color."""
        msg = ColorPoseStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "world"
      
        msg.pose.position.x = round((y_mm) / 1000.0 ,5) # convert mm to meters,    x,y of the robot are reversed 
        msg.pose.position.y = round((x_mm) / 1000.0,5)
        msg.pose.position.z = 0.0
        msg.pose.orientation.x = 0.0
        msg.pose.orientation.y = 0.0
        msg.pose.orientation.z = 0.0
        msg.pose.orientation.w = 1.0

        msg.color = color

        self.publisher_.publish(msg)
        self.get_logger().info(f"📤 Published {color} cube at X={x_mm:.1f}mm Y={y_mm:.1f}mm")

def main(args=None):
    rclpy.init(args=args)
    node = ColorPosePublisher()
    rclpy.spin(node)

if __name__ == '__main__':
    main()
