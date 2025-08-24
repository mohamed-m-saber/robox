# import os
# import cv2
# import rclpy
# from rclpy.node import Node
# from rclpy.action import ActionClient
# from ament_index_python.packages import get_package_share_directory
# from cube_msgs.action import PickAndPlace
# from geometry_msgs.msg import Pose
# from sensor_msgs.msg import Image
# from cv_bridge import CvBridge
# from color_pose_publisher.calibration_utils import load_calibration, undistort_image
# from color_pose_publisher.color_detection import detect_single_closest_cube
# from color_pose_publisher.vision_utils import find_workspace

# class ColorPoseClient(Node):
#     def __init__(self):
#         super().__init__('color_pose_client')
#         self._action_client = ActionClient(self, PickAndPlace, 'pick_and_place')
#         self.declare_parameter("red_priority", 1)
#         self.declare_parameter("blue_priority", 2)
#         self.declare_parameter("green_priority", 3)
#         package_dir = get_package_share_directory('color_pose_publisher')
#         calibration_file = os.path.join(package_dir, 'assets', 'camera_calibration_data.npz')
#         self.camera_matrix, self.dist_coeffs = load_calibration(calibration_file)
#         self.cap = cv2.VideoCapture(2)
#         if not self.cap.isOpened():
#             self.get_logger().error("❌ Could not open camera.")
#             rclpy.shutdown()
#         self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
#         self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
#         self.image_pub = self.create_publisher(Image, 'detection_feed', 10)
#         self.bridge = CvBridge()
#         self.busy = False
#         self.last_sent_pose = None  # (x_mm, y_mm, color)
#         self.processed_colors = []  # Tracks processed colors
#         self.successful_detections = 0  # Tracks successful pick-and-place actions
#         self.create_timer(0.033, self.detect_and_process)

#     def detect_and_process(self):
#         # Stop processing if 3 unique colors have been successfully processed
#         if self.successful_detections >= 3:
#             self.get_logger().info("✅ Reached maximum of 3 unique color detections. Shutting down.")
#             # self.shutdown()
#             return
#         if self.busy:
#             return
#         ret, frame = self.cap.read()
#         if not ret:
#             self.get_logger().warning("❌ Failed to read frame.")
#             return
#         undistorted, _, _ = undistort_image(frame, self.camera_matrix, self.dist_coeffs)
#         workspace_data = find_workspace(undistorted)
#         if workspace_data:
#             x, y, w, h, px_per_mm = workspace_data
#             roi = undistorted[y:y + h, x:x + w]
#             color_priorities = {
#                 'Red': self.get_parameter("red_priority").get_parameter_value().integer_value,
#                 'Green': self.get_parameter("green_priority").get_parameter_value().integer_value,
#                 'Blue': self.get_parameter("blue_priority").get_parameter_value().integer_value,
#             }
#             for color in self.processed_colors:
#                 color_priorities[color] = 9999  # Deprioritize processed colors
#             result = detect_single_closest_cube(roi, px_per_mm, x, y, color_priorities)
#             if result:
#                 x_mm, y_mm, theta_deg, color = result
#                 # Explicitly skip if color was already processed
#                 if color in self.processed_colors:
#                     self.get_logger().info(f"⚠️ Skipped {color} cube: already processed.")
#                     return
#                 current_pose = (x_mm, y_mm, color)
#                 if self.last_sent_pose != current_pose:
#                     self.send_pick_and_place_goal(x_mm, y_mm, theta_deg, color)
#                     self.last_sent_pose = current_pose
#                     self.processed_colors.append(color)
#                     self.get_logger().info(f"📌 Sent detection for {color}. Processed colors: {self.processed_colors}")
#         try:
#             image_msg = self.bridge.cv2_to_imgmsg(undistorted, encoding='bgr8')
#             self.image_pub.publish(image_msg)
#         except Exception as e:
#             self.get_logger().warning(f"⚠️ Could not publish image: {str(e)}")

