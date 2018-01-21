import imageio
from get_homography import get_homography
from to_mosaic import to_mosaic
from myvideomosaic import myvideomosaic
import numpy as np
from scipy import misc


def merge_consistent_video(v1, v2, v3, sn, en):
    vid1 = imageio.get_reader(v1, 'ffmpeg')
    vid2 = imageio.get_reader(v2, 'ffmpeg')
    vid3 = imageio.get_reader(v3, 'ffmpeg')

    vid1frames = []
    vid2frames = []
    vid3frames = []

    try:
        for im in vid1:
            vid1frames.append(np.asarray(im))
    except:
        pass
    try:
        for im in vid2:
            vid2frames.append(np.asarray(im))
    except:
        pass
    try:
        for im in vid3:
            vid3frames.append(np.asarray(im))
    except:
        pass

    max_frames = max(max(len(vid2frames), len(vid3frames)), len(vid1frames))

    vid1frames = vid1frames + [vid1frames[-1]] * (max_frames - len(vid1frames))
    vid2frames = vid2frames + [vid2frames[-1]] * (max_frames - len(vid2frames))
    vid3frames = vid3frames + [vid3frames[-1]] * (max_frames - len(vid3frames))

    mosaic_frames = []

    h12 = 0
    h32 = 0

    count = 0

    for i in range(sn, min(en, max_frames), 2):
        misc.imsave("vid1_" + str(i) + ".JPG", vid1frames[i])
        misc.imsave("vid2_" + str(i) + ".JPG", vid2frames[i])
        misc.imsave("vid3_" + str(i) + ".JPG", vid3frames[i])
        if count % 5 == 0:
            h12, h32 = get_homography(vid1frames[i], vid2frames[i], vid3frames[i])
        print "processing frame: " + str(i)
        mosaiced = to_mosaic([vid1frames[i], vid2frames[i], vid3frames[i]], h12, h32)
        mosaic_frames.append(mosaiced)
        misc.imsave("mosaiced_frame_" + str(i) + ".JPG", mosaiced)
        print "finished frame: " + str(i)
        count = count + 1

    myvideomosaic(mosaic_frames)

merge_consistent_video("Eng1_re.mp4", "Eng2_re.mp4", "Eng3_re.mp4", 0, 20)