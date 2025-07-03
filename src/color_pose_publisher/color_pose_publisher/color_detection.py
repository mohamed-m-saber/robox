# import cv2
# import numpy as np
# import matplotlib.pyplot as plt
# from color_pose_publisher.pose_estimation import estimate_pose

# def detect_and_log_cubes(roi_frame, pixel_size_mm, offset_x, offset_y, detected_cubes, pos_x, pos_y, publish_callback=None):
#     hsv = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2HSV)

#     # Define tightened HSV color ranges
#     colors = {
#         'Red': [([0, 120, 70], [10, 255, 255]), ([170, 120, 70], [180, 255, 255])],
#         'Green': [([40, 70, 70], [75, 255, 255])],
#         'Blue': [([100, 150, 50], [140, 255, 255])]
#     }

#     for color_name, ranges in colors.items():
#         mask = None
#         for lower, upper in ranges:
#             lower_np = np.array(lower)
#             upper_np = np.array(upper)
#             current_mask = cv2.inRange(hsv, lower_np, upper_np)
#             mask = current_mask if mask is None else cv2.bitwise_or(mask, current_mask)

#         contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#         new_poses = []

#         for cnt in contours:
#             area = cv2.contourArea(cnt)
#             if area > 1000:
#                 x, y, w, h = cv2.boundingRect(cnt)
#                 cv2.rectangle(roi_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
#                 cv2.putText(roi_frame, f"{color_name}", (x, y - 5),
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

#                 pose = estimate_pose(cnt, pixel_size_mm, offset_x, offset_y)
#                 if pose[0] is not None:
#                     x_mm, y_mm, z_mm, theta_x, theta_y, theta_z = pose
#                     new_poses.append((x_mm, y_mm, theta_z))

#         # Compare with previous poses and log only if new or moved
#         previous_poses = detected_cubes[color_name]
#         for new_pose in new_poses:
#             is_new = True
#             for prev_pose in previous_poses:
#                 if not pose_is_different(new_pose, prev_pose):
#                     is_new = False
#                     break
#             if is_new:
#                 detected_cubes[color_name].append(new_pose)
#                 pos_x.append(new_pose[0])
#                 pos_y.append(new_pose[1])

#                 # If a publish callback is provided, call it
#                 if publish_callback:
#                     publish_callback(new_pose[0], new_pose[1], new_pose[2], color_name)

#     return roi_frame


# def pose_is_different(pose1, pose2, pos_thresh=2.0, angle_thresh=5.0):
#     """Check if two poses differ by position or angle beyond thresholds."""
#     dx = abs(pose1[0] - pose2[0])
#     dy = abs(pose1[1] - pose2[1])
#     dtheta = abs(pose1[2] - pose2[2])
#     return dx > pos_thresh or dy > pos_thresh or dtheta > angle_thresh











import cv2
import numpy as np
from color_pose_publisher.pose_estimation import estimate_pose


def detect_and_log_cubes(roi_frame, pixel_size_mm, offset_x, offset_y, detected_cubes, pos_x, pos_y, publish_callback=None):
    hsv = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2HSV)

    # Define tightened HSV color ranges (adjusted green)
    colors = {
        'Red': [([0, 120, 70], [10, 255, 255]), ([170, 120, 70], [180, 255, 255])],
        'Green': [([40, 70, 70], [80, 255, 255])],  # adjusted: lower S and V thresholds for better robustness
        'Blue': [([100, 150, 50], [140, 255, 255])]
    }

    for color_name, ranges in colors.items():
        mask = None
        for lower, upper in ranges:
            lower_np = np.array(lower)
            upper_np = np.array(upper)
            current_mask = cv2.inRange(hsv, lower_np, upper_np)
            mask = current_mask if mask is None else cv2.bitwise_or(mask, current_mask)

        # Find contours from the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        new_poses = []

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 1000:
                # Approximate the contour to check for square shape
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.04 * peri, True)

                # Check if it's a quadrilateral
                if len(approx) == 4:
                    x, y, w, h = cv2.boundingRect(cnt)

                    # Check if the bounding box aspect ratio is close to 1 (square)
                    aspect_ratio = w / float(h)
                    if 0.85 <= aspect_ratio <= 1.15:
                        # Draw rectangle and label
                        cv2.rectangle(roi_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        cv2.putText(roi_frame, f"{color_name}", (x, y - 5),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

                        # Estimate real-world pose
                        pose = estimate_pose(cnt, pixel_size_mm, offset_x, offset_y)
                        if pose[0] is not None:
                            x_mm, y_mm, z_mm, theta_x, theta_y, theta_z = pose
                            new_poses.append((x_mm, y_mm, theta_z))

        # Compare with previous poses and log only if new or moved
        previous_poses = detected_cubes[color_name]
        for new_pose in new_poses:
            is_new = True
            for prev_pose in previous_poses:
                if not pose_is_different(new_pose, prev_pose):
                    is_new = False
                    break
            if is_new:
                detected_cubes[color_name].append(new_pose)
                pos_x.append(new_pose[0])
                pos_y.append(new_pose[1])

                # If a publish callback is provided, call it
                if publish_callback:
                    publish_callback(new_pose[0], new_pose[1], new_pose[2], color_name)

    return roi_frame


def pose_is_different(pose1, pose2, pos_thresh=2.0, angle_thresh=5.0):
    """Check if two poses differ by position or angle beyond thresholds."""
    dx = abs(pose1[0] - pose2[0])
    dy = abs(pose1[1] - pose2[1])
    dtheta = abs(pose1[2] - pose2[2])
    return dx > pos_thresh or dy > pos_thresh or dtheta > angle_thresh
