Task A:
Command: python taskA.py rotated_image.png
Functionality: Preprocesses the rotated image using thresholding and Gaussian blur, applies a Hough transform to detect the port, and compares the detected port center with the original port’s center to determine the angle of rotation.

Task B:
Command: python taskB.py cropped_image.png
Functionality: Uses template matching to locate the cropped segment within the original image and aligns the centers of the two images.

Task C:
Command: python taskC.py
Functionality: Calculates the destination corner points using mathematical and geometric methods, computes the homography matrix, and applies the corresponding transformation.
Output: transformed_aule_space.png

Task D:
Command: python taskD.py transformed_aule_space.png
Functionality: Computes the equations for the incremental translation steps between the transformed image and the original image, then applies the necessary translation.
Output: intermediate_steps
