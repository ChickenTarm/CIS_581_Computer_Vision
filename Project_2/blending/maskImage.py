'''
  File name: maskImage.py
  Author:
  Date created:
'''

from drawMask import draw_mask
from scipy import misc

def maskImage(img):
    mask, bbox = draw_mask(img)
    misc.imsave("mask.png", mask)

    return mask