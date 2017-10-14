'''
  File name: helpers.py
  Author:
  Date created:
'''

import numpy as np

'''
  File clarification:
    Helpers file that contributes the project
    You can design any helper function in this file to improve algorithm
'''

def otsu(img):
    maxT = int(np.max(img))
    y, x = img.shape
    total = y * x
    tList = list(range(0, maxT))
    variance = []

    for thresh in tList:
        w0 = 0
        w1 = 0
        u0 = 0
        u1 = 0
        for i in range(0, thresh):
            w0 = w0 + (np.sum(np.logical_and(img>=i-1,img<=i))).size / total
        for j in range(thresh, maxT):
            w1 = w1 + (np.sum(np.logical_and(img>=j-1,img<=j))).size / total
        if w0 == 0 or w1 == 0:
            variance.append((thresh, 0))
            continue
        for k in range(0, thresh):
            u0 = u0 + k * ((np.sum(np.logical_and(img>=k-1,img<=k))).size / total) / w0
        for l in range(thresh, maxT):
            u1 = u1 + l * ((np.sum(np.logical_and(img>=l-1,img<=l))).size / total) / w1
        variance.append((thresh, w0 * w1 * (u0 - u1) * (u0 - u1)))

    variance.sort(key= lambda x: x[1], reverse=True)
    print(variance)





