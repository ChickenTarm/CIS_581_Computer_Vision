'''
  File name: click_correspondences.py
  Author: 
  Date created: 
'''

from matplotlib import pyplot as plt
import numpy as np
from PIL import Image

'''
  File clarification:
    Click correspondences between two images
    - Input im1: target image
    - Input im2: source image
    - Output im1_pts: correspondences coordiantes in the target image
    - Output im2_pts: correspondences coordiantes in the source image
'''

def click_correspondences(im1, im2):
  '''
    Tips:
      - use 'matplotlib.pyplot.subplot' to create a figure that shows the source and target image together
      - add arguments in the 'imshow' function for better image view
      - use function 'ginput' and click correspondences in two images in turn
      - please check the 'ginput' function documentation carefully
        + determine the number of correspondences by yourself which is the argument of 'ginput' function
        + when using ginput, left click represents selection, right click represents removing the last click
        + click points in two images in turn and once you finish it, the function is supposed to 
          return a NumPy array contains correspondences position in two images
  '''

  fig, (img1, img2) = plt.subplots(1, 2)
  img1.imshow(im1)
  img2.imshow(im2)
  img1.set_title("Image 1")
  img2.set_title("Image 2")
  pts = plt.ginput(n=200,timeout=0,show_clicks=True)
  plt.show()

  img1pts = pts[0::2]
  img2pts = pts[1::2]

  y1Max, x1Max, depth1 = im1.shape
  y2Max, x2Max, depth2 = im2.shape

  img1pts = np.append(img1pts,
    [(0, 0), (0, y1Max / 4), (0, y1Max / 2), (0, 3 * y1Max / 4), (0, y1Max),
     (x1Max / 4, y1Max), (x1Max / 2, y1Max), (3 * x1Max / 4, y1Max), (x1Max, y1Max),
     (x1Max, 3 * y1Max / 4), (x1Max, y1Max / 2), (x1Max, y1Max / 4), (x1Max, 0),
     (3 * x1Max / 4, 0), (x1Max / 2, 0), (x1Max / 4, 0)], axis=0)
  img2pts = np.append(img2pts,
    [(0, 0), (0, y2Max / 4), (0, y2Max / 2), (0, 3 * y2Max / 4), (0, y2Max),
     (x2Max / 4, y2Max), (x2Max / 2, y2Max), (3 * x2Max / 4, y2Max), (x2Max, y2Max),
     (x2Max, 3 * y2Max / 4), (x2Max, y2Max / 2), (x2Max, y2Max / 4), (x2Max, 0),
     (3 * x2Max / 4, 0), (x2Max / 2, 0), (x2Max / 4, 0)], axis=0)

  np.savetxt("im1pts.csv",img1pts)
  np.savetxt("im2pts.csv", img2pts)
  
  return img1pts, img2pts

# click_correspondences(np.asarray(Image.open("kb_interview.jpg")), np.asarray(Image.open("kb_vm.jpg")))