#     def send_pick_and_place_goal(self, x_mm, y_mm, theta_deg, color):
#         goal_msg = PickAndPlace.Goal()
#         pose = Pose()
#         pose.position.x = round(y_mm / 1000.0, 5)
#         pose.position.y = round(x_mm / 1000.0, 5)
#         pose.position.z = theta_deg
#         pose.orientation.w = 1.0
#         goal_msg.target_pose = pose
#         goal_msg.color = color
#         if not self._action_client.wait_for_server(timeout_sec=0.5):
#             self.get_logger().warning("⚠️ PickAndPlace action server not available.")
#             return
#         self.busy = True
#         self._action_client.send_goal_async(
#             goal_msg, feedback_callback=self.feedback_callback
#         ).add_done_callback(self.goal_response_callback)
#         self.get_logger().info(f"📤 Sent {color} cube goal at X={x_mm:.1f}mm Y={y_mm:.1f}mm")

#     def feedback_callback(self, feedback_msg):
#         self.get_logger().info(f"📣 Feedback: {feedback_msg.feedback.status}")

#     def goal_response_callback(self, future):
#         goal_handle = future.result()
#         if not goal_handle.accepted:
#             self.get_logger().info("❌ Goal rejected.")
#             self.busy = False
#             return
#         self.get_logger().info("✅ Goal accepted.")
#         goal_handle.get_result_async().add_done_callback(self.result_callback)

#     def result_callback(self, future):
#         result = future.result().result
#         if result.success:
#             self.successful_detections += 1
#             self.get_logger().info(f"🎉 Result: {result.message}. Successful detections: {self.successful_detections}/3")
#             if self.successful_detections >= 2:
#                 self.get_logger().info("✅ Reached maximum of 3 unique color detections. Shutting down.")
#                 self.shutdown()
#         else:
#             self.get_logger().info(f"⚠️ Failed: {result.message}")
#             # Remove the last processed color on failure to allow retry
#             if self.processed_colors:
#                 failed_color = self.processed_colors.pop()
#                 self.get_logger().info(f"🔄 Removed {failed_color} from processed colors due to failure.")
#         self.busy = False
#         self.last_sent_pose = None

#     def shutdown(self):
#         self.cap.release()
#         self.get_logger().info("✅ Program ended.")
#         rclpy.shutdown()

# def main(args=None):
#     rclpy.init(args=args)
#     try:
#         node = ColorPoseClient()
#         rclpy.spin(node)
#     except RuntimeError as e:
#         print(str(e))
#     finally:
#         rclpy.shutdown()

# if __name__ == '__main__':
#     main()












# import os
# import cv2
# import rclpy
# from rclpy.node import Node
# from rclpy.action import ActionClient
# from ament_index_python.packages import get_package_share_directory
# from cube_msgs.action import PickAndPlace
# from geometry_msgs.msg import Pose
# from sensor_msgs.msg import Image
# from cv_bridge import CvBridge
# from color_pose_publisher.calibration_utils import load_calibration, undistort_image
# from color_pose_publisher.color_detection import detect_single_closest_cube
# from color_pose_publisher.vision_utils import find_workspace

# class ColorPoseClient(Node):
#     def __init__(self):
#         super().__init__('color_pose_client')
#         self._action_client = ActionClient(self, PickAndPlace, 'pick_and_place')
#         self.declare_parameter("red_priority", 1)
#         self.declare_parameter("blue_priority", 2)
#         self.declare_parameter("green_priority", 3)
#         package_dir = get_package_share_directory('color_pose_publisher')
#         calibration_file = os.path.join(package_dir, 'assets', 'camera_calibration_data.npz')
#         self.camera_matrix, self.dist_coeffs = load_calibration(calibration_file)
#         self.cap = cv2.VideoCapture(2)
#         if not self.cap.isOpened():
#             self.get_logger().error("❌ Could not open camera.")
#             raise RuntimeError("Failed to open camera")
#         self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
#         self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
#         self.image_pub = self.create_publisher(Image, 'detection_feed', 10)
#         self.bridge = CvBridge()
#         self.busy = False
#         self.last_sent_pose = None  # (x_mm, y_mm, color)
#         self.processed_colors = []  # Tracks processed colors
#         self.successful_detections = 0  # Tracks successful pick-and-place actions
#         self.failed_attempts = 0
#         self.max_failed_attempts = 150  # Increased to ~5 seconds at 30 Hz
#         self.fallback_threshold = 50  # Try fallback after 50 failed attempts
#         self.create_timer(0.033, self.detect_and_process)

