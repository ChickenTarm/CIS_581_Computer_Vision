'''
  File name: eval_morphing_project2.py
  Author: Haoyuan(Steve) Zhang
  Date created: 13/10/2017
'''

'''
  File clarification:
    check the accuracy of your image morphing implementation
'''

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import imageio

from morph_tri import *


def main():
    test_img = "project2_testimg.png"
    im_cur = np.array(Image.open(test_img).convert('RGB'))

    # create correspondences
    p1 = np.array([[0, 0], [256, 0], [0, 256], [256, 256], [128, 128]])
    p2 = np.zeros([5, 5, 2])
    p2[0, :, :] = np.array([[0, 0], [256, 0], [0, 256], [256, 256], [128, 32]])
    p2[1, :, :] = np.array([[0, 0], [256, 0], [0, 256], [256, 256], [32, 128]])
    p2[2, :, :] = np.array([[0, 0], [256, 0], [0, 256], [256, 256], [128, 222]])
    p2[3, :, :] = np.array([[0, 0], [256, 0], [0, 256], [256, 256], [222, 128]])
    p2[4, :, :] = np.array([[0, 0], [256, 0], [0, 256], [256, 256], [128, 32]])

    # create reference images
    img_ref = []
    warp_frac, dissolve_frac = np.array([1]), np.array([0])

    for i in range(5):
        morphed_cur = morph_tri(im_cur, im_cur, p1, p2[i, :, :], warp_frac, dissolve_frac)
        img_ref.append(morphed_cur[0, :, :, :])

    # morphed iteration
    w = np.arange(0, 1.1, 0.1)
    res_list = []
    for j in range(4):
        img_source = img_ref[j]
        p_source = p2[j, :, :]
        img_dest = img_ref[j + 1]
        p_dest = p2[j + 1, :, :]

        morphed_set = morph_tri(img_source, img_dest, p_source, p_dest, w, w)

        k = 0
        while k < 11:
            res_list.append(morphed_set[k, :, :, :])
            k += 1

    # generate gif file
    imageio.mimsave('./eval_testimg.gif', res_list)


if __name__ == "__main__":
    main()