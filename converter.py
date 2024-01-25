import json
import os

def convert_to_yolopose_format(data, image_width, image_height, output_dir):
    # if not os.path.exists(output_dir):
    #     os.makedirs(output_dir)

    # Extract data from JSON
    print(data)

    file_name = data['mpii_image'].replace(".jpg", ".txt")
    keypoints = data['mpii_body_pts']
    bbox = data['head_box']  

    # Calculate bbox center, width, and height 
    #TODO: check this :)
    x_center = (bbox[0][0] + bbox[1][0]) / 2.0
    y_center = (bbox[0][1] + bbox[1][1]) / 2.0
    width = abs(bbox[1][0] - bbox[0][0])
    height = abs(bbox[1][1] - bbox[0][1])

    # Normalize coordinates
    x_center /= image_width
    y_center /= image_height
    width /= image_width
    height /= image_height

    # Normalize keypoints
    norm_keypoints = [f"{kp[0]/image_width} {kp[1]/image_height}" for kp in keypoints if kp[2] != 0]

    #combine
    yolopose_line = f"0 {x_center} {y_center} {width} {height} {' '.join(norm_keypoints)}\n"
    print(yolopose_line)

    # Write
    with open(os.path.join(output_dir, file_name), 'w') as file:
        file.write(yolopose_line)
