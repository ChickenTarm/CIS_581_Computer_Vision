
from corner_detector import corner_detector
from anms import anms
from feat_desc import feat_desc
from feat_match import feat_match
from ransac_est_homography import ransac_est_homography
import TWanms
from matplotlib import pyplot as plt
from PIL import Image
import numpy as np
np.set_printoptions(threshold=np.nan)
from skimage import color
from skimage import io
import scipy.misc
from matplotlib import pyplot as plt
from matplotlib import image as mpimg
import time


if __name__ == "__main__":


    img1 = Image.open('vid1_0.JPG').convert('L')
    img1.save('greyscale.png')
    I1 = np.asarray(img1, dtype=np.uint8)
    # print I
    cimg1 = corner_detector(I1);
    cimg1 = np.asarray(cimg1)
    # print cimg
    print "image1"
    print cimg1.shape

    # im1fx, im1fy, r1max = anms(cimg1, 10)

    im1fxt, im1fyt, r1maxt = TWanms.anms(cimg1, 600)

    scipy.misc.imsave('outfile.jpg', cimg1)

    img2 = Image.open('vid2_0.JPG').convert('L')
    I2 = np.asarray(img2, dtype=np.uint8)
    # print I
    cimg2 = corner_detector(I2);
    cimg2 = np.asmatrix(cimg2)
    # print cimg
    im2fx, im2fy, r2max = TWanms.anms(cimg2, 600)

    print im2fx.shape
    print im2fy.shape

    im1fdes = feat_desc(I1, im1fxt, im1fyt)

    im2fdes = feat_desc(I2, im2fx, im2fy)

    print im2fdes.shape

    fmatches = feat_match(im1fdes, im2fdes)

    print "\n\n\n Matches"

    # print fmatches

    result1 = ""
    result2 = ""

    for i in range(0, len(fmatches)):
        coord2 = int(fmatches[i][0])
        if coord2 > -1:
            result1 +=str((np.array(im1fyt[i]).flatten()[0], np.array(im1fxt[i]).flatten()[0])).strip('()')+ "\n"
            result2 += str((np.array(im2fy[coord2]).flatten()[0], np.array(im2fx[coord2]).flatten()[0])).strip('()')+ "\n"

    result1 = result1.replace(', ', ',')
    result2 = result2.replace(', ', ',')
    f = open('points1.dat','w')
    f.write(result1)
    f.close()

    f = open('points2.dat','w')
    f.write(result2)
    f.close()

    x1 = []
    y1 = []
    x2 = []
    y2 = []

    for i in range(0, len(fmatches)):
        coord2 = int(fmatches[i][0])
        if coord2 > -1:
            print str((np.array(im1fyt[i]).flatten()[0], np.array(im1fxt[i]).flatten()[0])) + " matches " + str((np.array(im2fy[coord2]).flatten()[0], np.array(im2fx[coord2]).flatten()[0]))
            x1.append(np.array(im1fxt[i]).flatten()[0])
            y1.append(np.array(im1fyt[i]).flatten()[0])
            x2.append(np.array(im2fx[coord2]).flatten()[0])
            y2.append(np.array(im2fy[coord2]).flatten()[0])

    x1 = np.reshape(np.array(x1), newshape=(len(x1), 1))
    y1 = np.reshape(np.array(y1), newshape=(len(y1), 1))
    x2 = np.reshape(np.array(x2), newshape=(len(x2), 1))
    y2 = np.reshape(np.array(y2), newshape=(len(y2), 1))

    plt.imshow(mpimg.imread("vid1_0.JPG"))
    plt.scatter(im1fxt.flatten(), im1fyt.flatten())

    plt.figure()
    plt.imshow(mpimg.imread("vid2_0.JPG"))
    plt.scatter(im2fx, im2fy)
    plt.show()

    ransac_est_homography(x1, y1, x2, y2, 4)