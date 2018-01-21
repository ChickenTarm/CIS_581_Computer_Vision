import imageio
from mymosaic import mymosaic
from myvideomosaic import myvideomosaic
import numpy as np
from scipy import misc


def merge_video(v1, v2, v3, sn, en):
    vid1 = imageio.get_reader(v1, 'ffmpeg')
    vid2 = imageio.get_reader(v2, 'ffmpeg')
    vid3 = imageio.get_reader(v3, 'ffmpeg')

    vid1frames = []
    vid2frames = []
    vid3frames = []

    for im in vid1:
        vid1frames.append(np.asarray(im))
    for im in vid2:
        vid2frames.append(np.asarray(im))
    for im in vid3:
        vid3frames.append(np.asarray(im))

    max_frames = max(max(len(vid2frames), len(vid3frames)), len(vid1frames))

    vid1frames = vid1frames + [vid1frames[-1]] * (max_frames - len(vid1frames))
    vid2frames = vid2frames + [vid2frames[-1]] * (max_frames - len(vid2frames))
    vid3frames = vid3frames + [vid3frames[-1]] * (max_frames - len(vid3frames))

    mosaic_frames = []

    for i in range(sn, min(en, max_frames)):
        misc.imsave("vid1_" + str(i) + ".JPG", vid1frames[i])
        misc.imsave("vid2_" + str(i) + ".JPG", vid2frames[i])
        misc.imsave("vid3_" + str(i) + ".JPG", vid3frames[i])
        # mosaiced = mymosaic([vid1frames[i], vid2frames[i], vid3frames[i]])
        # mosaic_frames.append(mosaiced)
        # misc.imsave("mosaiced_frame_" + str(i) + ".JPG", mosaiced)
        print "finished frame: " + str(i)

    # myvideomosaic(mosaic_frames)

merge_video("Video1.mp4", "Video2.mp4", "Video3.mp4", 63, 64)