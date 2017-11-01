'''
  File name: cumMinEngHor.py
  Author:
  Date created:
'''

import numpy as np


def cumMinEngHor(e):
  yMax, xMax = e.shape
  My = np.zeros(shape=(yMax, xMax))
  Tby = np.zeros(shape=(yMax, xMax), dtype=int)

  My[:, 0] = e[:, 0]

  for x in range(1, xMax):
    for y in range(0, yMax):
      if y == 0:
         parents = [float("inf"), My[y][x - 1], My[y + 1][x - 1]]
      elif y == yMax - 1:
        parents = [My[y - 1][x - 1], My[y][x - 1], float("inf")]
      else:
        parents = [My[y - 1][x - 1], My[y][x - 1], My[y + 1][x - 1]]

      cheap = parents.index(min(parents))

      My[y][x] = parents[cheap] + e[y][x]

      if cheap == 0:
        Tby[y][x] = -1
      elif cheap == 1:
        Tby[y][x] = 0
      else:
        Tby[y][x] = 1

  return My, Tby