import imageio
import numpy as np


def extract_frames(v1, v2, v3):
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

    frame_lst = []

    for i in range(0, max_frames):
        frame_lst.append([np.asarray(vid1frames[i], dtype='uint8'), np.asarray(vid2frames[i], dtype='uint8'), np.asarray(vid3frames[i], dtype='uint8')])

    ordered_frames = np.array(frame_lst)

    return ordered_frames