'''
  File name: faceTracking.py
  Author: Hongrui Zheng
  Date created: 11/21/2017
'''

'''
  File clarification:
    Generate a video with tracking features and bounding box for face regions
    - Input rawVideo: the video contains one or more faces
    - Output trackedVideo: the generated video with tracked features and bounding box for face regions
'''
import cv2
import numpy as np
import detectFace, getFeatures, estimateFeatureTranslation, estimateAllTranslation, applyGeometricTransformation, helper
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import imageio
import time

def faceTracking(rawVideo):
  vid_reader = imageio.get_reader(rawVideo+'.mp4', 'ffmpeg')
  frames = []
  for f in vid_reader:
      frames.append(f)
  frame = frames[0]
  frame_shape = frame.shape[0:2]
  out = imageio.get_writer(rawVideo+'out.mp4', fps=20.0)
  # face/feature detection
  bbox = detectFace.detectFace(frame)
  x, y = getFeatures.getFeatures(frame, bbox)

  # displaying stuff
  bbox_pts = []
  for (xb, yb, w, h) in bbox:
    bbox_pts.append([(xb,yb), (xb,yb+h), (xb+w,yb+h), (xb+w,yb)])
  frame_with_graphics = helper.draw(frame, bbox_pts, x, y)
  out.append_data(frame_with_graphics)
  redetect_thresh = 8
  output_frames = [frame_with_graphics]
  
  for g in range(1, len(frames)):
    print g
    frame_new = frames[g]
    newXs, newYs = estimateAllTranslation.estimateAllTranslation(x, y, frame, frame_new)
    x_new, y_new, bbox_pts = applyGeometricTransformation.applyGeometricTransformation(x, y, newXs, newYs, bbox_pts)
    # redetect
    min_feat = float('Inf')
    for i in xrange(x_new.shape[1]):
      feats = len(x_new[:,i][x_new[:,i]>=0])
      if feats<min_feat:
        min_feat = feats
    if min_feat < redetect_thresh:
      print 'redetect'
      x_new, y_new = helper.reGetFeature(frame, bbox_pts)
    frame_with_graphics = helper.draw(frame_new, bbox_pts, x_new, y_new)
    plt.imshow(frame_with_graphics)
    plt.show()
    x = x_new
    y = y_new
    frame = frame_new
    out.append_data(frame_with_graphics)
  out.close()


if __name__ == '__main__':
  # rawVideo = 'Easy/MarquesBrownlee'
  # rawVideo = 'Easy/TheMartian'
  # rawVideo = 'Medium/TyrionLannister'
  rawVideo = 'Difficult/StrangerThings'# doesn't work properly
  faceTracking(rawVideo)