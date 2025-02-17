import cv2
import numpy as np
import math

def transform_image(image):
    h, w = image.shape[:2]  

    center_screen = (int(w/2), int(h/2))
    center_circle = (178,141) 

    dx = int(w/2)-178  
    dy = int(h/2)-141  

    original_pts = np.float32([
        [0, 0],        
        [w, 0],        
        [0, h],        
        [w, h]         
    ])
    
    new_pts = np.float32([
        [dx, dy],           
        [w+ dx, dy],        
        [dx, h + dy],       
        [w + dx, h + dy]    
    ])

    H_center = cv2.getPerspectiveTransform(original_pts, new_pts)
    centered_image = cv2.warpPerspective(image, H_center, (w, h))

    x_left = 45  
    y_left = 20
    x_right = 10
    y_right = 25  


    new_pts_right = np.float32([
        [x_left, y_left],      
        [w+x_right, -y_right],           
        [x_left, h - y_left],  
        [w+x_right, h + y_right]])

    H_right = cv2.getPerspectiveTransform(original_pts, new_pts_right)

    final_image = cv2.warpPerspective(centered_image, H_right, (w, h))

    return final_image

def main():
    image_path = "aule_space.png"
    image = cv2.imread(image_path)

    t_image = transform_image(image)

    cv2.imwrite("transformed_aule_space.png", t_image)

if __name__ == "__main__":
    main()
