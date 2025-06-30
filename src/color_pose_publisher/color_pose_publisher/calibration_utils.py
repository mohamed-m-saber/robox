import cv2
import numpy as np

def load_calibration(file_path):
    data = np.load(file_path)
    return data['camera_matrix'], data['dist_coeffs']

def compute_pixel_size(camera_matrix, real_width_mm, pixel_width, distance_mm):
    fx = camera_matrix[0, 0]
    return (fx * real_width_mm) / (pixel_width * distance_mm)

def undistort_image(image, camera_matrix, dist_coeffs):
    h, w = image.shape[:2]
    new_camera_mtx, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coeffs, (w, h), 1, (w, h))
    undistorted = cv2.undistort(image, camera_matrix, dist_coeffs, None, new_camera_mtx)
    x, y, w, h = roi
    return undistorted[y:y + h, x:x + w], new_camera_mtx, roi
