import os
import os.path
import numpy as np
import json
import matplotlib as plt
import matplotlib.pyplot as plt
import checkyolo


plt.rcParams['figure.figsize'] = (20,20)
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'

outpath = "test_output/"
if not os.path.isdir(outpath):
    os.makedirs(outpath)

# Input data paths
paths = ['test/']
inpath = paths[0]
files = sorted([f for f in os.listdir(inpath) if f.endswith('.json')])

for f in files:
    im = plt.imread(inpath+f[0:-5]+'.jpg')
    height, width = im.shape[:2]

    with open(inpath+f, 'r') as fid:
        dat = json.load(fid)

    pts = np.array(dat['hand_pts'])
    invalid = pts[:,2]!=1
    
    file_name = dat["mpii_image"].replace(".jpg", ".txt")
    label = dat["mpii_annorect_idx"]
    center = dat["hand_box_center"]  
    dat['hand_pts'] = pts.tolist()

    x = []
    y = []
    hand_points = []
    normalized_hand_points = []
    for p in range(pts.shape[0]):
        if pts[p,2]!=0:
            hand_points.append((pts[p,0], pts[p,1]))
            x.append(pts[p,0])
            y.append(pts[p,1])
            normalized_hand_points.append(pts[p,0]/width)
            normalized_hand_points.append(pts[p,1]/height)

    bbox_w = max(x) - min(x)
    bbox_h = max(y)- min(y)

    normalized_center_x = center[0] / width
    normalized_center_y = center[1] / height
    normalized_bbox_width = bbox_w / width
    normalized_bbox_height = bbox_h / height
    norm_keypoints_str = ' '.join(str(num) for num in normalized_hand_points)

    yolopose_line = f"{label} {normalized_center_x} {normalized_center_y} {normalized_bbox_width} {normalized_bbox_height} {norm_keypoints_str}\n"
            
            
    ############### testing ###############
    checkyolo.test_annotations(inpath, outpath, f, yolopose_line, width, height)
