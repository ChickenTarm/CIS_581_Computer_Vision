'''
  File name: morph_face.py
  Author: Tarmily Wen
  Date created:
'''

import cv2
import numpy as np
from scipy.spatial import Delaunay
import itertools
from scipy import misc
from PIL import Image
from matplotlib import pyplot as plt

def morph_face(src_face, src_pts, tgt_pts, tgt_width, tgt_height):
    src_y, src_x, _ = src_face.shape
    if not src_x == tgt_width and not src_y == tgt_height:
        adjusted_face = cv2.resize(src_face, (tgt_width, tgt_height), interpolation = cv2.INTER_NEAREST)
        adjusted_pts = np.copy(src_pts)
        adjusted_pts[:, 0] = adjusted_pts[:, 0] * float(tgt_width) / float(src_x)
        adjusted_pts[:, 1] = adjusted_pts[:, 1] * float(tgt_height) / float(src_y)
        adjusted_pts = np.rint(adjusted_pts).astype(dtype=int)
    else:
        adjusted_face = np.copy(src_face)
        adjusted_pts = np.copy(src_pts)
    s_pts = np.append(adjusted_pts, [[0, 0], [tgt_width - 1, 0], [tgt_width - 1, tgt_height - 1], [0, tgt_height - 1]], axis=0)
    t_pts = np.append(tgt_pts, [[0, 0], [tgt_width - 1, 0], [tgt_width - 1, tgt_height - 1], [0, tgt_height - 1]], axis=0)
    avg_shape = (s_pts + t_pts) / 2.0

    tri = Delaunay(avg_shape)

    src_tri = Delaunay(s_pts)
    src_tri.simplices = tri.simplices.copy()
    tgt_tri = Delaunay(t_pts)
    tgt_tri.simplices = tri.simplices.copy()

    morphed_face = np.empty(shape=(tgt_height, tgt_width, 3))

    src_mat = []

    for t in tri.simplices:
        p1 = src_tri.points[t[0]]
        p2 = src_tri.points[t[1]]
        p3 = src_tri.points[t[2]]
        A = np.matrix([[p1[0], p2[0], p3[0]], [p1[1], p2[1], p3[1]], [1, 1, 1]])
        src_mat.append(A)

    tri_mat = []
    for t in tri.simplices:
        p1 = tgt_tri.points[t[0]]
        p2 = tgt_tri.points[t[1]]
        p3 = tgt_tri.points[t[2]]
        A = np.matrix([[p1[0], p2[0], p3[0]], [p1[1], p2[1], p3[1]], [1, 1, 1]])
        tri_mat.append((A, A.I))

    y = np.arange(0, tgt_height)
    x = np.arange(0, tgt_width)
    points = np.array(list(itertools.product(x, y)))
    one_column = np.ones(points.shape[0])[np.newaxis].T
    points_homo = np.transpose(np.hstack((points, one_column)), axes=(1, 0))
    inTri = Delaunay.find_simplex(tgt_tri, points, bruteforce=True)

    count = 0

    for t in tri.simplices:
        indices = np.where(inTri == count)[0]
        tri_bary = np.dot(tri_mat[count][1], np.take(points_homo, indices=indices, axis=1))
        src_pixels = np.array(np.rint(np.dot(src_mat[count], tri_bary)[0:2,:]).astype(dtype=int).T)
        tgt_pixels = np.take(points, indices=indices, axis=0)
        morphed_face[tgt_pixels[:, 1], tgt_pixels[:, 0]] = adjusted_face[src_pixels[:, 1], src_pixels[:, 0]]
        count = count + 1

    # plt.imshow(morphed_face)
    # plt.show()

    # misc.imsave("morphed_face.png", morphed_face)
    return morphed_face

# morph_face(np.asarray(Image.open("./Faces/Marq.png")), np.asarray(Image.open("./Faces/Marq.png")), np.loadtxt("./Faces/Marq.csv"), np.loadtxt("./Faces/Smile.csv"), 1000, 667)