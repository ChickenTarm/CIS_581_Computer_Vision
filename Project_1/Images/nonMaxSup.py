'''
  File name: nonMaxSup.py
  Author: Tarmily Wen
  Date created: Wednesday Sept. 20, 2017
'''

import numpy as np

'''
  File clarification:
    Find local maximum edge pixel using NMS along the line of the gradient
    - Input Mag: H x W matrix represents the magnitude of derivatives
    - Input Ori: H x W matrix represents the orientation of derivatives
    - Output M: H x W binary matrix represents the edge map after non-maximum suppression
'''


def nonMaxSup(Mag, Ori):
    suppressed = np.copy(Mag)
    suppressed.fill(0)
    yMax, xMax = Mag.shape
    for y in range(1, yMax - 1):
        for x in range(1, xMax - 1):
            currentMag = Mag[y][x]

            angle = Ori[y][x]

            angleDeg = np.degrees(angle)

            discrete = [0, 45, 90, 135, 180, -45, -90, -135, -180]

            dir = min(discrete, key=lambda x:abs(x-angleDeg))

            if dir == 0 or dir == -180 or dir == 180:
                (index1y, index1x) = y, x + 1
                (index2y, index2x) = y, x - 1
            elif dir == 45 or dir == -135:
                (index1y, index1x) = y - 1, x + 1
                (index2y, index2x) = y + 1, x - 1
            elif dir == 90 or dir == -90:
                (index1y, index1x) = y - 1, x
                (index2y, index2x) = y + 1, x
            else:
                (index1y, index1x) = y - 1, x - 1
                (index2y, index2x) = y + 1, x + 1

            newX = np.cos(angle)
            newY = np.sin(angle)

            # Quadrants for interpolation: creates a bounding box going through the center of each neighboring pixel
            if newX >= 0 and newY >= 0:
                if angle > np.pi / 4.0:

                    weight = 1.0 / abs(np.tan(angle))
                    pixel1Val = weight * Mag[y-1][x+1] + (1 - weight) * Mag[y-1][x]
                    pixel2Val = weight * Mag[y+1][x-1] + (1 - weight) * Mag[y+1][x]
                else:
                    weight = abs(np.tan(angle))
                    pixel1Val = weight * Mag[y-1][x+1] + (1 - weight) * Mag[y][x+1]
                    pixel2Val = weight * Mag[y+1][x-1] + (1 - weight) * Mag[y][x-1]
            elif newX <= 0 and newY >= 0:
                if angle < 3.0 * np.pi / 4.0:
                    weight = 1.0 / abs(np.tan(angle))
                    pixel1Val = weight * Mag[y-1][x-1] + (1 - weight) * Mag[y-1][x]
                    pixel2Val = weight * Mag[y+1][x+1] + (1 - weight) * Mag[y+1][x]
                else:
                    weight = abs(np.tan(angle))
                    pixel1Val = weight * Mag[y-1][x-1] + (1 - weight) * Mag[y][x-1]
                    pixel2Val = weight * Mag[y+1][x+1] + (1 - weight) * Mag[y][x+1]
            elif newX <= 0 and newY <= 0:
                if angle < -3.0 * np.pi / 4.0:
                    weight = abs(np.tan(angle))
                    pixel1Val = weight * Mag[y+1][x-1] + (1 - weight) * Mag[y][x-1]
                    pixel2Val = weight * Mag[y-1][x+1] + (1 - weight) * Mag[y][x+1]
                else:
                    weight = 1.0 / abs(np.tan(angle))
                    pixel1Val = weight * Mag[y+1][x-1] + (1 - weight) * Mag[y+1][x]
                    pixel2Val = weight * Mag[y-1][x+1] + (1 - weight) * Mag[y-1][x]
            else:
                if angle < -1 * (np.pi / 4.0):
                    weight = 1.0 / abs(np.tan(angle))
                    pixel1Val = weight * Mag[y+1][x+1] + (1 - weight) * Mag[y+1][x]
                    pixel2Val = weight * Mag[y-1][x-1] + (1 - weight) * Mag[y-1][x]
                else:
                    weight = abs(np.tan(angle))
                    pixel1Val = weight * Mag[y+1][x+1] + (1 - weight) * Mag[y][x+1]
                    pixel2Val = weight * Mag[y-1][x-1] + (1 - weight) * Mag[y][x-1]

            if currentMag >= pixel2Val and currentMag >= pixel1Val and suppressed[index1y][index1x] == 0 and suppressed[index2y][index2x] == 0:
                suppressed[y][x] = 1
    return suppressed

