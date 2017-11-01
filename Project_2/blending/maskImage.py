'''
  File name: maskImage.py
  Author:
  Date created:
'''

from drawMask import draw_mask
from scipy import misc
from PIL import Image
import numpy as np

def maskImage(img):
    mask, bbox = draw_mask(img)
    misc.imsave("mask.png", mask)

    return mask

maskImage(np.asarray(Image.open("Floppy_Right_Ear.png")))