import numpy as np
import math
from skimage.feature import corner_harris, corner_peaks


def anms(cimg, max_pts):

    thresholds = np.where(cimg > np.percentile(cimg, 99.5))

    thx = thresholds[1]
    thy = thresholds[0]

    threshFeat = np.array(zip(thy.flatten(), thx.flatten()))

    coords = []
    feature_mag = np.zeros(shape=(len(thx),))

    for i in range(0, len(thx)):
        y = threshFeat[i][0]
        x = threshFeat[i][1]
        coords.append((y,x))
        feature_mag[i] = cimg[y,x]

    feature_mag = np.array(feature_mag)

    feature_radius = []

    for i in range(0, len(thx)):
        curr_mag = feature_mag[i]
        greater = (np.where(feature_mag > curr_mag))[0]
        radi = []
        (cy, cx) = coords[i]
        for ind in greater:
            (ty, tx) = coords[ind]
            radi.append(math.hypot(cx-tx, cy-ty))
        if len(radi) == 0:
            feature_radius.append((cy, cx, float("inf")))
        else:
            radi.sort()
            feature_radius.append((cy, cx, radi[0]))

    feature_radius.sort(key=lambda k: k[2], reverse=True)

    N = min(max_pts, len(feature_radius))

    x = np.zeros(shape=(N, 1))
    y = np.zeros(shape=(N, 1))

    for i in range(0, N):
        x[i] = feature_radius[i][1]

    for i in range(0, N):
        y[i] = feature_radius[i][0]

    rmax = feature_radius[N - 1][2]

    x = x.astype(int)

    y = y.astype(int)

    return x, y, rmax