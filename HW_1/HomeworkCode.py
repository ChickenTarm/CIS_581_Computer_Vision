import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from scipy import signal
from PIL import Image

# -- Read an image --
# Attribution - Bikesgray.jpg By Davidwkennedy (http://en.wikipedia.org/wiki/File:Bikesgray.jpg) [CC BY-SA 3.0 (http://creativecommons.org/licenses/by-sa/3.0)], via Wikimedia Commons
img1 =  Image.open('Bikesgray.jpg')

# -- Display original image --
img1.show()

# -- X gradient - Sobel Operator --
f1 = np.asarray([[1, 0, -1], [2, 0, -2], [1, 0, -1]])

# -- Convolve image with kernel f1 -> This highlights the vertical edges in the image --
vertical_sobel = signal.convolve2d(img1, f1, mode='full')

# -- Display the image --
# Write code here to display the image 'vertical_sobel' (hint: use plt.imshow with a color may of gray)
plt.imshow(vertical_sobel, cmap="gray")
mpimg.imsave("Vertical_Edges.jpg", arr=vertical_sobel, cmap="gray")
plt.figure()

# -- Y gradient - Sobel Operator --
f2 =  np.asarray([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])

# -- Convolve image with kernel f2 -> This should highlight the horizontal edges in the image --
horz_sobel = signal.convolve2d(img1, f2, mode='full')

# -- Display the image --
# Write code here to display the image 'horz_sobel' (hint: use plt.imshow with a color may of gray)
plt.imshow(horz_sobel, cmap="gray")
mpimg.imsave("Horizontal_Edges.jpg", arr=horz_sobel, cmap="gray")
plt.show()