#     def detect_and_process(self):
#         if self.successful_detections >= 3:
#             self.get_logger().info("✅ Reached maximum of 3 unique color detections. Shutting down.")
#             self.shutdown()
#             return
#         if self.busy:
#             return
#         ret, frame = self.cap.read()
#         if not ret:
#             self.get_logger().warning("❌ Failed to read frame.")
#             self.failed_attempts += 1
#             if self.failed_attempts >= self.max_failed_attempts:
#                 self.get_logger().error(f"❌ Exceeded {self.max_failed_attempts} failed frame reads. Shutting down.")
#                 self.shutdown()
#             return
#         undistorted, _, _ = undistort_image(frame, self.camera_matrix, self.dist_coeffs)
#         workspace_data = find_workspace(undistorted)
#         if workspace_data:
#             x, y, w, h, px_per_mm = workspace_data
#             self.get_logger().info(f"📏 Workspace ROI: x={x}, y={y}, w={w}, h={h}, px_per_mm={px_per_mm:.2f}")
#             roi = undistorted[y:y + h, x:x + w]
#             color_priorities = {
#                 'Red': self.get_parameter("red_priority").get_parameter_value().integer_value,
#                 'Green': self.get_parameter("green_priority").get_parameter_value().integer_value,
#                 'Blue': self.get_parameter("blue_priority").get_parameter_value().integer_value,
#             }
#             available_colors = [c for c in color_priorities if c not in self.processed_colors]
#             self.get_logger().info(f"🔍 Available colors: {available_colors}")
#             # NEW: Fallback to force detection of unprocessed colors
#             if self.failed_attempts >= self.fallback_threshold and available_colors:
#                 self.get_logger().info(f"⚠️ Fallback: Prioritizing unprocessed colors {available_colors}")
#                 for color in available_colors:
#                     color_priorities[color] = 0  # Force unprocessed colors to highest priority
#             for color in self.processed_colors:
#                 color_priorities[color] = 9999  # Deprioritize processed colors
#             result = detect_single_closest_cube(roi, px_per_mm, x, y, color_priorities)
#             if result:
#                 x_mm, y_mm, theta_deg, color = result
#                 self.get_logger().info(f"🟦 Detected cube: {color} at x={x_mm:.1f}mm, y={y_mm:.1f}mm, theta={theta_deg:.1f}deg")
#                 if color in self.processed_colors:
#                     self.get_logger().info(f"⚠️ Skipped {color} cube: already processed.")
#                     self.failed_attempts += 1
#                     if self.failed_attempts >= self.max_failed_attempts:
#                         self.get_logger().error(f"❌ Exceeded {self.max_failed_attempts} failed attempts. Shutting down.")
#                         self.shutdown()
#                     return
#                 current_pose = (x_mm, y_mm, color)
#                 if self.last_sent_pose != current_pose:
#                     self.send_pick_and_place_goal(x_mm, y_mm, theta_deg, color)
#                     self.last_sent_pose = current_pose
#                     self.processed_colors.append(color)
#                     self.failed_attempts = 0
#                     self.get_logger().info(f"📌 Sent detection for {color}. Processed colors: {self.processed_colors}")
#             else:
#                 self.get_logger().info("⚠️ No cube detected.")
#                 self.failed_attempts += 1
#                 if self.failed_attempts >= self.max_failed_attempts:
#                     self.get_logger().error(f"❌ Exceeded {self.max_failed_attempts} failed attempts. Shutting down.")
#                     self.shutdown()
#         try:
#             image_msg = self.bridge.cv2_to_imgmsg(undistorted, encoding='bgr8')
#             self.image_pub.publish(image_msg)
#         except Exception as e:
#             self.get_logger().warning(f"⚠️ Could not publish image: {str(e)}")

