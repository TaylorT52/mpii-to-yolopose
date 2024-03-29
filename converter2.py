import os
import os.path
import numpy as np
import json
import matplotlib.pyplot as plt
import checkyolo
import shutil

#TODO: ADD OUTPATH HERE
outpath = "../../labels_training/manual_test/"
if not os.path.isdir(outpath):
    os.makedirs(outpath)

#TODO: ADD INPUT DATA PATH HERE
test_img_path = "../../labels_training/test_annot/"
#TODO: ADD IN PATH HERE
inpath = "../../hand-labels-yolof/manual_test/"
files = sorted([f for f in os.listdir(inpath) if f.endswith('.json')])

for f in files: 
    img_path = inpath+f[0:-5]+'.jpg'
    im = plt.imread(img_path)
    height, width = im.shape[:2]
    with open(inpath+f, 'r') as fid:
        dat = json.load(fid)

    pts = np.array(dat['hand_pts'])
    invalid = pts[:,2]!=1
    
    file_name = f.replace(".jpg", ".txt") 

    #accounting for no mpii_annorect_idx
    try:
        label = dat["mpii_annorect_idx"]
    except: 
        label = 0

    center = dat["hand_box_center"]  
    dat['hand_pts'] = pts.tolist()

    #normalize for yolo!
    norm_x = []
    norm_y = []
    normalized_hand_points = []
    for p in range(pts.shape[0]):
        if pts[p,2]!=0:
            norm_x.append(pts[p,0]/width)
            norm_y.append(pts[p,1]/height)
            normalized_hand_points.append(pts[p,0]/width)
            normalized_hand_points.append(pts[p,1]/height)

    bbox_w = max(norm_x) - min(norm_x)
    bbox_h = max(norm_y)- min(norm_y)

    normalized_center_x = center[0] / width
    normalized_center_y = center[1] / height
    normalized_bbox_width = bbox_w
    normalized_bbox_height = bbox_h
    norm_keypoints_str = ' '.join(str(num) for num in normalized_hand_points)

    #format: <class-index> <x> <y> <width> <height> <px1> <py1> <px2> <py2> ... <pxn> <pyn>

    cont = True
    yolopose_line = f"{label} {normalized_center_x} {normalized_center_y} {normalized_bbox_width} {normalized_bbox_height} {norm_keypoints_str}\n"
    for val in normalized_hand_points:
        if val > 1: 
            print(width, height)
            print(val)
            print(yolopose_line)
            cont = False

    if cont: 
        base_name = f[:-5] 
        txt_file_path = os.path.join(outpath, base_name + '.txt')
        with open(txt_file_path, 'w') as file:
            file.write(yolopose_line)
            shutil.copy(inpath+f[0:-5]+'.jpg', outpath)

    print(yolopose_line)

    ############### testing ###############
    checkyolo.test_annotations(img_path, test_img_path, f, yolopose_line, width, height, output_annotations=True)
