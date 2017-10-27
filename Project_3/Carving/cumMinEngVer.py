'''
  File name: cumMinEngVer.py
  Author:
  Date created:
'''

import numpy as np


def cumMinEngVer(e):
  yMax, xMax = e.shape
  Mx = np.zeros(shape=(yMax,xMax))
  Tbx = np.zeros(shape=(yMax,xMax), dtype=int)

  Mx[0] = e[0,:]

  for y in range(1,yMax):
    for x in range(0,xMax):
      if x == 0:
         parents = [float("inf"), e[y - 1][x], e[y - 1][x + 1]]
      elif x == xMax - 1:
        parents = [e[y - 1][x - 1], e[y - 1][x], float("inf")]
      else:
        parents = [e[y - 1][x - 1], e[y - 1][x], e[y - 1][x + 1]]

      cheap = parents.index(min(parents))

      Mx[y][x] = parents[cheap] + e[y][x]

      if cheap == 0:
        Tbx[y][x] = -1
      elif cheap == 1:
        Tbx[y][x] = 0
      else:
        Tbx[y][x] = 1

  return Mx, Tbx