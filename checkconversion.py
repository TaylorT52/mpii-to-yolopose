import cv2
import numpy as np

# Function to draw keypoints
def draw_keypoints(image, keypoints, color=(0, 255, 0), radius=5, thickness=-1):
    for i in range(5, len(keypoints), 2):
        x = int(keypoints[i] * image.shape[1])
        y = int(keypoints[i+1] * image.shape[0])
        cv2.circle(image, (x, y), radius, color, thickness)

# Your keypoints data
data_string = "0 0.7880859375 0.12890625 0.1015625 0.20833333333333334 0.8095703125 0.38671875 0.791015625 0.20052083333333334 0.6875 0.5130208333333334 0.744140625 0.3645833333333333 0.875 0.4075520833333333 0.787109375 0.3333333333333333 0.771484375 0.57421875 0.6640625 0.5260416666666666 0.68359375 0.3671875 0.7119140625 0.18489583333333334 0.869140625 0.21614583333333334 0.9130859375 0.3802083333333333 0.85546875 0.4596354166666667"
keypoints = [float(num) for num in data_string.split()]

# Load your image
image_path = 'test/000648952_02_l copy.jpg' 
image = cv2.imread(image_path)

draw_keypoints(image, keypoints)

# Display the image
cv2.imshow("Keypoints", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
