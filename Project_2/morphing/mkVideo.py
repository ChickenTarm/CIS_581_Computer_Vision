'''
  File name: mkVideo.py
  Author:
  Date created:
'''

import imageio
from morph_tri import morph_tri
from PIL import Image
import numpy as np

def mkVideo(frames, fDuration):
    imageio.mimsave('result.gif', frames, format='MP4', duration=fDuration)
#
# warp = [i / 60.0 for i in range(0, 61)]
#
# mkVideo(morph_tri(np.asarray(Image.open("kb_interview.jpg")), np.asarray(Image.open("kb_vm.jpg")), np.genfromtxt('kb1pts.csv', delimiter=','), np.genfromtxt('kb2pts.csv', delimiter=','), warp, warp), 1/45.0)