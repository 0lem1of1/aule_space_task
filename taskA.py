import matplotlib.pyplot as plt 
import numpy as np
import cv2
import sys
import math

def detect_port_centre(image):
    height, width = image.shape[:2]
    image_center = (width // 2, height // 2)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = np.uint8(gray)
    _, thresh = cv2.threshold(gray, 0.1, 255, cv2.THRESH_BINARY_INV)
    blurred = cv2.GaussianBlur(thresh, (9, 9), 5)

    circles = cv2.HoughCircles(
        blurred, 
        cv2.HOUGH_GRADIENT, dp=1.2, minDist=30,
        param1=200, param2=20, minRadius=5, maxRadius=50
    )

    if circles is not None:
        circles = np.uint16(np.around(circles))
        circle = circles[0, 0]
        cx, cy, _ = circle
        
        relative_x = cx - image_center[0]
        relative_y = cy - image_center[1]
        
        return [relative_x, relative_y], (cx, cy)
    else:
        return None, None

import math

def calculate_angle(x, y):
    angle_radians = math.atan2(y, x)
    angle_degrees = math.degrees(angle_radians)
    
    if angle_degrees < 0:
        angle_degrees += 360
    
    return round(angle_degrees, 2)

def main(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Unable to read image from {image_path}")
        return

    rot_centre, rot_absolute = detect_port_centre(image)
    org_image = cv2.imread("aule_space.png")
    if org_image is None:
        print("Error: Unable to read original image")
        return

    org_centre, org_absolute = detect_port_centre(org_image)

    if rot_centre is not None and org_centre is not None:
        angle = calculate_angle(rot_centre[0],rot_centre[1])-calculate_angle(org_centre[0],org_centre[1])
        print(f"Rotated Image Centre (relative): {rot_centre}, Absolute: {rot_absolute}")
        print(f"Original Image Centre (relative): {org_centre}, Absolute: {org_absolute}")
        print(f"Angle rotated: {angle:.2f} degrees")
    else:
        print("Unable to calculate angle: One or both centres not detected")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <image_path>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    main(image_path)
