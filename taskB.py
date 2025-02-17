import cv2
import numpy as np
import math

def detect_circle(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)
    circles = cv2.HoughCircles(
        blurred,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=50,
        param1=100,
        param2=30,
        minRadius=10,
        maxRadius=50
    )
    if circles is not None:
        circles = np.uint16(np.around(circles))
        return circles[0][0]
    else:
        return None

def detect_rectangle(original_image, cropped_image):
    gray_original = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    gray_cropped = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(gray_original, gray_cropped, cv2.TM_CCOEFF_NORMED)
    _, _, _, max_loc = cv2.minMaxLoc(result)

    top_left = max_loc
    h, w = gray_cropped.shape
    rect_center_x = top_left[0] + w // 2
    rect_center_y = top_left[1] + h // 2
    
    return rect_center_x, rect_center_y

def main(image_path):
    org_image = cv2.imread("aule_space.png")
    if org_image is None:
        print("Error: Unable to read original image.")
        return
    
    circle = detect_circle(org_image)
    if circle is None:
        print("No circle detected in the original image.")
        return

    cx, cy, _ = circle
    print(f"Circle Center: ({cx}, {cy})")

    cropped_image = cv2.imread(image_path)
    if cropped_image is None:
        print(f"Error: Unable to read image from {image_path}")
        return

    rect_center = detect_rectangle(org_image, cropped_image)
    if rect_center is None:
        print("No rectangle detected in the cropped image.")
        return

    rect_center_x, rect_center_y = rect_center
    print(f"Rectangle Center: ({rect_center_x}, {rect_center_y})")

    dx = cx - rect_center_x
    dy = cy - rect_center_y

    horizontal_move = f"{abs(dx)/10} {'cm right' if dx > 0 else 'cm left'}" if dx != 0 else ""
    vertical_move = f"{abs(dy)/10} {'cm down' if dy > 0 else 'cm up'}" if dy != 0 else ""
    
    steps = " and ".join(filter(None, [horizontal_move, vertical_move]))
    print(f"Steps to move rectangle: {steps}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python script.py <image_path>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    main(image_path)