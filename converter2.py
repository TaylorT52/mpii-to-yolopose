import os
import os.path
import numpy as np
import json
import matplotlib as plt
import matplotlib.pyplot as plt


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
    # Plot annotations

    edges = [[0,1],[1,2],[2,3],[3,4],[0,5],[5,6],[6,7],[7,8],[0,9],[9,10],[10,11],[11,12],[0,13],[13,14],[14,15],[15,16],[0,17],[17,18],[18,19],[19,20]]
    
    plt.clf()
    print(inpath+f[0:-5]+'.jpg')
    im = plt.imread(inpath+f[0:-5]+'.jpg')
    plt.imshow(im)

    for p in range(len(hand_points)):
        if pts[p,2]!=0:
            plt.plot(pts[p,0], pts[p,1],'r.')
            plt.text(pts[p,0], pts[p,1], '{0}'.format(p))

    for ie, e in enumerate(edges):
        if np.all(pts[e,2]!=0):
            plt.plot(pts[e,0],pts[e,1],color='b')

    plt.text(center[0], center[1], 'C')
    bbox_x_left = min(x)  
    bbox_y_top = min(y)
    rect = plt.Rectangle((bbox_x_left, bbox_y_top), bbox_w, bbox_h, linewidth=1, edgecolor='r', facecolor='none')
    plt.gca().add_patch(rect)

    plt.axis('off')
    plt.savefig(outpath+f[0:-5]+'.jpg', bbox_inches='tight')