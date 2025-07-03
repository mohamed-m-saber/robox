# import rclpy
# from rclpy.node import Node
# from rclpy.action import ActionClient
# from cube_msgs.action import PickAndPlace
# from geometry_msgs.msg import Pose
# import cv2
# from color_pose_publisher.calibration_utils import load_calibration, undistort_image
# from color_pose_publisher.color_detection import detect_and_log_cubes
# from color_pose_publisher.vision_utils import find_workspace
# from ament_index_python.packages import get_package_share_directory
# import os


# class ColorPoseClient(Node):
#     def __init__(self):
#         super().__init__('color_pose_client')

#         # Action client for pick and place goals
#         self._action_client = ActionClient(self, PickAndPlace, 'pick_and_place')

#         # Load camera calibration data
#         package_share_dir = get_package_share_directory('color_pose_publisher')
#         calibration_file = os.path.join(package_share_dir, 'assets', 'camera_calibration_data.npz')
#         self.camera_matrix, self.dist_coeffs = load_calibration(calibration_file)

#         # Open webcam
#         self.cap = cv2.VideoCapture(2)
#         if not self.cap.isOpened():
#             self.get_logger().error("❌ Could not open camera.")
#             rclpy.shutdown()

#         self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
#         self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

#         # Initialize detection data structures
#         self.detected_cubes = {'Red': [], 'Green': [], 'Blue': []}
#         self.pos_x, self.pos_y = [], []

#         # Run detection every 0.033s (~30 FPS)
#         self.create_timer(0.033, self.detect_and_send_goal)

#     def detect_and_send_goal(self):
#         ret, frame = self.cap.read()
#         if not ret:
#             self.get_logger().warning("❌ Failed to read frame.")
#             return

#         undistorted, _, _ = undistort_image(frame, self.camera_matrix, self.dist_coeffs)

#         workspace_data = find_workspace(undistorted)
#         if workspace_data:
#             x, y, w, h, px_per_mm = workspace_data
#             roi = undistorted[y:y + h, x:x + w]

#             # Process ROI, detect cubes and send pick-and-place goals
#             processed = detect_and_log_cubes(
#                 roi, px_per_mm, x, y, self.detected_cubes, self.pos_x, self.pos_y, self.send_pick_and_place_goal
#             )

#             undistorted[y:y + h, x:x + w] = processed

#         cv2.imshow("Detection Output", undistorted)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             self.cap.release()
#             cv2.destroyAllWindows()
#             self.get_logger().info("✅ Program ended.")
#             rclpy.shutdown()

#     def send_pick_and_place_goal(self, x_mm, y_mm, theta_deg, color):
#         """Send a pick-and-place action goal for a detected cube."""
#         goal_msg = PickAndPlace.Goal()

#         pose = Pose()
#         pose.position.x = round((y_mm) / 1000.0, 5)  # convert mm to meters   ,   x,y of the robot are reversed 
#         pose.position.y = round((x_mm) / 1000.0, 5)
#         pose.position.z = 0.0
#         pose.orientation.x = 0.0
#         pose.orientation.y = 0.0
#         pose.orientation.z = 0.0
#         pose.orientation.w = 1.0

#         goal_msg.target_pose = pose
#         goal_msg.color = color

#         if not self._action_client.wait_for_server(timeout_sec=1.0):
#             self.get_logger().warning("⚠️ PickAndPlace action server not available.")
#             return

#         self._action_client.send_goal_async(
#             goal_msg,
#             feedback_callback=self.feedback_callback
#         ).add_done_callback(self.goal_response_callback)

#         self.get_logger().info(f"📤 Sent {color} cube goal at X={x_mm:.1f}mm Y={y_mm:.1f}mm")

#     def feedback_callback(self, feedback_msg):
#         self.get_logger().info(f"📣 Feedback: {feedback_msg.feedback.status}")

#     def goal_response_callback(self, future):
#         goal_handle = future.result()
#         if not goal_handle.accepted:
#             self.get_logger().info("❌ Goal rejected.")
#             return

#         self.get_logger().info("✅ Goal accepted.")
#         goal_handle.get_result_async().add_done_callback(self.result_callback)

#     def result_callback(self, future):
#         result = future.result().result
#         if result.success:
#             self.get_logger().info(f"🎉 Result: {result.message}")
#         else:
#             self.get_logger().info(f"⚠️ Failed: {result.message}")


# def main(args=None):
#     rclpy.init(args=args)
#     node = ColorPoseClient()
#     rclpy.spin(node)


