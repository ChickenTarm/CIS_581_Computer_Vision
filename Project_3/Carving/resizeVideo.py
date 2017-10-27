'''
  File name: resizeVideo.py
  Author:
  Date created:
'''

import numpy as np
from cumMinEngHor import cumMinEngHor
from cumMinEngVer import cumMinEngVer
from rmHorSeam import rmHorSeam
from rmVerSeam import rmVerSeam
from genEngMap import genEngMap
from PIL import Image
import imageio

def getSeq(seq, map, y, x):
    if y == 0 and x == 0:
        return
    dir = map[y][x]
    seq.append(dir)
    if dir == -1:
        getSeq(seq, map, y, x - 1)
    if dir == 1:
        getSeq(seq, map, y - 1, x)


def fillFrames(frames, directions, imgs, count, maxF, y, x, h, w):
    if count == maxF:
        return
    im, _, _, _ , _, = imgs[y][x]
    ch, cx, _ = im.shape
    frm = np.zeros(shape=(h, w, 3))
    frm[0 : ch, 0 : cx, :] = im
    np.clip(frm, 0, 255, out=frm)
    frmRBG = frm.astype('uint8')
    frames.append(frmRBG)
    direct = directions[count]
    if direct == -1:
        fillFrames(frames, directions, imgs, count + 1, maxF, y, x + 1, h, w)
    else:
        fillFrames(frames, directions, imgs, count + 1, maxF, y + 1, x, h, w)


def mkVid (I, nr, nc):
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
    # print imgTby[26][999]
    horImg, E = rmHorSeam(img, imgMy, imgTby)
    horEng = genEngMap(horImg)
    horMx, horTbx = cumMinEngVer(horEng)
    horMy, horTby = cumMinEngHor(horEng)
    intImg[i][0] = (horImg, horMx, horTbx, horMy, horTby)
    T[i][0] = 1

  for j in range(1, nc + 1):
    img, imgMx, imgTbx, imgMy, imgTby = intImg[0][j - 1]
    vertImg, E = rmVerSeam(img, imgMx, imgTbx)
    vertEng = genEngMap(vertImg)
    vertMx, vertTbx = cumMinEngVer(vertEng)
    vertMy, vertTby = cumMinEngHor(vertEng)
    intImg[0][j] = (vertImg, vertMx, vertTbx, vertMy, vertTby)
    T[0][j] = -1

  for y in range(1, nr + 1):
    for x in range(1, nc + 1):
      abvImg, abvMx, abvTbx, abvMy, abvTby = intImg[y - 1][x]
      lftImg, lftMx, lftTbx, lftMy, lftTby = intImg[y][x - 1]
      abvImgDelHor, horCost = rmHorSeam(abvImg, abvMy, abvTby)
      lftImgDelVert, vertCost = rmVerSeam(lftImg, lftMx, lftTbx)
      if horCost < vertCost:
        horEng = genEngMap(abvImgDelHor)
        nImgMx, nImgTbx = cumMinEngVer(horEng)
        nImgMy, nImgTby = cumMinEngHor(horEng)
        intImg[y][x] = (abvImgDelHor, nImgMx, nImgTbx, nImgMy, nImgTby)
        T[y][x] = 1
      else:
        vertEng = genEngMap(lftImgDelVert)
        nImgMx, nImgTbx = cumMinEngVer(vertEng)
        nImgMy, nImgTby = cumMinEngHor(vertEng)
        intImg[y][x] = (lftImgDelVert, nImgMx, nImgTbx, nImgMy, nImgTby)
        T[y][x] = -1

  directions = []

  getSeq(directions, T, nc, nr)

  directions = list(reversed(directions))

  print directions

  frameImg = []

  print len(directions)

  fillFrames(frameImg, directions, intImg, 0, len(directions), 0, 0, yMax, xMax)

  print len(frameImg)

  imageio.mimsave('result.gif', frameImg, format='GIF', duration=1 / 30)


mkVid(np.asarray(Image.open("tower.jpg")), 50, 50)