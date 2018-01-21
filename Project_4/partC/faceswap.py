'''
  File name: faceswap.py
  Author: Hongrui Zheng
  Date created:
'''

import sys, os, dlib, cv2, argparse, imutils, imageio, utils, cut_out_face, copy, morph_face
from imutils import face_utils
import numpy as np


# parsing arguments
ap = argparse.ArgumentParser()
ap.add_argument('-vb', '--video_background', required=True,
	help='path to the video that the background is kept')
ap.add_argument('-vf', '--video_face', required=True,
	help='path to the video that the face is kept')
ap.add_argument('-out', '--output_name', required=True,
	help='name of the output video')
ap.add_argument('-alpha', '--alpha', required=False,
	help='alpha for alpha blending')
ap.add_argument('-of', '--use_optical_flow', required=False,
	help='whether or not use optical flow')
args = vars(ap.parse_args())

# initializing dlib's cnn-based face detector
cnn_face_detector = dlib.cnn_face_detection_model_v1('mmod_human_face_detector.dat')
detector = dlib.get_frontal_face_detector()
# initializing dlib's facial landmark predictor
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

# alpha for blending
alpha = 1

# initializing opencv stuff
font = cv2.FONT_HERSHEY_SIMPLEX
cap_b = cv2.VideoCapture(args['video_background'])
cap_f = cv2.VideoCapture(args['video_face'])
# cap = cv2.VideoCapture('http://192.168.1.161/live')
ret, f = cap_f.read()
ret, b = cap_b.read()
f_size = f.shape
print f_size[0:2]
writer = imageio.get_writer(args['output_name']+'.mp4', fps=20.0)


# prompt the user if the face found is a good detection
face_dets = detector(f, 1)
cut = None
mask = None
face_pts = None
while True:
	if len(face_dets) == 0:
		ret, f = cap_f.read()
		face_dets = detector(f, 1)
		continue
	for (i, face) in enumerate(face_dets):
	    # face = face.rect
	    f_show = copy.deepcopy(f)
	    (x, y, w, h) = face_utils.rect_to_bb(face)
	    cv2.rectangle(f_show, (x,y), (x+w,y+h), (0, 255, 0), 2)
	    shape = predictor(f, face)
	    shape = face_utils.shape_to_np(shape)
	    for (xs, ys) in shape:
	    	cv2.circle(f_show, (xs, ys), 1, (0,0,255), -1)
	cv2.putText(f_show, 'Press s to select current face',
    	(30,30), font, 1, (255,255,255), 2, cv2.LINE_AA)
	cv2.putText(f_show, 'Press d to detect again',
    	(30,60), font, 1, (255,255,255), 2, cv2.LINE_AA)
	winname = 'Faces'
	cv2.namedWindow(winname, cv2.WINDOW_NORMAL)
	cv2.moveWindow(winname, 400,500)
	cv2.imshow(winname, f_show)
	k = cv2.waitKey(0)
	if k == 115:
		print 'Face Selected'
		face_pts = shape
		break
	elif k == 100:
		print 'Face Not Selected'
		ret, f = cap_f.read()
		face_dets = detector(f, 1)
cv2.destroyAllWindows()



# background loop 
frame = 0
while ret:
	skipping = False
	print 'Current Frame: '+ str(frame)
	ret, body_frame = cap_b.read()
	if not ret:
		break
	face_dets = detector(body_frame, 1)
	for (i, face) in enumerate(face_dets):
		# face = face.rect
		(x, y, w, h) = face_utils.rect_to_bb(face)
		shape = predictor(body_frame, face)
		shape = face_utils.shape_to_np(shape)
		try:
			morphed_face = morph_face.morph_face(f, face_pts, shape,
				body_frame.shape[1], body_frame.shape[0])
		except:
			skipping = True
			continue
		cut = cut_out_face.cut_out_face(morphed_face, shape)

		cut = cut.astype(np.uint8)
		morphed_mask_multi = np.ones(cut.shape, cut.dtype)*255
		morphed_mask = np.ones(cut.shape[0:2], cut.dtype)*255
		morphed_mask_multi[(cut[:,:,0]==0)&(cut[:,:,1]==0)&(cut[:,:,2]==0)] = (0,0,0)
		morphed_mask[(cut[:,:,0]==0)&(cut[:,:,1]==0)&(cut[:,:,2]==0)] = 0
		center = utils.bounding_center(shape)

		body_frame_with_head = np.copy(body_frame)
		body_frame_with_head[morphed_mask>0] = cut[morphed_mask>0]*alpha + body_frame_with_head[morphed_mask>0]*(1-alpha)
		body_frame = cv2.seamlessClone(body_frame_with_head, body_frame, morphed_mask_multi, center, cv2.NORMAL_CLONE)

	frame = frame + 1
	if skipping:
		continue
	writer.append_data(cv2.cvtColor(body_frame, cv2.COLOR_BGR2RGB))

cap_f.release()
# out.release()
writer.close()
cv2.destroyAllWindows()
