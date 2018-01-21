'''
  File name: estimateAllTranslation.py
  Author: Hongrui Zheng
  Date created: 11/20/2017
'''

'''
  File clarification:
    Estimate the translation for all features for each bounding box as well as its four corners
    - Input startXs: all x coordinates for features wrt the first frame
    - Input startYs: all y coordinates for features wrt the first frame
    - Input img1: the first image frame
    - Input img2: the second image frame
    - Output newXs: all x coordinates for features wrt the second frame
    - Output newYs: all y coordinates for features wrt the second frame
'''

import numpy as np
from scipy import signal
import skimage, estimateFeatureTranslation
import sklearn.preprocessing as prep
import cv2

def estimateAllTranslation(startXs, startYs, img1, img2):
  # # filter for gradient
  # dx = np.asarray([[0.5,0.0,-0.5]])
  # dy = dx.transpose()
<<<<<<< HEAD
  dx = np.asarray([[0.125,0.0,-0.125],[0.25,0.0,-0.25],[0.125,0.0,-0.125]])
  dy = np.asarray([[0.125,0.25,0.125],[0.0,0.0,0.0],[-0.125,-0.25,-0.125]])
  # dx = np.asarray([[1,0,-1],[2,0,-2],[1,0,-1]])
  # dy = np.asarray([[1,2,1],[0,0,0],[-1,-2,-1]])
=======
  # dx = np.asarray([[0.125,0.0,-0.125],[0.25,0.0,-0.25],[0.125,0.0,-0.125]])
  # dy = np.asarray([[0.125,0.25,0.125],[0.0,0.0,0.0],[-0.125,-0.25,-0.125]])
  

  dx = np.asarray([[1.0,0.0,-1.0],[2.0,0.0,-2.0],[1.0,0.0,-1.0]])
  dy = np.asarray([[1.0,2.0,1.0],[0.0,0.0,0.0],[-1.0,-2.0,-1.0]])
  # dx = prep.normalize(dx)
  # dy = prep.normalize(dy)

  # print dx
>>>>>>> 47df3244f0fc75f2d6e90cd3fe61564471afff9f
  # rgb2gray
  I_gray = skimage.color.rgb2gray(img1)
  I_gray_nxt = skimage.color.rgb2gray(img2)
  # I_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
  # I_gray_nxt = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
  # gradients
  Ix = signal.convolve2d(I_gray,dx,'same')
  Iy = signal.convolve2d(I_gray,dy,'same')
  Ix_nxt = signal.convolve2d(I_gray_nxt, dx, 'same')
  Iy_nxt = signal.convolve2d(I_gray_nxt, dy, 'same')
  # take average
  Ix = (Ix+Ix_nxt)/2
  Iy = (Iy+Iy_nxt)/2
  # cv2.imshow('Ix', Ix)
  # cv2.waitKey(0)
  # cv2.imshow('Iy', Iy)
  # cv2.waitKey(0)
  # get new coords
  newXs = np.empty(startXs.shape)
  newYs = np.empty(startYs.shape)
  # num of faces
  num_box = startXs.shape[1]
  for j in xrange(num_box):
    for i in xrange(startXs.shape[0]):
      if startXs[i,j] > 0:
        newX, newY = estimateFeatureTranslation.estimateFeatureTranslation(startXs[i,j], startYs[i,j], Ix, Iy, I_gray, I_gray_nxt)
        newXs[i,j] = newX
        newYs[i,j] = newY
      else:
        newXs[i,j] = -1
        newYs[i,j] = -1
  return newXs, newYs