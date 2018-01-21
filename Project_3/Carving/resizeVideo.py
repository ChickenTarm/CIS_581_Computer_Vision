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
import gc
import scipy.misc

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
    im = imgs[y][x]
    ch, cx, _ = im.shape
    frm = np.zeros(shape=(h, w, 3))
    frm[0 : ch, 0 : cx, :] = im
    np.clip(frm, 0, 255, out=frm)
    frmRBG = frm.astype('uint8')
    frames.append(frmRBG)
    if count + 1 == maxF:
        return
    else:
        direct = directions[count + 1]
        if direct == -1:
            fillFrames(frames, directions, imgs, count + 1, maxF, y, x + 1, h, w)
        else:
            fillFrames(frames, directions, imgs, count + 1, maxF, y + 1, x, h, w)


def mkFrames(im, directions, frames):
    frames.append(im)
    final = np.zeros(shape=im.shape)
    for d in directions:
        if d == -1:
            mx, tbx = cumMinEngVer(genEngMap(frames[-1]))
            vim, e = rmVerSeam(frames[-1], mx, tbx)
            frames.append(vim)
            final = vim
        else:
            my, tby = cumMinEngHor(genEngMap(frames[-1]))
            vim, e = rmHorSeam(frames[-1], my, tby)
            frames.append(vim)
            final = vim
    return final

def formatFrames(im, frames):
    for i in range(0, len(frames)):
        temp = np.zeros(shape=im.shape)
        ys, xs, _ = frames[i].shape
        temp[0 : ys, 0 : xs, :] = frames[i]
        np.clip(temp, 0, 255, out=temp)
        tempRBG = temp.astype('uint8')
        frames[i] = tempRBG

# Takes in the same arguments as carv in carv.py


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

    Cost = np.zeros(shape=(nr + 1, nc + 1))
    Cost[0][0] = 0

    # initialize the far left column which are deletions of only horizontal seams
    for i in range(1, nr + 1):
        img, imgMx, imgTbx, imgMy, imgTby = intImg[i - 1][0]
        horImg, E = rmHorSeam(img, imgMy, imgTby)
        horEng = genEngMap(horImg)
        horMx, horTbx = cumMinEngVer(horEng)
        horMy, horTby = cumMinEngHor(horEng)
        intImg[i][0] = (horImg, horMx, horTbx, horMy, horTby)
        Cost[i][0] = Cost[i - 1][0] + E
        T[i][0] = 1

    for j in range(1, nc + 1):
        img, imgMx, imgTbx, imgMy, imgTby = intImg[0][j - 1]
        vertImg, E = rmVerSeam(img, imgMx, imgTbx)
        vertEng = genEngMap(vertImg)
        vertMx, vertTbx = cumMinEngVer(vertEng)
        vertMy, vertTby = cumMinEngHor(vertEng)
        intImg[0][j] = (vertImg, vertMx, vertTbx, vertMy, vertTby)
        Cost[0][j] = Cost[0][j - 1] + E
        T[0][j] = -1

    del fstMx
    del fstTbx
    del fstMy
    del fstTby
    intImg[0][0] = 0

    for y in range(1, nr + 1):
        for x in range(1, nc + 1):
            print "y, x: " + str((y,x))
            abvImg, abvMx, abvTbx, abvMy, abvTby = intImg[y - 1][x]
            lftImg, lftMx, lftTbx, lftMy, lftTby = intImg[y][x - 1]
            abvImgDelHor, horCost = rmHorSeam(abvImg, abvMy, abvTby)
            lftImgDelVert, vertCost = rmVerSeam(lftImg, lftMx, lftTbx)
            tHorCost = horCost + Cost[y - 1][x]
            tVertCost = vertCost + Cost[y][x - 1]
            if tHorCost < tVertCost:
                print "del hor"
                horEng = genEngMap(abvImgDelHor)
                nImgMx, nImgTbx = cumMinEngVer(horEng)
                nImgMy, nImgTby = cumMinEngHor(horEng)
                intImg[y][x] = (abvImgDelHor, nImgMx, nImgTbx, nImgMy, nImgTby)
                Cost[y][x] = tHorCost
                T[y][x] = 1
            else:
                print "del ver"
                vertEng = genEngMap(lftImgDelVert)
                nImgMx, nImgTbx = cumMinEngVer(vertEng)
                nImgMy, nImgTby = cumMinEngHor(vertEng)
                intImg[y][x] = (lftImgDelVert, nImgMx, nImgTbx, nImgMy, nImgTby)
                Cost[y][x] = tVertCost
                T[y][x] = -1
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

    for x in range(1, nc + 1):
        lftImg, lftMx, lftTbx, lftMy, lftTby = intImg[-1][x]
        del lftMx
        del lftTbx
        del lftMy
        del lftTby
        del lftImg
        intImg[-1][x] = 0
        gc.collect()

    directions = []

    getSeq(directions, T, nc, nr)

    directions = list(reversed(directions))

    frameImg = []

    final = mkFrames(I, directions, frameImg)

    formatFrames(I, frameImg)

    imageio.mimsave('result.mp4', frameImg, format='MP4', fps=30)
    scipy.misc.imsave("result.png", final)


mkVid(np.asarray(Image.open("soccer.jpeg")), 10, 10)