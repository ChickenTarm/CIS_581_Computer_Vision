"""
    File name: video_preprocess.py
    Author: Hongrui Zheng
    Preprocess videos for better face detection results
"""

import sys, os, cv2, argparse, imageio, dlib
from imutils import face_utils
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument('-v', '--video', required=True,
    help='path to the video to be processed')
ap.add_argument('-o', '--output', required=False,
    help='name of output video')
args = vars(ap.parse_args())

cnn_face_detector = dlib.cnn_face_detection_model_v1('mmod_human_face_detector.dat')
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

lk_params = dict(winSize=(15,15),
                 maxLevel=2,
                 criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

cap = cv2.VideoCapture(args['video'])
# writer = imageio.get_writer(args['output']+'.mp4', fps=20.0)
# brightness_change = int(args['brightness_change'])
ret, frame = cap.read()
frame_gray_old = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
face_dets = cnn_face_detector(frame, 1)
for (i, face) in enumerate(face_dets):
    shape = predictor(frame, face.rect)
    shape = face_utils.shape_to_np(shape)
while True:
    ret, frame = cap.read()
    f_show = np.copy(frame)
    if not ret:
        break
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    shape_new, st, err = cv2.calcOpticalFlowPyrLK(frame_gray_old, frame_gray, shape,
        None, **lk_params)
    good_pt_new = shape_new[st == 1]
    good_pt_old = shape[st == 1]
    for (xs, ys) in good_pt_new:
        cv2.circle(f_show, (xs, ys), 2, (0,0,255), -1)
    cv2.imshow('frame', f_show)
    cv2.waitKey(0)
    # converting to HSV
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # frame[:,:,2] += brightness_change
    # writer.append_data(cv2.cvtColor(frame, cv2.COLOR_HSV2RGB))
    frame_gray_old = np.copy(frame_gray)
    shape = good_pt_new
cap.release()
# writer.close()
cv2.destroyAllWindows()