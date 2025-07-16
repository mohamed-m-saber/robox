# import cv2
# import numpy as np
# from pyzbar.pyzbar import decode
# from color_pose_publisher.pose_estimation import estimate_pose  # assuming this takes a contour-like polygon

# def detect_single_closest_qr(roi_frame, pixel_size_mm, offset_x, offset_y):
#     """Detect QR codes, return pose of the highest priority one (by content then proximity)."""
#     kernel = np.ones((5, 5), np.uint8)
#     detected_poses = []

#     # Decode QR codes
#     decoded_objects = decode(roi_frame)

#     if not decoded_objects:
#         return None  # no QR codes detected

#     # Define content priority: lower number = higher priority
#     content_priority = {'bina': 1, 'binb': 2, 'red': 3, 'green': 4, 'blue': 5}

#     for obj in decoded_objects:
#         qr_data = obj.data.decode('utf-8').strip().lower()  # lowercase for consistency

#         if qr_data not in content_priority:
#             continue  # ignore unknown QR labels

#         # Get bounding box info
#         (x, y, w, h) = obj.rect

#         # Compute center point
#         cx = x + w / 2
#         cy = y + h / 2

#         # Convert to mm
#         x_mm = (cx / pixel_size_mm) + offset_x
#         y_mm = (cy / pixel_size_mm) + offset_y

#         # Orientation estimation from bounding box
#         pts = np.array([(p.x, p.y) for p in obj.polygon], dtype=np.int32)

#         if len(pts) < 4:
#             continue  # skip incomplete detections

#         rect = cv2.minAreaRect(pts)
#         angle = rect[2]
#         if angle < -45:
#             angle += 90.0

#         # Optional: draw detection rectangle and label
#         cv2.polylines(roi_frame, [pts], isClosed=True, color=(0, 255, 0), thickness=2)
#         cv2.putText(roi_frame, qr_data, (x, y - 5),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

#         detected_poses.append((
#             content_priority[qr_data],
#             cy,  # for proximity
#             x_mm, y_mm, angle, qr_data
#         ))

#     if not detected_poses:
#         return None  # no relevant QR codes detected

#     # Sort by priority (lower is better), then by image Y (lower is closer)
#     detected_poses.sort()

#     # Pick the best one
#     _, _, x_mm, y_mm, theta_z, qr_data = detected_poses[0]

#     print(f"{qr_data}: x={x_mm:.1f} mm, y={y_mm:.1f} mm, angle={theta_z:.1f}°")

#     return (x_mm, y_mm, theta_z, qr_data)


















import cv2
import numpy as np
from pyzbar.pyzbar import decode
from color_pose_publisher.pose_estimation import estimate_pose  # same function as used for cubes

def detect_single_closest_qr(roi_frame, pixel_size_mm, offset_x, offset_y):
    """Detect QR codes, return pose of the highest priority one (by content then proximity)."""
    kernel = np.ones((5, 5), np.uint8)
    detected_poses = []

    # Decode QR codes
    decoded_objects = decode(roi_frame)

    if not decoded_objects:
        return None  # no QR codes detected

    # Define content priority: lower number = higher priority
    content_priority = {'bina': 1, 'binb': 2, 'red': 3, 'green': 4, 'blue': 5}

    for obj in decoded_objects:
        qr_data = obj.data.decode('utf-8').strip().lower()

        if qr_data not in content_priority:
            continue  # ignore unknown QR labels

        # Get polygon points as contour
        pts = np.array([(p.x, p.y) for p in obj.polygon], dtype=np.int32)

        if len(pts) < 4:
            continue  # skip incomplete detections

        # Draw detection rectangle and label
        cv2.polylines(roi_frame, [pts], isClosed=True, color=(0, 255, 0), thickness=2)
        x, y = pts[0]  # for text placement
        cv2.putText(roi_frame, qr_data, (x, y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

        # Estimate pose using the same estimate_pose() function as for cubes
        pose = estimate_pose(pts, pixel_size_mm, offset_x, offset_y)

        if pose[0] is not None:
            x_mm, y_mm, z_mm, theta_x, theta_y, theta_z = pose

            detected_poses.append((
                content_priority[qr_data],
                y,  # image Y for proximity
                x_mm, y_mm, theta_z, qr_data
            ))

    if not detected_poses:
        return None  # no relevant QR codes detected

    # Sort by priority (lower is better), then by image Y (lower is closer)
    detected_poses.sort()

    # Pick the best one
    _, _, x_mm, y_mm, theta_z, qr_data = detected_poses[0]

    print(f"{qr_data}: x={x_mm:.1f} mm, y={y_mm:.1f} mm, angle={theta_z:.1f}°")

    return (x_mm, y_mm, theta_z, qr_data)
