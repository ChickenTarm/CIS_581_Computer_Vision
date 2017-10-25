'''
  File name: mkVideo.py
  Author:
  Date created:
'''

import imageio

def mkVideo(frames, fDuration):
    imageio.mimsave('result.gif', frames, format='GIF', duration=fDuration)