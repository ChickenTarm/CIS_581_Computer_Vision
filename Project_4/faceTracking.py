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
  # video writer inits
  # fourcc = cv2.VideoWriter_fourcc(*'DIVX')
  vid_reader = imageio.get_reader(rawVideo+'.mp4', 'ffmpeg')
  frames = []
  for f in vid_reader:
      frames.append(f)
  # vidcap = cv2.VideoCapture(rawVideo+'.mp4')
  # flag, frame = vidcap.read()
  # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
  frame = frames[0]
  frame_shape = frame.shape[0:2]
  # out = cv2.VideoWriter(rawVideo+'out.avi',fourcc,20.0,frame_shape)
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
  # orig_pts = len(x)
  redetect_thresh = 8
  # cv2.imshow('frame', frame_with_graphics)
  # cv2.waitKey(0)
  output_frames = [frame_with_graphics]
  
  for g in range(1, len(frames))
    print g
    # flag, frame_new = vidcap.read()
    # if not flag:
    #   break
    # frame_new = cv2.cvtColor(frame_new, cv2.COLOR_BGR2RGB)
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
      # bbox = detectFace.detectFace(frame)
      # if len(bbox) > 0:
      # x_new, y_new = getFeatures.getFeatures(frame, bbox)
      x_new, y_new = helper.reGetFeature(frame, bbox_pts)
        # bbox_pts = []
        # for (xb, yb, w, h) in bbox:
        #   bbox_pts.append([(xb,yb), (xb,yb+h), (xb+w,yb+h), (xb+w,yb)])
    # print x_new, y_new, bbox_pts
    frame_with_graphics = helper.draw(frame_new, bbox_pts, x_new, y_new)
    # out.write(frame_with_graphics)
    # out.append_data(frame_with_graphics)
    # cv2.imshow('frame', frame_with_graphics)
    # cv2.waitKey(0)
    x = x_new
    y = y_new
    frame = frame_new
    output_frames.append(frame_with_graphics)
  # return trackedVideo
  imageio.mimsave(rawVideo+'out.mp4', output_frames, format='MP4', fps=25.0)
  # vidcap.release()
  # out.release()
  # out.close()
  # cv2.destroyAllWindows()


if __name__ == '__main__':
  rawVideo = 'Easy/MarquesBrownlee'
  # rawVideo = 'Easy/TheMartian' # params used: re_thresh=0.3, tolerance=4, window=3, minNeighbor=10
  # rawVideo = 'Medium/TyrionLannister' # params used: re_thresh=0.3, tolerance=10, window=3, minNeighbor=5
  # rawVideo = 'Difficult/StrangerThings'
  faceTracking(rawVideo)