# import cv2
# import numpy as np
# def estimate_pose(cnt, px_per_mm, offset_x, offset_y):
#     M = cv2.moments(cnt)
#     if M['m00'] == 0:
#         return None, None, None, None, None, None

#     cx = int(M['m10'] / M['m00'])
#     cy = int(M['m01'] / M['m00'])

#     # Orientation (theta_z)
#     if M['m20'] + M['m02'] == 0:
#         theta_z = 0.0
#     else:
#         mu20 = M['m20'] / M['m00']
#         mu02 = M['m02'] / M['m00']
#         mu11 = M['m11'] / M['m00']
#         angle = 0.5 * np.arctan2(2 * mu11, (mu20 - mu02))
#         theta_z = np.degrees(angle)

#     # ✅ Remove offset_x, offset_y since cx, cy are relative to workspace ROI
#     x_mm = cx / px_per_mm
#     y_mm = cy / px_per_mm
#     z_mm = 2.0

#     theta_x = 0.0
#     theta_y = 0.0

#     return round(x_mm, 5), round(y_mm, 5), round(z_mm, 5), round(theta_x, 5), round(theta_y, 5), round(theta_z, 5)

















# import cv2
# import numpy as np

# def estimate_pose(cnt, px_per_mm, offset_x, offset_y):
#     M = cv2.moments(cnt)
#     if M['m00'] == 0:
#         return None, None, None, None, None, None

#     cx = int(M['m10'] / M['m00'])
#     cy = int(M['m01'] / M['m00'])

#     # Orientation (theta_z) relative to horizontal axis
#     if M['m20'] + M['m02'] == 0:
#         theta_z_x_axis = 0.0
#     else:
#         mu20 = M['m20'] / M['m00']
#         mu02 = M['m02'] / M['m00']
#         mu11 = M['m11'] / M['m00']
#         angle = 0.5 * np.arctan2(2 * mu11, (mu20 - mu02))
#         theta_z_x_axis = np.degrees(angle)

#     # Now adjust angle relative to vertical axis
#     theta_z_y_axis = (theta_z_x_axis - 90.0) % 360

#     # Position in mm relative to ROI
#     x_mm = cx / px_per_mm
#     y_mm = cy / px_per_mm
#     z_mm = 2.0

#     theta_x = 0.0
#     theta_y = 0.0

#     return round(x_mm, 5), round(y_mm, 5), round(z_mm, 5), round(theta_x, 5), round(theta_y, 5), round(theta_z_y_axis, 5)








import cv2
import numpy as np

def estimate_pose(cnt, px_per_mm, offset_x, offset_y):
    # Error handling
    if not cnt.any() or px_per_mm <= 0:
        raise ValueError("Invalid contour or px_per_mm")

    # Get minimum area rectangle
    rect = cv2.minAreaRect(cnt)
    (cx, cy), (width, height), angle = rect

    # Adjust angle so long side is vertical if needed
    if width < height:
        angle += 90.0

    # Normalize angle to [0, 360) and reduce to [0, 90) for cube symmetry
    angle = angle % 360
    theta_z = angle % 90

    # Position in mm relative to ROI
    x_mm = cx  / px_per_mm
    y_mm = cy  / px_per_mm

    # Fixed values for unused outputs
    z_mm = 0.0
    theta_x = 0.0
    theta_y = 0.0

    return round(x_mm, 5), round(y_mm, 5), round(z_mm, 5), round(theta_x, 5), round(theta_y, 5), round(theta_z, 5)