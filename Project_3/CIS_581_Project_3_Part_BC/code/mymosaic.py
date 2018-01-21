'''
  File name: mymosaic.py
  Author:
  Date created:
'''

import numpy as np
from scipy import misc
from get_homography import get_homography
from to_mosaic import to_mosaic
from extract_frames import extract_frames


def mymosaic(img_input):

    numFrames = len(img_input)

    h12 = 0
    h32 = 0

    count = 0

    mosaic_frames = []

    for i in range(0, numFrames):
        v1 = img_input[i][0]
        v2 = img_input[i][1]
        v3 = img_input[i][2]
        if count % 5 == 0:
            h12, h32 = get_homography(v1, v2, v3)
        print "processing frame: " + str(i)
        mosaiced = to_mosaic([v1, v2, v3], h12, h32)
        mosaic_frames.append(mosaiced)
        print "finished frame: " + str(i)
        count = count + 1

    final_frames = np.array(mosaic_frames)

    return final_frames

mymosaic(extract_frames("Video1.mp4", "Video2.mp4", "Video3.mp4"))
# mymosaic(extract_frames("Eng1_re.mp4", "Eng2_re.mp4", "Eng3_re.mp4"))