# if __name__ == '__main__':
#     main()






import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from cube_msgs.action import PickAndPlace
from geometry_msgs.msg import Pose
import cv2
from color_pose_publisher.calibration_utils import load_calibration, undistort_image
from color_pose_publisher.color_detection import detect_and_log_cubes
from color_pose_publisher.vision_utils import find_workspace
from ament_index_python.packages import get_package_share_directory
import os


class ColorPoseClient(Node):
    def __init__(self):
        super().__init__('color_pose_client')

        # Action client for pick and place goals
        self._action_client = ActionClient(self, PickAndPlace, 'pick_and_place')

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

        # Initialize detection data structures
        self.detected_cubes = {'Red': [], 'Green': [], 'Blue': []}
        self.pos_x, self.pos_y = [], []

        # Action queue state
        self.goal_queue = []
        self.busy = False

        # Run detection every 0.033s (~30 FPS)
        self.create_timer(0.033, self.detect_and_queue)

    def detect_and_queue(self):
        ret, frame = self.cap.read()
        if not ret:
            self.get_logger().warning("❌ Failed to read frame.")
            return

        undistorted, _, _ = undistort_image(frame, self.camera_matrix, self.dist_coeffs)

        workspace_data = find_workspace(undistorted)
        if workspace_data:
            x, y, w, h, px_per_mm = workspace_data
            roi = undistorted[y:y + h, x:x + w]

            # Process ROI, detect cubes and queue pick-and-place goals
            processed = detect_and_log_cubes(
                roi, px_per_mm, x, y, self.detected_cubes, self.pos_x, self.pos_y, self.queue_pick_and_place_goal
            )

            undistorted[y:y + h, x:x + w] = processed

        cv2.imshow("Detection Output", undistorted)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.cap.release()
            cv2.destroyAllWindows()
            self.get_logger().info("✅ Program ended.")
            rclpy.shutdown()

        # Try sending a queued goal if not busy
        self.process_goal_queue()

    def queue_pick_and_place_goal(self, x_mm, y_mm, theta_deg, color):
        """Add a pick-and-place goal to the queue."""
        self.goal_queue.append((x_mm, y_mm, theta_deg, color))
        self.get_logger().info(f"📝 Queued {color} cube at X={x_mm:.1f}mm Y={y_mm:.1f}mm")

    def process_goal_queue(self):
        """Send the next goal if not busy."""
        if self.busy or not self.goal_queue:
            return

        x_mm, y_mm, theta_deg, color = self.goal_queue.pop(0)
        goal_msg = PickAndPlace.Goal()

        pose = Pose()
        pose.position.x = round((y_mm) / 1000.0, 5)  # mm to meters, y becomes robot's x
        pose.position.y = round((x_mm) / 1000.0, 5)
        pose.position.z = 0.0
        pose.orientation.x = 0.0
        pose.orientation.y = 0.0
        pose.orientation.z = 0.0
        pose.orientation.w = 1.0

        goal_msg.target_pose = pose
        goal_msg.color = color

        if not self._action_client.wait_for_server(timeout_sec=0.5):
            self.get_logger().warning("⚠️ PickAndPlace action server not available.")
            return

        self.busy = True
        self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        ).add_done_callback(self.goal_response_callback)

        self.get_logger().info(f"📤 Sent {color} cube goal at X={x_mm:.1f}mm Y={y_mm:.1f}mm")

    def feedback_callback(self, feedback_msg):
        self.get_logger().info(f"📣 Feedback: {feedback_msg.feedback.status}")

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info("❌ Goal rejected.")
            self.busy = False
            return

        self.get_logger().info("✅ Goal accepted.")
        goal_handle.get_result_async().add_done_callback(self.result_callback)

    def result_callback(self, future):
        result = future.result().result
        if result.success:
            self.get_logger().info(f"🎉 Result: {result.message}")
        else:
            self.get_logger().info(f"⚠️ Failed: {result.message}")

        self.busy = False  # Allow sending next queued goal
        self.process_goal_queue()


def main(args=None):
    rclpy.init(args=args)
    node = ColorPoseClient()
    rclpy.spin(node)


if __name__ == '__main__':
    main()



# #!/usr/bin/env python3

# import rclpy
# from rclpy.node import Node
# from rclpy.action import ActionClient
# from rclpy.parameter import Parameter
# from cube_msgs.action import PickAndPlace
# from geometry_msgs.msg import Pose

