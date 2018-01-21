'''
  File name: applyGeometricTransformation.py
  Author: Tarmily Wen
  Date created:
'''

import numpy as np
from skimage import transform as tf
import math

'''
  File clarification:
    Estimate the translation for bounding box
    - Input startXs: the x coordinates for all features wrt the first frame
    - Input startYs: the y coordinates for all features wrt the first frame
    - Input newXs: the x coordinates for all features wrt the second frame
    - Input newYs: the y coordinates for all features wrt the second frame
    - Input bbox: corner coordiantes of all detected bounding boxes

    - Output Xs: the x coordinates(after eliminating outliers) for all features wrt the second frame
    - Output Ys: the y coordinates(after eliminating outliers) for all features wrt the second frame
    - Output newbbox: corner coordiantes of all detected bounding boxes after transformation
'''


def applyGeometricTransformation(startX, startY, newXs, newYs, bbox):
    bboxc = np.array(bbox)

    # print bboxc
    #
    # print zip(startX, startY)
    # print zip(newXs, newYs)

    tolerance = 15

    num_boxes = len(bboxc)
    newbbox = np.full(shape=bboxc.shape, fill_value=-1)

    try:
        feats, b = startX.shape

        sx = startX
        sy = startY

        nx = newXs
        ny = newYs

        goodX = np.full(shape=startX.shape, fill_value=-1)
        goodY = np.full(shape=startY.shape, fill_value=-1)
    except:
        feats = len(startX)

        sx = np.reshape(startX, newshape=(feats, 1))
        sy = np.reshape(startY, newshape=(feats, 1))

        nx = np.reshape(newXs, newshape=(feats, 1))
        ny = np.reshape(newYs, newshape=(feats, 1))

        goodX = np.full(shape=(feats, 1), fill_value=-1)
        goodY = np.full(shape=(feats, 1), fill_value=-1)

    max_feat = 0

    bad_feats = []

    good_feats = []

    for i in range(0, num_boxes):

        box_sx = sx[:, i]
        box_sy = sy[:, i]

        box_nx = nx[:, i]
        box_ny = ny[:, i]

        start_coord = np.array(zip(box_sx[box_nx >= 0], box_sy[box_ny >= 0]))
        end_coord = np.array(zip(box_nx[box_nx >= 0], box_ny[box_ny >= 0]))

        keepSX = []
        keepSY = []

        keepEX = []
        keepEY = []

        bad = []
        good = []

        for j in range(0, len(start_coord)):
            s = start_coord[j]
            e = end_coord[j]
            dist = math.sqrt((s[0] - e[0]) ** 2 + (s[1] - e[1]) ** 2)
            if dist < tolerance:
                good.append(j)
                keepSX.append(s[0])
                keepSY.append(s[1])
                keepEX.append(e[0])
                keepEY.append(e[1])
            else:
                bad.append(j)

        good_feats.append(good)
        bad_feats.append(bad)
        # print keepEX
        # print keepEY

        affine = tf.SimilarityTransform()
        try:
            estimate = affine.estimate(np.array(zip(keepSX, keepSY)), np.array(zip(keepEX, keepEY)))
            # print estimate

            if estimate:
                nbox = affine(bboxc[i])
            else:
                nbox = bboxc[i]
        except:
            nbox = bboxc[i]
            # print zip(keepSX, keepSY)
            # print zip(keepEX, keepEY)

        if len(keepEX) > max_feat:
            max_feat = len(keepEX)

        keepX = np.array(keepEX)
        keepY = np.array(keepEY)

        goodX[0:len(keepX), i] = keepX
        goodY[0:len(keepY), i] = keepY

        newbbox[i] = nbox

    Xs = goodX[0:max_feat, :]
    Ys = goodY[0:max_feat, :]

    # print Xs.shape
    # print Ys.shape

    # print [item for sublist in Xs for item in sublist]
    # print [item for sublist in Ys for item in sublist]


    # for i in range(0, len(good_feats)):
    #     print "face " + str(i)
    #     s_good = zip(sx[:, i], sy[:, i])
    #     n_good = zip(nx[:, i], ny[:, i])
    #     gl = good_feats[i]
    #     print "start"
    #     for ind in gl:
    #         print "feature " + str(ind)
    #         print str(s_good[ind]) + " -> " + str(n_good[ind]) + " is good"
    #     print "\n\n"
    #
    #
    # for i in range(0, len(bad_feats)):
    #     print "face " + str(i)
    #     s_bad = zip(sx[:, i], sy[:, i])
    #     n_bad = zip(nx[:, i], ny[:, i])
    #     bl = bad_feats[i]
    #     for ind in bl:
    #         print "feature " + str(ind)
    #         print str(s_bad[ind]) + " -> " + str(n_bad[ind]) + " is bad"
    #     print "\n\n"

    return Xs, Ys, newbbox.tolist()