'''
  File name: estimateFeatureTranslation.py
  Author: Hongrui Zheng
  Date created: 11/21/2017
'''

'''
  File clarification:
    Estimate the translation for single features 
    - Input startX: the x coordinate for single feature wrt the first frame
    - Input startY: the y coordinate for single feature wrt the first frame
    - Input Ix: the gradient along the x direction
    - Input Iy: the gradient along the y direction
    - Input img1: the first image frame
    - Input img2: the second image frame
    - Output newX: the x coordinate for the feature wrt the second frame
    - Output newY: the y coordinate for the feature wrt the second frame
'''
import numpy as np
import cv2, skimage

def estimateFeatureTranslation(startX, startY, Ix, Iy, img1, img2):
  # img1 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
  # img2 = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)
  # img1 = skimage.color.rgb2gray(img1)
  # img2 = skimage.color.rgb2gray(img2)
  # klt window size
  size_window = 10
  # temporal gradient
  It = cv2.subtract(img2, img1)
  # cv2.imshow('it', It)
  # cv2.waitKey(0)
  # windows
  Ix_window = Ix[startY-size_window/2:startY+size_window/2, startX-size_window/2:startX+size_window/2]
  Iy_window = Iy[startY-size_window/2:startY+size_window/2, startX-size_window/2:startX+size_window/2]
  It_window = It[startY-size_window/2:startY+size_window/2, startX-size_window/2:startX+size_window/2]
  # finding sums for gradients
  sum_matrix = np.array([[np.sum(Ix_window*Ix_window),np.sum(Ix_window*Iy_window)],[np.sum(Ix_window*Iy_window),np.sum(Iy_window*Iy_window)]])
  # finding sums for temporal gradients
  sum_tempo = np.array([[np.sum(Ix_window*It_window)],[np.sum(Iy_window*It_window)]])
  sum_tempo = -sum_tempo
  # find the inverse
  try:
    sum_inverse = np.linalg.inv(sum_matrix)
  except:
    sum_inverse = sum_matrix
  # solve for u and v
  displacement = np.dot(sum_inverse,sum_tempo)
  # print displacement
  newX = startX+displacement[0,0]
  newY = startY+displacement[1,0]
  # print startX, startY
  # print newX, newY
  return newX, newY
  # return startX+1, startY+1