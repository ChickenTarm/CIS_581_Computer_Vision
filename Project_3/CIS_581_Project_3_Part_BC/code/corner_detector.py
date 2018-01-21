
from skimage.feature import corner_harris

def corner_detector(img):

    cimg = corner_harris(img);

  # Your Code Here
    return cimg
