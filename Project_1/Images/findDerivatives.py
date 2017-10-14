'''
  File name: findDerivatives.py
  Author: Tarmily Wen
  Date created: Wednesday Sept. 20, 2017
'''

import numpy as np
from scipy import signal
import utils
from PIL import Image
import matplotlib.pyplot as plt

'''
  File clarification:
    Compute gradient put ginformation of the inrayscale image
    - Input I_gray: H x W matrix as image
    - Output Mag: H x W matrix represents the magnitude of derivatives
    - Output Magx: H x W matrix represents the magnitude of derivatives along x-axis
    - Output Magy: H x W matrix represents the magnitude of derivatives along y-axis
    - Output Ori: H x W matrix represents the orientation of derivatives
'''

def findDerivatives(I_gray):
    gaussian = np.array([[2, 4, 5, 4, 2], [4, 9, 12, 9, 4], [5, 12, 15, 12, 5], [4, 9, 12, 9, 4], [2, 4, 5, 4, 2]]) / 159.0
    dx = np.asarray([[-1.0, 0.0, 1.0], [-2.0, 0.0, 2.0], [-1.0, 0.0, 1.0]])
    dy = np.asarray([[1.0, 2.0, 1.0], [0.0, 0.0, 0.0], [-1.0, -2.0, -1.0]])

    Gx = signal.convolve2d(gaussian, dx, mode="same", boundary='fill', fillvalue=0)
    Gy = signal.convolve2d(gaussian, dy, mode="same", boundary='fill', fillvalue=0)

    Magx = signal.convolve2d(I_gray, Gx, mode="same", boundary='fill', fillvalue=0)
    Magy = signal.convolve2d(I_gray, Gy, mode="same", boundary='fill', fillvalue=0)

    Mag = np.sqrt(np.square(Magx) + np.square(Magy))

    Ori = np.arctan2(Magy, Magx)

    return Mag, Magx, Magy, Ori