# import cv2
# import numpy as np
# from color_pose_publisher.calibration_utils import load_calibration, undistort_image
# from color_pose_publisher.color_detection import detect_and_log_cubes
# from color_pose_publisher.vision_utils import find_workspace
# from ament_index_python.packages import get_package_share_directory
# import os
# import time
# import threading


# class ColorPoseClient(Node):
#     def __init__(self):
#         super().__init__('color_pose_client')

#         # Declare parameters
#         self.declare_parameter('camera_index', 2)
#         self.declare_parameter('detection_rate', 20.0)
#         self.declare_parameter('duplicate_tolerance_mm', 0.0)
#         self.declare_parameter('action_timeout_sec', 30.0)
#         self.declare_parameter('camera_width', 1280)
#         self.declare_parameter('camera_height', 720)
#         self.declare_parameter('enable_debug_logging', False)

#         # Get parameters
#         self.camera_index = self.get_parameter('camera_index').get_parameter_value().integer_value
#         detection_rate = self.get_parameter('detection_rate').get_parameter_value().double_value
#         self.duplicate_tolerance = self.get_parameter('duplicate_tolerance_mm').get_parameter_value().double_value
#         self.action_timeout = self.get_parameter('action_timeout_sec').get_parameter_value().double_value
#         camera_width = self.get_parameter('camera_width').get_parameter_value().integer_value
#         camera_height = self.get_parameter('camera_height').get_parameter_value().integer_value
#         self.debug_logging = self.get_parameter('enable_debug_logging').get_parameter_value().bool_value

#         # Initialize action client
#         self._action_client = ActionClient(self, PickAndPlace, 'pick_and_place')
#         self.is_busy = False
#         self.current_goal_handle = None
#         self.action_start_time = None
        
#         # New state variables for motion-aware detection
#         self.motion_in_progress = False
#         self.detection_paused = False
#         self.goal_sent = False  # Track if goal has been sent for current detection

#         # Load camera calibration
#         try:
#             package_share_dir = get_package_share_directory('color_pose_publisher')
#             calibration_file = os.path.join(package_share_dir, 'assets', 'camera_calibration_data.npz')
#             self.camera_matrix, self.dist_coeffs = load_calibration(calibration_file)
#             self.get_logger().info("✅ Camera calibration loaded successfully.")
#         except Exception as e:
#             self.get_logger().error(f"❌ Failed to load camera calibration: {e}")
#             self.camera_matrix = None
#             self.dist_coeffs = None

#         # Initialize camera
#         self.cap = None
#         self.initialize_camera(camera_width, camera_height)

#         # Detection queue and state
#         self.detection_queue = []
#         self.last_detection_time = time.time()
#         self.detection_lock = threading.Lock()

#         # Create detection timer
#         detection_period = 1.0 / detection_rate
#         self.detection_timer = self.create_timer(detection_period, self.detect_and_queue)

#         # Create timeout checker timer
#         self.timeout_timer = self.create_timer(1.0, self.check_action_timeout)

#         self.get_logger().info("🚀 ColorPoseClient initialized successfully.")

#     def initialize_camera(self, width, height):
#         """Initialize camera with error handling and fallback options."""
     
#         try:
#             self.cap = cv2.VideoCapture(self.camera_index,cv2.CAP_V4L2)
#             if not self.cap.isOpened():
#                 raise RuntimeError(f"Camera {self.camera_index} could not be opened")

#             # Set camera properties
#             self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
#             self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
#             self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Reduce buffer to get latest frames

#             # Test frame capture
#             ret, frame = self.cap.read()
#             if not ret:
#                 raise RuntimeError("Failed to capture test frame")

#             self.get_logger().info(f"✅ Camera {self.camera_index} initialized successfully at {width}x{height}.")
#             return

#         except Exception as e:
#             self.get_logger().warning(f"⚠️ Camera initialization attempt failed: {e}")
#             if self.cap:
#                 self.cap.release()
#                 self.cap = None
            
#         # Final failure
#         self.get_logger().error("❌ Failed to initialize any camera. Shutting down.")
#         rclpy.shutdown()

#     def is_duplicate_cube(self, new_cube):
#         """Check if cube is duplicate based on position tolerance."""
#         new_x, new_y, _, new_color = new_cube
        
#         for existing_cube in self.detection_queue:
#             existing_x, existing_y, _, existing_color = existing_cube
            
#             # Check if same color and within tolerance distance
#             if (new_color == existing_color and 
#                 abs(new_x - existing_x) < self.duplicate_tolerance and 
#                 abs(new_y - existing_y) < self.duplicate_tolerance):
#                 return True
#         return False