#     def send_pick_and_place_goal(self, x_mm, y_mm, theta_deg, color):
#         goal_msg = PickAndPlace.Goal()
#         pose = Pose()
#         pose.position.x = round(y_mm / 1000.0, 5)
#         pose.position.y = round(x_mm / 1000.0, 5)
#         pose.position.z = theta_deg
#         pose.orientation.w = 1.0
#         goal_msg.target_pose = pose
#         goal_msg.color = color
#         if not self._action_client.wait_for_server(timeout_sec=0.5):
#             self.get_logger().warning("⚠️ PickAndPlace action server not available.")
#             self.failed_attempts += 1
#             if self.failed_attempts >= self.max_failed_attempts:
#                 self.get_logger().error(f"❌ Exceeded {self.max_failed_attempts} failed attempts. Shutting down.")
#                 self.shutdown()
#             return
#         self.busy = True
#         self._action_client.send_goal_async(
#             goal_msg, feedback_callback=self.feedback_callback
#         ).add_done_callback(self.goal_response_callback)
#         self.get_logger().info(f"📤 Sent {color} cube goal at X={x_mm:.1f}mm Y={y_mm:.1f}mm")

#     def feedback_callback(self, feedback_msg):
#         self.get_logger().info(f"📣 Feedback: {feedback_msg.feedback.status}")

#     def goal_response_callback(self, future):
#         goal_handle = future.result()
#         if not goal_handle.accepted:
#             self.get_logger().info("❌ Goal rejected.")
#             self.busy = False
#             self.failed_attempts += 1
#             if self.failed_attempts >= self.max_failed_attempts:
#                 self.get_logger().error(f"❌ Exceeded {self.max_failed_attempts} failed attempts. Shutting down.")
#                 self.shutdown()
#             return
#         self.get_logger().info("✅ Goal accepted.")
#         goal_handle.get_result_async().add_done_callback(self.result_callback)

#     def result_callback(self, future):
#         result = future.result().result
#         if result.success:
#             self.successful_detections += 1
#             self.get_logger().info(f"🎉 Result: {result.message}. Successful detections: {self.successful_detections}/3")
#             if self.successful_detections >= 3:
#                 self.get_logger().info("✅ Reached maximum of 3 unique color detections. Shutting down.")
#                 self.shutdown()
#         else:
#             self.get_logger().info(f"⚠️ Failed: {result.message}")
#             if self.processed_colors:
#                 failed_color = self.processed_colors.pop()
#                 self.get_logger().info(f"🔄 Removed {failed_color} from processed colors due to failure.")
#             self.failed_attempts += 1
#             if self.failed_attempts >= self.max_failed_attempts:
#                 self.get_logger().error(f"❌ Exceeded {self.max_failed_attempts} failed attempts. Shutting down.")
#                 self.shutdown()
#         self.busy = False
#         self.last_sent_pose = None

#     def shutdown(self):
#         self.cap.release()
#         self.get_logger().info("✅ Program ended.")
#         if rclpy.ok():
#             rclpy.shutdown()

# def main(args=None):
#     try:
#         rclpy.init(args=args)
#         node = ColorPoseClient()
#         rclpy.spin(node)
#     except RuntimeError as e:
#         print(f"Error: {str(e)}")

# if __name__ == '__main__':
#     main()






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
from color_pose_publisher.color_detection import detect_single_closest_cube
from color_pose_publisher.vision_utils import find_workspace

