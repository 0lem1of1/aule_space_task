import cv2
import numpy as np
import math
import os

def incremental_transform(image):
    h, w = image.shape[:2]
    
    original_pts = np.float32([
        [0, 0],        
        [w, 0],        
        [0, h],        
        [w, h]         
    ])
    

    x_left = 45  
    y_left = 20
    x_right = 10
    y_right = 25  

    new_pts_right = np.float32([
        [x_left, y_left],      
        [w+x_right, -y_right],           
        [x_left, h - y_left],  
        [w+x_right, h + y_right]
    ])

    N_transform = 10

    intermediate_images = []

    for k in range(N_transform + 1):
        t = k / N_transform
        
        new_pts_k = (1 - t) * new_pts_right + t * original_pts
        new_pts_k = new_pts_k.astype(np.float32)
        
        H_k = cv2.getPerspectiveTransform(new_pts_right, new_pts_k)
        
        warped = cv2.warpPerspective(image, H_k, (w, h))
        
        warped_rgb = cv2.cvtColor(warped, cv2.COLOR_BGR2RGB)
        intermediate_images.append(warped_rgb)
    
    return intermediate_images

def main(image_path):
    output_folder = "intermediate_steps"
    os.makedirs(output_folder, exist_ok=True)

    image = cv2.imread(image_path)

    intermediate_images = incremental_transform(image)

    for i, img in enumerate(intermediate_images):
        output_path = os.path.join(output_folder, f"step_{i}.png")
        cv2.imwrite(output_path, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))

if __name__ == "__main__":
    transformed_path = "transformed_aule_space.png"  
    main(transformed_path)