#     def detect_and_queue(self):
#         """Main detection loop with motion-aware detection control."""
#         if not self.cap or not self.cap.isOpened():
#             self.get_logger().warning("⚠️ Camera not available for detection.")
#             return

#         # Skip detection if motion is in progress
#         if self.motion_in_progress:
#             if self.debug_logging:
#                 self.get_logger().debug("⏸️ Detection paused - motion in progress.")
#             return

#         try:
#             # Read frame
#             ret, frame = self.cap.read()
#             if not ret:
#                 self.get_logger().warning("⚠️ Failed to read frame from camera.")
#                 return

#             # Process frame
#             processed_frame = self.process_frame(frame)
            
#             # Display result
#             if processed_frame is not None:
#                 cv2.imshow("Detection Output", processed_frame)
                
#             # Handle window events
#             key = cv2.waitKey(1) & 0xFF
#             if key == ord('q'):
#                 self.shutdown_gracefully()
#             elif key == ord('c'):  # Clear queue
#                 with self.detection_lock:
#                     self.detection_queue.clear()
#                     self.goal_sent = False  # Reset goal sent flag
#                 self.get_logger().info("🗑️ Detection queue cleared.")

#             # Process next goal if not busy and goal hasn't been sent yet
#             if not self.is_busy and not self.goal_sent:
#                 self.process_next_goal()

#         except Exception as e:
#             self.get_logger().error(f"❌ Error in detection loop: {e}")

#     def process_frame(self, frame):
#         """Process a single frame and return the processed image."""
#         try:
#             # Apply camera calibration if available
#             if self.camera_matrix is not None and self.dist_coeffs is not None:
#                 undistorted, _, _ = undistort_image(frame, self.camera_matrix, self.dist_coeffs)
#             else:
#                 undistorted = frame.copy()
#                 self.get_logger().warning("⚠️ No camera calibration applied.")

#             # Find workspace
#             workspace_data = find_workspace(undistorted)
#             if not workspace_data:
#                 if self.debug_logging:
#                     self.get_logger().debug("🔍 No workspace detected in current frame.")
#                 return undistorted

#             x, y, w, h, px_per_mm = workspace_data
#             roi = undistorted[y:y + h, x:x + w]

#             # Detect cubes
#             detected_cubes, processed_roi = detect_and_log_cubes(roi, px_per_mm, x, y)

#             # Add new cubes to queue only if no motion is in progress
#             if not self.motion_in_progress:
#                 new_cubes_count = -1
#                 with self.detection_lock:
#                     for cube in detected_cubes:
#                         if not self.is_duplicate_cube(cube):
#                             self.detection_queue.append(cube)
                            

#                 if new_cubes_count > 0:
#                     self.get_logger().info(f"🎯 Added {new_cubes_count} new cubes to queue. Total: {len(self.detection_queue)}")

#             # Update processed frame
#             undistorted[y:y + h, x:x + w] = processed_roi

#             return undistorted

#         except Exception as e:
#             self.get_logger().error(f"❌ Error processing frame: {e}")
#             return frame

#     def process_next_goal(self):
#         """Process the next cube in the queue."""
#         with self.detection_lock:
#             if self.is_busy or not self.detection_queue or self.goal_sent:
#                 return

#             # Sort by y_mm (ascending) since pose.position.x = y_mm/1000.0
#             # This prioritizes cubes with minimum pose.position.x
#             self.detection_queue.sort(key=lambda c: c[1])
#             x_mm, y_mm, theta_deg, color = self.detection_queue.pop(0)

#         # Create goal message
#         goal_msg = PickAndPlace.Goal()
#         pose = Pose()
        
#         # Convert coordinates (mm to meters) and transform coordinate system
#         pose.position.x = round((y_mm) / 1000.0, 5)  # Image Y → Robot X
#         pose.position.y = round((x_mm) / 1000.0, 5)  # Image X → Robot Y
#         pose.position.z = 0.0
#         pose.orientation.x = 0.0
#         pose.orientation.y = 0.0
#         pose.orientation.z = 0.0
#         pose.orientation.w = 1.0

#         goal_msg.target_pose = pose
#         goal_msg.color = color

#         # Wait for action server
#         if not self._action_client.wait_for_server(timeout_sec=1.0):
#             self.get_logger().warning("⚠️ PickAndPlace action server not available. Re-queuing cube.")
#             with self.detection_lock:
#                 self.detection_queue.insert(0, (x_mm, y_mm, theta_deg, color))
#             return

