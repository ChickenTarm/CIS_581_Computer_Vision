import numpy as np
from anms import anms
from corner_detector import corner_detector
from feat_desc import feat_desc
from feat_match import feat_match
from ransac_est_homography import ransac_est_homography
from skimage import color


def get_match(matches, fx1, fy1, fx2, fy2):
    x1 = []
    y1 = []
    x2 = []
    y2 = []
    for i in range(0, len(matches)):
        coord2 = int(matches[i][0])
        if coord2 > -1:
            x1.append(np.array(fx1[i]).flatten()[0])
            y1.append(np.array(fy1[i]).flatten()[0])
            x2.append(np.array(fx2[coord2]).flatten()[0])
            y2.append(np.array(fy2[coord2]).flatten()[0])
    x1 = np.reshape(np.array(x1), newshape=(len(x1), 1))
    y1 = np.reshape(np.array(y1), newshape=(len(y1), 1))
    x2 = np.reshape(np.array(x2), newshape=(len(x2), 1))
    y2 = np.reshape(np.array(y2), newshape=(len(y2), 1))
    return x1, y1, x2, y2


def get_homography(img1, img2, img3):
    I1 = color.rgb2gray(img1)
    I2 = color.rgb2gray(img2)
    I3 = color.rgb2gray(img3)


    cimg1 = np.asmatrix(corner_detector(I1))
    cimg2 = np.asmatrix(corner_detector(I2))
    cimg3 = np.asmatrix(corner_detector(I3))


    im1fx, im1fy, r1max = anms(cimg1, 800)
    im2fx, im2fy, r2max = anms(cimg2, 800)
    im3fx, im3fy, r3max = anms(cimg3, 800)


    im1fdes = feat_desc(I1, im1fx, im1fy)
    im2fdes = feat_desc(I2, im2fx, im2fy)
    im3fdes = feat_desc(I3, im3fx, im3fy)

    f12matches = feat_match(im1fdes, im2fdes)
    f32matches = feat_match(im3fdes, im2fdes)

    x12, y12, x21, y21 = get_match(f12matches, im1fx, im1fy, im2fx, im2fy)

    x32, y32, x23, y23 = get_match(f32matches, im3fx, im3fy, im2fx, im2fy)

    h12, _ = ransac_est_homography(x12, y12, x21, y21, 3)

    h32, _ = ransac_est_homography(x32, y32, x23, y23, 3)

    return h12, h32