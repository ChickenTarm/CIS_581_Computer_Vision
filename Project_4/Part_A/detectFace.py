'''
  File name: detectFace.py
  Author: Hongrui Zheng
  Date created: 11/22/2017
'''

'''
  File clarification:
    Detect or hand-label bounding box for all face regions
    - Input img: the first frame of video
    - Output bbox: the four corners of bounding boxes for all detected faces
'''
import cv2

def detectFace(img):
  face_cascade = cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml')
  img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  bbox = face_cascade.detectMultiScale(img_gray, scaleFactor=1.1, minNeighbors=6)
  return bbox