#         # Send goal
#         self.is_busy = True
#         self.motion_in_progress = True  # Start motion state
#         self.goal_sent = True  # Mark goal as sent
#         self.action_start_time = time.time()

#         future = self._action_client.send_goal_async(
#             goal_msg,
#             feedback_callback=self.feedback_callback
#         )
#         future.add_done_callback(self.goal_response_callback)

#         self.get_logger().info(f"📤 Sent {color} cube goal at pose.position.x={y_mm/1000.0:.3f}m (Y={y_mm:.1f}mm, X={x_mm:.1f}mm) (Queue: {len(self.detection_queue)})")
#         self.get_logger().info("⏸️ Detection paused - waiting for motion to complete.")

#     def feedback_callback(self, feedback_msg):
#         """Handle action feedback."""
#         if self.debug_logging:
#             self.get_logger().info(f"📣 Feedback: {feedback_msg.feedback.status}")

#     def goal_response_callback(self, future):
#         """Handle goal response."""
#         try:
#             goal_handle = future.result()
#             if not goal_handle.accepted:
#                 self.get_logger().warning("❌ Goal rejected by action server.")
#                 self.reset_busy_state()
#                 return

#             self.get_logger().info("✅ Goal accepted by action server.")
#             self.current_goal_handle = goal_handle
#             goal_handle.get_result_async().add_done_callback(self.result_callback)

#         except Exception as e:
#             self.get_logger().error(f"❌ Error in goal response: {e}")
#             self.reset_busy_state()

#     def result_callback(self, future):
#         """Handle action result."""
#         try:
#             result = future.result().result
#             if result.success:
#                 self.get_logger().info(f"🎉 Action completed successfully: {result.message}")
#             else:
#                 self.get_logger().warning(f"⚠️ Action failed: {result.message}")

#         except Exception as e:
#             self.get_logger().error(f"❌ Error getting action result: {e}")
#         finally:
#             self.reset_busy_state()

#     def check_action_timeout(self):
#         """Check if current action has timed out."""
#         if (self.is_busy and self.action_start_time and 
#             time.time() - self.action_start_time > self.action_timeout):
            
#             self.get_logger().warning(f"⏰ Action timeout after {self.action_timeout}s. Canceling and resetting.")
            
#             if self.current_goal_handle:
#                 try:
#                     self.current_goal_handle.cancel_goal_async()
#                 except Exception as e:
#                     self.get_logger().error(f"❌ Error canceling goal: {e}")
            
#             self.reset_busy_state()

#     def reset_busy_state(self):
#         """Reset the busy state and related variables."""
#         self.is_busy = False
#         self.motion_in_progress = False  # Reset motion state
#         self.goal_sent = False  # Reset goal sent flag
#         self.current_goal_handle = None
#         self.action_start_time = None
        
#         # Clear detection queue to start fresh
#         with self.detection_lock:
#             self.detection_queue.clear()
        
#         self.get_logger().info("▶️ Detection resumed - ready for new cubes.")

#     def shutdown_gracefully(self):
#         """Perform graceful shutdown."""
#         self.get_logger().info("🛑 Initiating graceful shutdown...")
        
#         # Cancel current action if running
#         if self.current_goal_handle:
#             try:
#                 self.current_goal_handle.cancel_goal_async()
#             except Exception as e:
#                 self.get_logger().warning(f"⚠️ Error canceling action during shutdown: {e}")

#         # Release camera
#         if self.cap and self.cap.isOpened():
#             self.cap.release()
#             self.get_logger().info("📷 Camera released.")

#         # Close CV windows
#         cv2.destroyAllWindows()
        
#         self.get_logger().info("✅ Graceful shutdown completed.")
#         rclpy.shutdown()

#     def __del__(self):
#         """Destructor to ensure proper cleanup."""
#         try:
#             if hasattr(self, 'cap') and self.cap and self.cap.isOpened():
#                 self.cap.release()
#             cv2.destroyAllWindows()
#         except Exception:
#             pass  # Ignore errors during cleanup


# def main(args=None):
#     rclpy.init(args=args)
    
#     try:
#         node = ColorPoseClient()
#         rclpy.spin(node)
#     except KeyboardInterrupt:
#         print("\n🛑 Interrupted by user")
#     except Exception as e:
#         print(f"❌ Fatal error: {e}")
#     finally:
#         try:
#             rclpy.shutdown()
#         except Exception:
#             pass


# if __name__ == '__main__':
#     main()




