'''
  File name: edgeLink.py
  Author: Tarmily Wen
  Date created: Sunday Sept. 24, 2017
'''

import numpy as np

'''
  File clarification:
    Use hysteresis to link edges based on high and low magnitude thresholds
    - Input M: H x W logical map after non-max suppression
    - Input Mag: H x W matrix represents the magnitude of gradient
    - Input Ori: H x W matrix represents the orientation of gradient
    - Output E: H x W binary matrix represents the final canny edge detection map
'''

# Recursive link broke the stack but for proof of concept here it is
def link (ys,xs, lowT, M, O, Edge, binary, ysMax, xsMax):
    angle = abs(np.degrees(O[curY][curX]))

    perp = int(get_dir(angle))

    if perp == 0:
        (index1y, index1x) = ys, xs + 1
        (index2y, index2x) = ys, xs - 1
        if 0 <= index1y < ysMax and 0 <= index1x < xsMax and 0 <= index2y < ysMax and 0 <= index2x < xsMax:
            pixel1Val = M[ys][xs + 1]
            pixel2Val = M[ys][xs - 1]
        else:
            return
    elif perp == 45:
        (index1y, index1x) = ys - 1, xs - 1
        (index2y, index2x) = ys + 1, xs + 1
        if 0 <= index1y < ysMax and 0 <= index1x < xsMax and 0 <= index2y < ysMax and 0 <= index2x < xsMax:
            pixel1Val = M[ys - 1][xs + 1]
            pixel2Val = M[ys + 1][xs - 1]
        else:
            return
    elif perp == 90:
        (index1y, index1x) = ys - 1, xs
        (index2y, index2x) = ys + 1, xs
        if 0 <= index1y < ysMax and 0 <= index1x < xsMax and 0 <= index2y < ysMax and 0 <= index2x < xsMax:
            pixel1Val = M[ys - 1][xs]
            pixel2Val = M[ys + 1][xs]
        else:
            return
    elif perp == 135:
        (index1y, index1x) = ys - 1, xs - 1
        (index2y, index2x) = ys + 1, xs + 1
        if 0 <= index1y < ysMax and 0 <= index1x < xsMax and 0 <= index2y < ysMax and 0 <= index2x < xsMax:
            pixel1Val = M[ys - 1][xs - 1]
            pixel2Val = M[ys + 1][xs + 1]
        else:
            return
    else:
        (index1y, index1x) = ys, xs - 1
        (index2y, index2x) = ys, xs + 1
        if 0 <= index1y < ysMax and 0 <= index1x < xsMax and 0 <= index2y < ysMax and 0 <= index2x < xsMax:
            pixel1Val = M[ys][xs - 1]
            pixel2Val = M[ys][xs + 1]
        else:
            return

    if pixel1Val > lowT and Edge[index1y][index1x] == 0 and binary[index1y][index1x] == 1:
        Edge[index1y][index1x] = 1
        link(index1y, index1x, lowT, M, O, Edge, ysMax, xsMax)
    if pixel2Val > lowT and Edge[index2y][index2x] == 0 and binary[index2y][index2x] == 1:
        Edge[index2y][index2x] = 1
        link(index2y, index2x, lowT, M, O, Edge, ysMax, xsMax)
    return


