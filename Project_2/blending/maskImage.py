'''
  File name: maskImage.py
  Author:
  Date created:
'''

from PIL import Image
from matplotlib import pyplot as plt
from roipoly import roipoly
import numpy as np
from scipy import misc

def maskImage(img):
    plt.imshow(img)
    plt.title("left click: line segment         right click: close region")

    # let user draw first ROI
    ROI1 = roipoly(roicolor='r')  # let user draw first ROI

    ROI1.displayROI()
    ROI1.displayMean(img)

    # plt.imshow(ROI1.getMask(img),
    #           interpolation='nearest', cmap="Greys")
    # plt.title('ROI masks of the ROI')
    # plt.show()

    mask = ROI1.getMask(img).astype(int)

    fig, ax2 = plt.subplots(1)
    ax2.imshow(mask, cmap='gray', interpolation='nearest')
    ax2.axis("off")
    ax2.set_title('Canny Edge Detection')
    plt.show()

    misc.imsave("mask.jpg", mask)

    return mask

maskImage(np.asarray(Image.open("face.jpg")))