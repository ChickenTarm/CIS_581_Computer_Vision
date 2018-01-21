'''
  File name: feat_match.py
  Author:
  Date created:
'''

import numpy as np


def get_ssd(f1, f2):
    sum = 0
    for i in range(0, 64):
        diff = f1[i] - f2[i]
        sum = sum + (diff * diff)
    return sum


def feat_match(descs1, descs2):

    n1ton2 = {}

    yMax1, xMax1 = descs1.shape

    yMax2, xMax2 = descs2.shape

    thresh = .8

    for i in range(0, xMax1):
        diff = []
        pt1 = np.ravel(descs1[:, i])
        for j in range(0, xMax2):
            pt2 = np.ravel(descs2[:,j])
            sim = np.sum((pt1 - pt2) ** 2)
            diff.append((j, sim))
        diff.sort(key=lambda k: k[1])
        top1 = diff[0]
        top2 = diff[1]
        if top1[1] / top2[1] < thresh:
            n1ton2[i] = top1[0]
        else:
            n1ton2[i] = -1

    match = np.zeros(shape=(xMax1, 1))

    for i in range(0, len(n1ton2)):
        match[i] = n1ton2[i]

    return match
