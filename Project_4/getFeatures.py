'''
  File name: getFeatures.py
  Author: Hongrui Zheng
  Date created: 11/22/2017
'''

'''
  File clarification:
    Detect features within each detected bounding box
    - Input img: the first frame (in the grayscale) of video
    - Input bbox: the four corners of bounding boxes
    - Output x: the x coordinates of features
    - Output y: the y coordinates of features
'''
from skimage.feature import corner_harris, corner_peaks
import cv2
import numpy as np
import matplotlib.pyplot as plt

def getFeatures(img, bbox):
  # max number of features
  N = 100
  x = []
  y = []
  for (xb, yb, w, h) in bbox:
    crop_box = img[yb:yb+h, xb:xb+w]
    crop_box_gray = cv2.cvtColor(crop_box, cv2.COLOR_BGR2GRAY)
    
    crop_corners = cv2.goodFeaturesToTrack(crop_box_gray, N, 0.01, 8)
    crop_corners = np.int0(crop_corners)
    x_feat = [sub[0][0]+xb for sub in crop_corners]
    y_feat = [sub[0][1]+yb for sub in crop_corners]

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