class ColorPoseClient(Node):
    def __init__(self):
        super().__init__('color_pose_client')
        self._action_client = ActionClient(self, PickAndPlace, 'pick_and_place')
        self.declare_parameter("red_priority", 1)
        self.declare_parameter("blue_priority", 2)
        self.declare_parameter("green_priority", 3)
        package_dir = get_package_share_directory('color_pose_publisher')
        calibration_file = os.path.join(package_dir, 'assets', 'camera_calibration_data.npz')
        self.camera_matrix, self.dist_coeffs = load_calibration(calibration_file)
        self.cap = cv2.VideoCapture(2)
        if not self.cap.isOpened():
            self.get_logger().error("❌ Could not open camera.")
            raise RuntimeError("Failed to open camera")
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.image_pub = self.create_publisher(Image, 'detection_feed', 10)
        self.bridge = CvBridge()
        self.busy = False
        self.last_sent_pose = None
        self.processed_colors = []
        self.successful_detections = 0
        self.create_timer(0.033, self.detect_and_process)

    def detect_and_process(self):
        if self.successful_detections >= 3:
            self.shutdown("Reached 3 unique color detections")
            return
        if self.busy:
            return
        ret, frame = self.cap.read()
        if not ret:
            self.get_logger().warning("❌ Failed to read frame.")
            return
        undistorted, _, _ = undistort_image(frame, self.camera_matrix, self.dist_coeffs)
        workspace_data = find_workspace(undistorted)
        if workspace_data:
            x, y, w, h, px_per_mm = workspace_data
            self.get_logger().info(f"ROI: x={x}, y={y}, w={w}, h={h}")
            roi = undistorted[y:y + h, x:x + w]
            color_priorities = {
                'Red': self.get_parameter("red_priority").get_parameter_value().integer_value,
                'Green': self.get_parameter("green_priority").get_parameter_value().integer_value,
                'Blue': self.get_parameter("blue_priority").get_parameter_value().integer_value,
            }
            for color in self.processed_colors:
                color_priorities[color] = 9999
            result = detect_single_closest_cube(roi, px_per_mm, x, y, color_priorities)
            if result:
                x_mm, y_mm, theta_deg, color = result
                if color in self.processed_colors:
                    self.get_logger().info(f"Skipped {color}: already processed")
                    return
                if self.last_sent_pose != (x_mm, y_mm, color):
                    self.send_pick_and_place_goal(x_mm, y_mm, theta_deg, color)
                    self.last_sent_pose = (x_mm, y_mm, color)
                    self.processed_colors.append(color)
                    self.get_logger().info(f"Sent {color} goal: x={x_mm:.1f}mm, y={y_mm:.1f}mm")
        try:
            self.image_pub.publish(self.bridge.cv2_to_imgmsg(undistorted, encoding='bgr8'))
        except Exception as e:
            self.get_logger().warning(f"Could not publish image: {str(e)}")

    def send_pick_and_place_goal(self, x_mm, y_mm, theta_deg, color):
        goal_msg = PickAndPlace.Goal()
        pose = Pose()
        pose.position.x = round(y_mm / 1000.0, 5)
        pose.position.y = round(x_mm / 1000.0, 5)
        pose.position.z = theta_deg
        pose.orientation.w = 1.0
        goal_msg.target_pose = pose
        goal_msg.color = color
        if not self._action_client.wait_for_server(timeout_sec=0.5):
            self.get_logger().warning("Action server unavailable")
            return
        self.busy = True
        self._action_client.send_goal_async(goal_msg, feedback_callback=self.feedback_callback
        ).add_done_callback(self.goal_response_callback)

    def feedback_callback(self, feedback_msg):
        self.get_logger().info(f"Feedback: {feedback_msg.feedback.status}")

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info("Goal rejected")
            self.busy = False
            return
        self.get_logger().info("Goal accepted")
        goal_handle.get_result_async().add_done_callback(self.result_callback)

    def result_callback(self, future):
        result = future.result().result
        if result.success:
            self.successful_detections += 1
            self.get_logger().info(f"Success: {result.message} ({self.successful_detections}/3)")
            if self.successful_detections >= 3:
                self.shutdown("Reached 3 unique color detections")
        else:
            self.get_logger().info(f"Failed: {result.message}")
            if self.processed_colors:
                self.processed_colors.pop()
        self.busy = False
        self.last_sent_pose = None

    def shutdown(self, message="Program ended"):
        self.cap.release()
        self.get_logger().info(message)
        if rclpy.ok():
            rclpy.shutdown()

def main(args=None):
    try:
        rclpy.init(args=args)
        node = ColorPoseClient()
        rclpy.spin(node)
    except RuntimeError as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()