def linkl(ys,xs, lowT, M, O, Edge, binary, ysMax, xsMax):
    deadend = False
    curY = ys
    curX = xs
    while(not deadend):
        angle = abs(np.degrees(O[curY][curX]))

        perp = int(get_dir(angle))

        if perp == 0:
            (indy, indx) = curY, curX - 1
            if 0 <= indy < ysMax and 0 <= indx < xsMax:
                pixelVal = M[indy][indx]
            else:
                deadend = True
                continue
        elif perp == 45:
            (indy, indx) = curY + 1, curX - 1
            if 0 <= indy < ysMax and 0 <= indx < xsMax:
                pixelVal = M[indy][indx]
            else:
                deadend = True
                continue
        elif perp == 90:
            (indy, indx) = curY + 1, curX
            if 0 <= indy < ysMax and 0 <= indx < xsMax:
                pixelVal = M[indy][indx]
            else:
                deadend = True
                continue
        elif perp == 135:
            (indy, indx) = curY - 1, curX - 1
            if 0 <= indy < ysMax and 0 <= indx < xsMax:
                pixelVal = M[indy][indx]
            else:
                deadend = True
                continue
        else:
            (indy, indx) = curY, curX - 1
            if 0 <= indy < ysMax and 0 <= indx < xsMax:
                pixelVal = M[indy][indx]
            else:
                deadend = True
                continue
        if pixelVal > lowT and Edge[indy][indx] == 0 and binary[indy][indx] == 1:
            Edge[indy][indx] = 1
            curX = indx
            curY = indy
        else:
            deadend = True
            continue
    return


def linkr(ys,xs, lowT, M, O, Edge, binary, ysMax, xsMax):
    deadend = False
    curY = ys
    curX = xs
    while(not deadend):
        angle = abs(np.degrees(O[curY][curX]))

        perp = int(get_dir(angle))

        if perp == 0:
            (indy, indx) = curY, curX + 1
            if 0 <= indy < ysMax and 0 <= indx < xsMax:
                pixelVal = M[indy][indx]
            else:
                deadend = True
                continue
        elif perp == 45:
            (indy, indx) = curY - 1, curX + 1
            if 0 <= indy < ysMax and 0 <= indx < xsMax:
                pixelVal = M[indy][indx]
            else:
                deadend = True
                continue
        elif perp == 90:
            (indy, indx) = curY - 1, curX
            if 0 <= indy < ysMax and 0 <= indx < xsMax:
                pixelVal = M[indy][indx]
            else:
                deadend = True
                continue
        elif perp == 135:
            (indy, indx) = curY + 1, curX + 1
            if 0 <= indy < ysMax and 0 <= indx < xsMax:
                pixelVal = M[indy][indx]
            else:
                deadend = True
                continue
        else:
            (indy, indx) = curY, curX + 1
            if 0 <= indy < ysMax and 0 <= indx < xsMax:
                pixelVal = M[indy][indx]
            else:
                deadend = True
                continue
        if pixelVal > lowT and Edge[indy][indx] == 0 and binary[indy][indx] == 1:
            Edge[indy][indx] = 1
            curX = indx
            curY = indy
        else:
            deadend = True
            continue
    return


def get_dir(a):
    discrete = [0, 45, 90, 135, 180]
    return min(discrete, key=lambda x:abs(x-a))


def edgeLink(M, Mag, Ori):
    linked = np.copy(Mag)
    linked.fill(0)

    n6 = np.percentile(Mag, 96)
    ninty = np.percentile(Mag, 90)
    e5 = np.percentile(Mag, 85)
    e = np.percentile(Mag, 80)
    s5 = np.percentile(Mag, 75)
    s = np.percentile(Mag, 70)

    low = s

    if s < 4:
        if s5 < 4:
            if e < 4:
                if e5 < 4:
                    if ninty < 4:
                        low = n6
                    else:
                        low = ninty
                else:
                    low = e5
            else:
                low = e
        else:
            low = s5

    if low < 30:
        high = 2 * low
    else:
        high = 1.755 * low

    print((low, high))

    yMax, xMax = Mag.shape

    for y in range(1, yMax - 1):
        for x in range(1, xMax - 1):
            currentMag = Mag[y][x]

            if currentMag < low:
                linked[y][x] = 0
                continue
            if currentMag >= high and M[y][x] == 1:
                linked[y][x] = 1
                # Recursion causes a stack overflow so use while loops
                linkl(y, x, low, Mag, Ori, linked, M, yMax, xMax)
                linkr(y, x, low, Mag, Ori, linked, M, yMax, xMax)
    return linked
