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
from PIL import Image
from scipy import misc

def getColor(img1, img2):
  return


def morph_tri(im1, im2, im1_pts, im2_pts, warp_frac, dissolve_frac):
  # TODO: Your code here
  # Tips: use Delaunay() function to get Delaunay triangulation;
  # Tips: use tri.find_simplex(pts) to find the triangulation index that pts locates in.

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
    print ("frame: " + str(i))
    warp = warp_frac[i]
    int_pts = (1 - warp) * im1_pts + warp * im2_pts
    int_tri = Delaunay(int_pts)
    int_tri.simplices = tri.simplices.copy()

    tri_mat = []
    for t in tri.simplices:
      p1 = int_pts[[t[0]]]
      p2 = int_pts[[t[1]]]
      p3 = int_pts[[t[2]]]
      A = np.matrix([[p1[0][0], p2[0][0], p3[0][0]], [p1[0][1], p2[0][1], p3[0][1]], [1, 1, 1]])
      tri_mat.append(A.I)

    int_img = im2.copy()

    print "start dissolve"

    for y in range(0, yMax):
      for x in range(0, xMax):
        inTri = tri.find_simplex([x, y])
        bary = np.dot(tri_mat[inTri], [[x], [y], [1]])

        t1 = img1_tri.simplices[inTri]
        p11 = im1_pts[[t1[0]]]
        p12 = im1_pts[[t1[1]]]
        p13 = im1_pts[[t1[2]]]
        t1_mat = np.matrix([[p11[0][0], p12[0][0], p13[0][0]], [p11[0][1], p12[0][1], p13[0][1]], [1, 1, 1]])

        t2 = img2_tri.simplices[inTri]
        p21 = im2_pts[[t2[0]]]
        p22 = im2_pts[[t2[1]]]
        p23 = im2_pts[[t2[2]]]
        t2_mat = np.matrix([[p21[0][0], p22[0][0], p23[0][0]], [p21[0][1], p22[0][1], p23[0][1]], [1, 1, 1]])

        coord1 = np.dot(t1_mat, bary)
        coord2 = np.dot(t2_mat, bary)

        x1 = min(int(round(coord1[0])), xMax - 1)
        y1 = min(int(round(coord1[1])), yMax - 1)

        x2 = min(int(round(coord2[0])), xMax - 1)
        y2 = min(int(round(coord2[1])), yMax - 1)

        c1 = im1[y1][x1]
        c2 = im2[y2][x2]

        dis = dissolve_frac[i]

        int_c = (1 - dis) * c1 + dis * c2
        np.rint(int_c)

        int_img[y][x] = int_c

    images.append(int_img)
    misc.imsave("frame_" + str(i) + ".png", int_img)

  return np.asarray(images)

# warp = np.array(range(0, 61), dtype=float)
# warp = warp / (len(warp) - 1)
#
# morph_tri(np.asarray(Image.open("kb_interview.jpg")), np.asarray(Image.open("kb_vm.jpg")), np.loadtxt("kb1pts.csv"), np.loadtxt("kb2pts.csv"), warp, warp)
