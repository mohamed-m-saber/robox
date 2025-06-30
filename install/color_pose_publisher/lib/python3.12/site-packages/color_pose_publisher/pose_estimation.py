import cv2
import numpy as np
def estimate_pose(cnt, px_per_mm, offset_x, offset_y):
    M = cv2.moments(cnt)
    if M['m00'] == 0:
        return None, None, None, None, None, None

    cx = int(M['m10'] / M['m00'])
    cy = int(M['m01'] / M['m00'])

    # Orientation (theta_z)
    if M['m20'] + M['m02'] == 0:
        theta_z = 0.0
    else:
        mu20 = M['m20'] / M['m00']
        mu02 = M['m02'] / M['m00']
        mu11 = M['m11'] / M['m00']
        angle = 0.5 * np.arctan2(2 * mu11, (mu20 - mu02))
        theta_z = np.degrees(angle)

    # ✅ Remove offset_x, offset_y since cx, cy are relative to workspace ROI
    x_mm = cx / px_per_mm
    y_mm = cy / px_per_mm
    z_mm = 2.0

    theta_x = 0.0
    theta_y = 0.0

    return round(x_mm, 2), round(y_mm, 2), round(z_mm, 2), round(theta_x, 2), round(theta_y, 2), round(theta_z, 2)
