'''
  File name: feat_desc.py
  Author:
  Date created:
'''

import numpy as np
from scipy import ndimage
import math


def getSq(img, sy, sx, w):

    window = img[int(sy):int(sy+w), int(sx):int(sx+w)]

    patch = ndimage.zoom(window, zoom=(8.0 / float(w)))

    return patch.ravel()


def feat_desc(img, x, y):

    imy, imx = img.shape

    ratio = .002

    width = int(math.ceil(math.sqrt(imy * imx * ratio)))

    padded = np.zeros(shape=(imy + width, imx + width))

    halfw = int(math.ceil(width / 2.0))

    padded[halfw: imy + halfw, halfw: imx + halfw] = img

    pts = zip(y, x)

    descs = np.zeros(shape=(64, len(pts)))

    for i in range(0, len(pts)):
        (py, px) = pts[i]
        patch = getSq(padded, py, px, width)

        pn = (patch - np.mean(patch)) / np.std(patch)

        descs[:, i] = pn

    return descs