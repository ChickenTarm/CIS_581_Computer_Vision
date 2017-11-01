'''
  File name: carv.py
  Author:
  Date created:
'''

import numpy as np
from cumMinEngHor import cumMinEngHor
from cumMinEngVer import cumMinEngVer
from rmHorSeam import rmHorSeam
from rmVerSeam import rmVerSeam
from genEngMap import genEngMap
import gc


def carv(I, nr, nc):
  yMax, xMax, _ = I.shape
  T = np.zeros(shape=(nr + 1, nc + 1))

  # 1 denotes a horizontal row was removed and -1 is a vertical row
  T[0][0] = 0

  intImg = [([0] * (nc + 1)) for i in range(nr + 1)]

  engMap = genEngMap(I)

  # Storing tuples of Image, Mx, Tbx, My, Tby
  fstMx, fstTbx = cumMinEngVer(engMap)
  fstMy, fstTby = cumMinEngHor(engMap)
  intImg[0][0] = (I, fstMx, fstTbx, fstMy, fstTby)

  # initialize the far left column which are deletions of only horizontal seams
  for i in range(1, nr + 1):
    # print i
    img, imgMx, imgTbx, imgMy, imgTby = intImg[i - 1][0]
    horImg, E = rmHorSeam(img, imgMy, imgTby)
    horEng = genEngMap(horImg)
    horMx, horTbx = cumMinEngVer(horEng)
    horMy, horTby = cumMinEngHor(horEng)
    intImg[i][0] = (horImg, horMx, horTbx, horMy, horTby)
    T[i][0] = T[i - 1][0] + E

  for j in range(1, nc + 1):
    img, imgMx, imgTbx, imgMy, imgTby = intImg[0][j - 1]
    vertImg, E = rmVerSeam(img, imgMx, imgTbx)
    vertEng = genEngMap(vertImg)
    vertMx, vertTbx = cumMinEngVer(vertEng)
    vertMy, vertTby = cumMinEngHor(vertEng)
    intImg[0][j] = (vertImg, vertMx, vertTbx, vertMy, vertTby)
    T[0][j] = T[0][j - 1] + E

  del fstMx
  del fstTbx
  del fstMy
  del fstTby
  intImg[0][0] = I

  for y in range(1, nr + 1):
    for x in range(1, nc + 1):
      abvImg, abvMx, abvTbx, abvMy, abvTby = intImg[y - 1][x]
      lftImg, lftMx, lftTbx, lftMy, lftTby = intImg[y][x - 1]
      abvImgDelHor, horCost = rmHorSeam(abvImg, abvMy, abvTby)
      lftImgDelVert, vertCost = rmVerSeam(lftImg, lftMx, lftTbx)
      tHorCost = horCost + T[y - 1][x]
      tVertCost = vertCost + T[y][x - 1]
      if tHorCost < tVertCost:
        horEng = genEngMap(abvImgDelHor)
        nImgMx, nImgTbx = cumMinEngVer(horEng)
        nImgMy, nImgTby = cumMinEngHor(horEng)
        intImg[y][x] = (abvImgDelHor, nImgMx, nImgTbx, nImgMy, nImgTby)
        T[y][x] = tHorCost
      else:
        vertEng = genEngMap(lftImgDelVert)
        nImgMx, nImgTbx = cumMinEngVer(vertEng)
        nImgMy, nImgTby = cumMinEngHor(vertEng)
        intImg[y][x] = (lftImgDelVert, nImgMx, nImgTbx, nImgMy, nImgTby)
        T[y][x] = tVertCost
      del abvMx
      del abvTbx
      del abvMy
      del abvTby
      del abvImg
      intImg[y - 1][x] = 0
      gc.collect()
    lftImg, lftMx, lftTbx, lftMy, lftTby = intImg[y][0]
    del lftMx
    del lftTbx
    del lftMy
    del lftTby
    del lftImg
    intImg[y][0] = 0
    gc.collect()

  for x in range(1, nc):
    lftImg, lftMx, lftTbx, lftMy, lftTby = intImg[-1][x]
    del lftMx
    del lftTbx
    del lftMy
    del lftTby
    del lftImg
    intImg[-1][x] = 0
    gc.collect()

  intImg[-1][-1] = intImg[-1][-1][0]

  Ic = intImg[-1][-1]

  return Ic, T
