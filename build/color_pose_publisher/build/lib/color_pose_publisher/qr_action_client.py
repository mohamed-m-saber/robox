import os
import cv2
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from ament_index_python.packages import get_package_share_directory

from cube_msgs.action import PickAndPlace
from geometry_msgs.msg import Pose


from sensor_msgs.msg import Image
from cv_bridge import CvBridge

from color_pose_publisher.calibration_utils import load_calibration, undistort_image
from color_pose_publisher.QR_code_detection import detect_single_closest_qr

from color_pose_publisher.vision_utils import find_workspace


class ColorPoseClient(Node):
    def __init__(self):
        super().__init__('qr_pose_client')

        # Action client for pick and place service
        self._action_client = ActionClient(self, PickAndPlace, 'pick_and_place')

        # Load camera calibration parameters
        package_dir = get_package_share_directory('color_pose_publisher')
        calibration_file = os.path.join(package_dir, 'assets', 'camera_calibration_data.npz')
        self.camera_matrix, self.dist_coeffs = load_calibration(calibration_file)

        # Initialize camera
        self.cap = cv2.VideoCapture(2)
        if not self.cap.isOpened():
            self.get_logger().error("❌ Could not open camera.")
            rclpy.shutdown()

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


        self.image_pub = self.create_publisher(Image, 'detection_feed', 10)
        self.bridge = CvBridge()

        # State variable: whether robot is busy with a goal
        self.busy = False

        # Run detection loop at ~30 FPS
        self.create_timer(0.033, self.detect_and_process)

    def detect_and_process(self):
        """Capture frame, detect closest cube, and send pick goal if available."""
        if self.busy:
            return  # Skip if robot is handling a goal

        ret, frame = self.cap.read()
        if not ret:
            self.get_logger().warning("❌ Failed to read frame.")
            return

        undistorted, _, _ = undistort_image(frame, self.camera_matrix, self.dist_coeffs)
        workspace_data = find_workspace(undistorted)

        if workspace_data:
            x, y, w, h, px_per_mm = workspace_data
            roi = undistorted[y:y + h, x:x + w]

            # Detect closest cube in ROI
            result = detect_single_closest_qr(roi, px_per_mm, x, y)

            if result:
                x_mm, y_mm, theta_deg, qr = result
                self.send_pick_and_place_goal(x_mm, y_mm, theta_deg, qr)

        # Display image window
        # cv2.imshow("Detection Output", undistorted)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     self.shutdown()

        try:
            image_msg = self.bridge.cv2_to_imgmsg(undistorted, encoding='bgr8')
            self.image_pub.publish(image_msg)
        except Exception as e:
            self.get_logger().warning(f"⚠️ Could not publish image: {str(e)}")
    def send_pick_and_place_goal(self, x_mm, y_mm, theta_deg, qr):
        """Send a pick-and-place goal to the action server."""
        goal_msg = PickAndPlace.Goal()

        # Convert positions to meters and set Pose
        pose = Pose()
        pose.position.x = round(y_mm / 1000.0, 5)  # Y in image = X in robot
        pose.position.y = round(x_mm / 1000.0, 5)
        pose.position.z = theta_deg
        pose.orientation.w = 1.0  # No orientation control for now

        goal_msg.target_pose = pose
        goal_msg.qr = qr

        if not self._action_client.wait_for_server(timeout_sec=0.5):
            self.get_logger().warning("⚠️ PickAndPlace action server not available.")
            return

        self.busy = True
        self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        ).add_done_callback(self.goal_response_callback)

        self.get_logger().info(f"📤 Sent {qr} cube goal at X={x_mm:.1f}mm Y={y_mm:.1f}mm")

    def feedback_callback(self, feedback_msg):
        self.get_logger().info(f"📣 Feedback: {feedback_msg.feedback.status}")

    def goal_response_callback(self, future):
        """Handle goal acceptance and result."""
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info("❌ Goal rejected.")
            self.busy = False
            return

        self.get_logger().info("✅ Goal accepted.")
        goal_handle.get_result_async().add_done_callback(self.result_callback)

    def result_callback(self, future):
        """Handle action result and reset state."""
        result = future.result().result
        if result.success:
            self.get_logger().info(f"🎉 Result: {result.message}")
        else:
            self.get_logger().info(f"⚠️ Failed: {result.message}")

        self.busy = False  # Ready for next detection

    def shutdown(self):
        """Release camera and close program."""
        self.cap.release()
        cv2.destroyAllWindows()
        self.get_logger().info("✅ Program ended.")
        rclpy.shutdown()


def main(args=None):
    # rclpy.init(args=args)
    # node = ColorPoseClient()
    # rclpy.spin(node)
    rclpy.init(args=args)
    try:
        node = ColorPoseClient()
        rclpy.spin(node)
    except RuntimeError as e:
        print(str(e))
    finally:
        rclpy.shutdown()


if __name__ == '__main__':
    main()








