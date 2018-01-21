import sys, os, dlib, cv2, argparse, imutils, imageio
from imutils import face_utils
import numpy as np


def prompt_face(frame, face_detections):
    detect = True
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, 'Left click to choose face, right click to detect in next frame',
        (30,30), font, 0.6, (255,255,255), 1, cv2.LINE_AA)
    for (i, face) in enumerate(face_detections):
        face = face.rect
        (x, y, w, h) = face_utils.rect_to_bb(face)
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0, 255, 0), 2)
    winname = 'Faces'
    cv2.namedWindow(winname, cv2.WINDOW_NORMAL)
    cv2.moveWindow(winname, 400,600)
    cv2.imshow(winname, frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


"""
Find the centroid of all input points
"""
def centroid(points):
    length = points.shape[0]
    sum_x = np.sum(points[:,0])
    sum_y = np.sum(points[:,1])
    return (sum_x/length,sum_y/length)


"""
Find the center of the bounding box for all input points
"""
def bounding_center(points):
    min_x, min_y = np.min(points, axis=0)
    max_x, max_y = np.max(points, axis=0)
    return (int(min_x+(max_x-min_x)/2),int(min_y+(max_y-min_y)/2))