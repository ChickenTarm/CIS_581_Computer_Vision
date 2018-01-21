'''
  File name: ransac_est_homography.py
  Author:
  Date created:
'''

from est_homography import est_homography
import numpy as np
import math
import random

def ransac_est_homography(x1, y1, x2, y2, thresh):

    yMax, _ = x1.shape

    n1 = zip(y1.flatten(), x1.flatten())
    n2 = zip(y2.flatten(), x2.flatten())

    homos = []

    for i in range(0, 6000):
        randIdx = random.sample(range(0, yMax), 4)
        x = np.take(x1, randIdx)
        y = np.take(y1, randIdx)
        X = np.take(x2, randIdx)
        Y = np.take(y2, randIdx)
        h = np.asmatrix(est_homography(x, y, X, Y))
        inlier = np.zeros(shape=(yMax, 1))
        for j in range(0, yMax):
            ny1, nx1 = n1[j]
            ny2, nx2 = n2[j]
            n2c = np.array(np.dot(h, np.matrix([[nx1], [ny1], [1]]))).flatten()
            n2c = n2c / n2c[2]
            if math.hypot(nx2 - n2c[0], ny2 - n2c[1]) <= thresh:
                inlier[j] = 1
        ins = np.count_nonzero(inlier)
        if ins >= 14:
            homos.append((h, inlier, ins))

    homos.sort(key=lambda k: k[2], reverse=True)

    H = homos[0][0]
    inlier_ind = homos[0][1]

    return H, inlier_ind