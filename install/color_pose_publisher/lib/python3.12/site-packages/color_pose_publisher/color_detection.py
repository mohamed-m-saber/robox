import cv2
import numpy as np
from color_pose_publisher.pose_estimation import estimate_pose

def detect_single_closest_cube(roi_frame, pixel_size_mm, offset_x, offset_y):
    """Detect all cubes, return pose of the one with lowest Y (closest cube)."""
    hsv = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2HSV)

    # CLAHE for brightness consistency
    h, s, v = cv2.split(hsv)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    v = clahe.apply(v)
    hsv = cv2.merge([h, s, v])

    # Color ranges
    colors = {
        'Red': [
            ([0, 120, 70], [10, 255, 255]),
            ([170, 120, 70], [180, 255, 255])
        ],
        'Green': [
            ([40, 50, 50], [80, 255, 255])
        ],
        'Blue': [
            ([100, 150, 50], [140, 255, 255])
        ]
    }

    kernel = np.ones((5, 5), np.uint8)
    detected_poses = []

    for color_name, ranges in colors.items():
        mask = None
        for lower, upper in ranges:
            lower_np = np.array(lower, dtype=np.uint8)
            upper_np = np.array(upper, dtype=np.uint8)
            current_mask = cv2.inRange(hsv, lower_np, upper_np)
            mask = current_mask if mask is None else cv2.bitwise_or(mask, current_mask)

        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < 1000:
                continue

            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.04 * peri, True)

            if len(approx) != 4:
                continue

            x, y, w, h = cv2.boundingRect(cnt)
            aspect_ratio = w / float(h)
            if not (0.85 <= aspect_ratio <= 1.15):
                continue

            # Draw rectangle and label
            cv2.rectangle(roi_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(roi_frame, color_name, (x, y - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

            pose = estimate_pose(cnt, pixel_size_mm, offset_x, offset_y)
            if pose[0] is not None:
                x_mm, y_mm, z_mm, theta_x, theta_y, theta_z = pose
                detected_poses.append((x_mm, y_mm, theta_z, color_name, y))  # Add image Y for sorting

    if not detected_poses:
        return None  # No cubes detected this frame

    # Pick the cube with lowest image Y (closest to robot)
    closest_cube = min(detected_poses, key=lambda p: p[4])
    return closest_cube[:4]  # Return x_mm, y_mm, theta_z, color_name


