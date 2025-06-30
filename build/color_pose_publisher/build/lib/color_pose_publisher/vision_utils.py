import cv2
import numpy as np

def find_workspace(frame, debug=False, real_width_mm=250, real_height_mm=210):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    block_size = 25
    C = -10
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, block_size, C)
    
    kernel = np.ones((3, 3), np.uint8)
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

    if debug:
        cv2.imshow("Thresholded Workspace", closed)

    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        print("❌ No contours found.")
        return None

    largest_contour = max(contours, key=cv2.contourArea)
    epsilon = 0.02 * cv2.arcLength(largest_contour, True)
    approx = cv2.approxPolyDP(largest_contour, epsilon, True)

    if len(approx) == 4:
        x, y, w_pixels, h_pixels = cv2.boundingRect(largest_contour)
        px_per_mm_width = w_pixels / real_width_mm
        px_per_mm_height = h_pixels / real_height_mm
        px_per_mm = (px_per_mm_width + px_per_mm_height) / 2
        return (x, y, w_pixels, h_pixels, px_per_mm)
    else:
        print(f"⚠️ Contour shape has {len(approx)} sides (expected 4).")
        return None
