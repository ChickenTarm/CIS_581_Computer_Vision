import cv2
import numpy as np
from  matplotlib import pyplot as plt

img = cv2.imread("/Users/tommylee/Documents/CIS_581/Project_1/Images/16068.jpg")
edges = cv2.Canny(img, 50,100)

plt.subplot(121),plt.imshow(img,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Open CV Image'), plt.xticks([]), plt.yticks([])
plt.show()