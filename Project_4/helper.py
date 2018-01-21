'''
  File name: helper.py
  Author: Hongrui Zheng, Tarmily Wen
  Date created: 11/23/2017
'''

'''
  File clarification:
  Include any helper function you want for this project such as the 
  video frame extraction, video generation, drawing bounding box and so on.
'''
import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import copy

"""
Helper function to display bbox and features on the frame
input:      frame: the frame from original video
            bbox: the bounding box for face
            feature_x: x-coords for feature points
            feature_y: y-coords for feature points
output:     image: cv2 image with all added graphics
"""
def draw(frame, bbox, feat_x, feat_y):
    curr_img = copy.deepcopy(frame)

    faces = len(bbox)

    for i in range(0, faces):
        real_x = feat_x[feat_x >= 0]
        real_y = feat_y[feat_y >= 0]
        box = np.asarray(bbox, dtype=int)
        for j in range(0, len(real_x)):
            curr_img = cv2.circle(img=curr_img, center=(real_x[j], real_y[j]), radius=2, color=(255, 255, 0),
                                  thickness=-1)
        curr_img = cv2.polylines(img=curr_img, pts=box, isClosed=True, thickness=1, color=(0, 255, 0))

    return curr_img


def reGetFeature(img, bbox_pts):
    # max number of features
    N = 100
    x = []
    y = []
    for rect in bbox_pts:
        # rect: top left, bot left, bot right, top right
        # print np.array(rect)
        path = Path(np.array(rect), closed=False)
        # print path
        width = np.max([coord[0] for coord in rect]) - np.min([coord[0] for coord in rect])
        height = np.max([coord[1] for coord in rect]) - np.min([coord[1] for coord in rect])
        xb = rect[0][0]
        yb = rect[0][1]
        crop_box = img[yb:yb+height, xb:xb+width]
        crop_box_gray = cv2.cvtColor(crop_box, cv2.COLOR_BGR2GRAY)
        crop_corners = cv2.goodFeaturesToTrack(crop_box_gray, N, 0.01, 8)
        # crop_corners = np.int0(crop_corners)
        print rect
        crop_corners = np.reshape(crop_corners, (crop_corners.shape[0],crop_corners.shape[2]))
        crop_corners = crop_corners + [xb, yb]
        crop_corners = crop_corners[path.contains_points(crop_corners)]
        x_feat = crop_corners[:,0]
        y_feat = crop_corners[:,1]
        x_feat_l = np.array([-1]*N)[np.newaxis].T
        x_feat_l[0:len(x_feat),:] = np.array(x_feat)[np.newaxis].T
        y_feat_l = np.array([-1]*N)[np.newaxis].T
        y_feat_l[0:len(y_feat),:] = np.array(y_feat)[np.newaxis].T
        if len(x) == 0:
            y = y_feat_l
            x = x_feat_l
        else:
            try:
                y = np.append(y, y_feat_l, axis=1)
                x = np.append(x, x_feat_l, axis=1)
            except:
                print y.shape, y_feat_l.shape
    return x, y