import os
import os.path
import numpy as np
import json
import matplotlib.pyplot as plt

def test_annotations(inpath, outpath, f, yolof, width, height):
    # Parse YOLO formatted string
    sep_yolof = [float(val) for val in yolof.split(" ")]
    pts = sep_yolof[5:]
    center = (sep_yolof[1], sep_yolof[2])
    bbox_w = sep_yolof[3]
    bbox_h = sep_yolof[4]

    # Denormalize handpoints
    dn_handpoints = []
    for p in range(0, len(pts), 2):
        dn_x = pts[p] * width
        dn_y = pts[p + 1] * height
        dn_handpoints.append((dn_x, dn_y))

    # Denormalize bbox width, height, and center
    dn_width = bbox_w * width
    dn_height = bbox_h * height
    dn_centerx = center[0] * width
    dn_centery = center[1] * height

    # Define edges (assuming these are constant for your hand keypoints)
    edges = [[0,1],[1,2],[2,3],[3,4],[0,5],[5,6],[6,7],[7,8],[0,9],[9,10],[10,11],[11,12],[0,13],[13,14],[14,15],[15,16],[0,17],[17,18],[18,19],[19,20]]

    # Display image
    plt.clf()
    im = plt.imread(inpath + f[0:-5] + '.jpg')
    plt.imshow(im)

    # Draw hand keypoints
    for p, point in enumerate(dn_handpoints):
        plt.plot(point[0], point[1], 'r.')
        plt.text(point[0], point[1], f'{p}')

    # Draw edges
    for e in edges:
        plt.plot([dn_handpoints[idx][0] for idx in e],
                    [dn_handpoints[idx][1] for idx in e], color='b')

    # Draw center of bbox
    plt.text(dn_centerx, dn_centery, 'C')

    # Draw bbox
    bbox_x_left = dn_centerx - dn_width / 2
    bbox_y_top = dn_centery - dn_height / 2
    rect = plt.Rectangle((bbox_x_left, bbox_y_top), dn_width, dn_height, linewidth=1, edgecolor='r', facecolor='none')
    plt.gca().add_patch(rect)

    plt.axis('off')
    plt.savefig(outpath + f[0:-5] + 'test' + '.jpg', bbox_inches='tight')
