'''
  File name: FilterImage.py
  Author:
  Date created:
'''

import argparse
import numpy as np
import cv2
from seamlessCloningPoisson import seamlessCloningPoisson
from getOffsets import getOffsets


def getFeatCoor(t):
    target_gray = cv2.cvtColor(t, cv2.COLOR_BGR2GRAY)

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

    faces = face_cascade.detectMultiScale(target_gray, 1.3, 5)

    features = []

    for (x, y, w, h) in faces:
        features.append([(x,y), (x + w, y), (x + w, y + h), (x, y + h)])
        cv2.rectangle(t, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = target_gray[y:y + h, x:x + w]
        roi_color = t[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            features.append([(x + ex, y + ey), (x + ex + ew, y + ey), (x + ex + ew, y + ey + eh), (x + ex, y + ey + eh)])
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

    if features[1][0] > features[2][0]:
        temp = features[1]
        features[1] = features[2]
        features[2] = temp

    return features


def testBoxes(b):
    if len(b) != 3:
        print "Face Detector Failed"
        return False
    else:
        return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("target", type=str, help="The target image that will get all of the filters")
    parser.add_argument("filter", type=int, help="enter 1 for dog, 2 for cat, 3 for eyes, 4 for joker, 5 for anime eyes")



    args = parser.parse_args()

    target_img = cv2.imread(args.target)

    target_img_p = np.copy(target_img)

    boxes = getFeatCoor(target_img)

    filter = args.filter

    print boxes

    filter_list = []

    if filter == 1:
        filter_list.append((0, cv2.imread("Masks/Floppy_Left_Ear_Mask.png")[:,:,0], cv2.imread("Masks/Floppy_Left_Ear.png")))
        filter_list.append((1, cv2.imread("Masks/Floppy_Right_Ear_Mask.png")[:,:,0], cv2.imread("Masks/Floppy_Right_Ear.png")))
        filter_list.append((5, cv2.imread("Masks/Dog_Nose_Mask.png")[:,:,0], cv2.imread("Masks/Dog_Nose.png")))
    elif filter == 2:
        filter_list.append((3, cv2.imread("Masks/catleftear_mask.png")[:,:,0], cv2.imread("Masks/catleftear.png")))
        filter_list.append((4, cv2.imread("Masks/catrightear_mask.png")[:,:,0], cv2.imread("Masks/catrightear.png")))
        filter_list.append((5, cv2.imread("Masks/catnose_mask.png")[:,:,0], cv2.imread("Masks/catnose.png")))
    elif filter == 3:
        filter_list.append((6, cv2.imread("Masks/Left_Eye_Mask.png")[:,:,0], cv2.imread("Masks/Left_Eye.png")))
        filter_list.append((7, cv2.imread("Masks/Right_Eye_Mask.png")[:,:,0], cv2.imread("Masks/Right_Eye.png")))
    elif filter == 4:
        filter_list.append((8, cv2.imread("Masks/Joker_Nose_Mask.png")[:,:,0], cv2.imread("Masks/Joker_Nose.png")))
    else:
        filter_list.append((6, cv2.imread("Masks/Orange_Left_Eye_Mask.png")[:,:,0], cv2.imread("Masks/Orange_Left_Eye.png")))
        filter_list.append((7, cv2.imread("Masks/Orange_Right_Eye_Mask.png")[:, :, 0], cv2.imread("Masks/Orange_Right_Eye.png")))

    if testBoxes(boxes):
        cv2.imshow('img', target_img)
        cv2.imshow('img_pure', target_img_p)
        cv2.imwrite(args.target[:-4] + "_boxes" + args.target[-4:], target_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        temp_Img = target_img_p
        for filt in filter_list:
            filt_offx, filt_offy = getOffsets(boxes, filt[1], filt[0])
            print (filt_offx, filt_offy)
            temp_Img = seamlessCloningPoisson(filt[2], temp_Img, filt[1], filt_offx, filt_offy)
            cv2.imshow('img_filtered', temp_Img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        cv2.imshow('img_filtered', temp_Img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        name = args.target.split("/")[1]

        if filter == 1:
            cv2.imwrite("Results/" + name[:-4] + "_Dog" + name[-4:], temp_Img)
        elif filter == 2:
            cv2.imwrite("Results/" + name[:-4] + "_Cat" + name[-4:], temp_Img)
        elif filter == 3:
            cv2.imwrite("Results/" + name[:-4] + "_Eyes" + name[-4:], temp_Img)
        elif filter == 4:
            cv2.imwrite("Results/" + name[:-4] + "_Joker" + name[-4:], temp_Img)
        else:
            cv2.imwrite("Results/" + name[:-4] + "_Anime" + name[-4:], temp_Img)
        return
    else:
        return


if __name__ == "__main__":
    main()