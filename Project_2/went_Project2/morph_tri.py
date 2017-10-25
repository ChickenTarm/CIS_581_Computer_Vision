'''
  File name: morph_tri.py
  Author:
  Date created:
'''

'''
  File clarification:
    Image morphing via Triangulation
    - Input im1: target image
    - Input im2: source image
    - Input im1_pts: correspondences coordiantes in the target image
    - Input im2_pts: correspondences coordiantes in the source image
    - Input warp_frac: a vector contains warping parameters
    - Input dissolve_frac: a vector contains cross dissolve parameters

    - Output morphed_im: a set of morphed images obtained from different warp and dissolve parameters.
                         The size should be [number of images, image height, image Width, color channel number]
'''

from scipy.spatial import Delaunay
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
from scipy import misc


def morph_tri(im1, im2, im1_pts, im2_pts, warp_frac, dissolve_frac):

  yMax, xMax, depth = im2.shape

  avg_shape = (im1_pts + im2_pts) / 2

  tri = Delaunay(avg_shape)

  img1_tri = Delaunay(im1_pts)
  img1_tri.simplices = tri.simplices.copy()
  img2_tri = Delaunay(im2_pts)
  img2_tri.simplices = tri.simplices.copy()

  frames = len(warp_frac)

  images = []

  for i in range(0, frames):
    print "frame: " + str(i)
    warp = warp_frac[i]
    int_pts = (1 - warp) * im1_pts + warp * im2_pts
    int_tri = Delaunay(int_pts)
    int_tri.simplices = tri.simplices.copy()

    tri_mat = []
    for t in tri.simplices:
      p1 = int_tri.points[t[0]]
      p2 = int_tri.points[t[1]]
      p3 = int_tri.points[t[2]]
      A = np.matrix([[p1[0], p2[0], p3[0]], [p1[1], p2[1], p3[1]], [1, 1, 1]])
      tri_mat.append((A, A.I))

    int_img = im2.copy()

    print "start dissolving"

    for y in range(0, yMax):
      for x in range(0, xMax):
        inTri = Delaunay.find_simplex(int_tri, np.array([x,y]), bruteforce=True)
        bary = np.dot(tri_mat[inTri][1], [[x], [y], [1]])

        t1 = img1_tri.simplices[inTri]
        p11 = img1_tri.points[t1[0]]
        p12 = img1_tri.points[t1[1]]
        p13 = img1_tri.points[t1[2]]
        t1_mat = np.matrix([[p11[0], p12[0], p13[0]], [p11[1], p12[1], p13[1]], [1, 1, 1]])

        t2 = img2_tri.simplices[inTri]
        p21 = img2_tri.points[t2[0]]
        p22 = img2_tri.points[t2[1]]
        p23 = img2_tri.points[t2[2]]
        t2_mat = np.matrix([[p21[0], p22[0], p23[0]], [p21[1], p22[1], p23[1]], [1, 1, 1]])

        coord1 = np.dot(t1_mat, bary)
        coord2 = np.dot(t2_mat, bary)

        x1 = int(coord1[0])
        y1 = int(coord1[1])

        x2 = int(coord2[0])
        y2 = int(coord2[1])

        try:
          c1 = im1[y1][x1]
          c2 = im2[y2][x2]
        except:
          print "x,y: " + str((x, y))
          print "tri_mat: " + str(tri_mat[inTri])
          print "bary: " + str(bary)
          print "t1_mat: " + str(t1_mat)
          print "t2_mat: " + str(t2_mat)
          print "coord1: " + str(coord1)
          print "coord2: " + str(coord2)
          print "inTri: " + str(inTri)
          print "p11: " + str(p11)
          print "p12: " + str(p12)
          print "p13: " + str(p13)
          print "p21: " + str(p21)
          print "p22: " + str(p22)
          print "p23: " + str(p23)
          print "t1: " + str(t1)
          print "t2: " + str(t2)

        dis = dissolve_frac[i]

        int_c = (1 - dis) * c1 + dis * c2
        np.rint(int_c)

        int_img[y][x] = int_c

    images.append(int_img)

  images = np.array(images)

  return images