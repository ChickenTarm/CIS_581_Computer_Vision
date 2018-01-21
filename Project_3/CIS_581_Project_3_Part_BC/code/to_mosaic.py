import numpy as np
import math


def getDim(w1tl, w1tr, w1br, w1bl, otl, otr, obr, obl, w3tl, w3tr, w3br, w3bl):
    x = [w1tl[0], w1tr[0], w1br[0], w1bl[0], otl[0], otr[0], obr[0], obl[0], w3tl[0], w3tr[0], w3br[0], w3bl[0]]
    y = [w1tl[1], w1tr[1], w1br[1], w1bl[1], otl[1], otr[1], obr[1], obl[1], w3tl[1], w3tr[1], w3br[1], w3bl[1]]

    x1 = [w1tl[0], w1tr[0], w1br[0], w1bl[0]]

    min_x = min(x)
    min_y = min(y)
    max_x = max(x)
    max_y = max(y)

    return (int(math.ceil(max_y - min_y)), int(math.ceil(max_x - min_x)), 3), int(min_y), int(min_x), int(math.ceil(max(x1)))


def alpha_blend12(x, y, ox, oy, y2, img_input):
    if 0 <= x < 60 and 0 <= y < 60:
        if x < y:
            alpha = x / 60.0
        else:
            alpha = y / 60.0
    elif 0 <= x < 60 and y2 - 61 <= y < y2:
        ydist = y2 - 1 - y
        if x < ydist:
            alpha = x / 60.0
        else:
            alpha = ydist / 60.0
    elif 0 <= x < 60:
        alpha = x / 60.0
    elif 0 <= y < 60:
        alpha = y / 60.0
    else:
        ydist = y2 - 1 - y
        alpha = ydist / 60.0
    try:
        color = img_input[0][int(oy)][int(ox)] * (1 - alpha) + img_input[1][y][x] * alpha
        return np.clip(color, a_min=0, a_max=255)
    except:
        print(oy, ox)
        print(y, x)


def alpha_blend32(x, y, ox, oy, y2, x2, img_input):
    if x2 - 61 <= x < x2 and 0 <= y < 60:
        xdist = x2 - 1 - x
        if xdist < y:
            alpha = xdist / 60.0
        else:
            alpha = y / 60.0
    elif x2 - 61 <= x < x2 and y2 - 61 <= y < y2:
        xdist = x2 - 1 - x
        ydist = y2 - 1 - y
        if xdist < ydist:
            alpha = xdist / 60.0
        else:
            alpha = ydist / 60.0
    elif x2 - 61 <= x < x2:
        xdist = x2 - 1 - x
        alpha = xdist / 60.0
    elif 0 <= y < 60:
        alpha = y / 60.0
    else:
        ydist = y2 - 1 - y
        alpha = ydist / 60.0
    try:
        color = img_input[2][int(oy)][int(ox)] * (1 - alpha) + img_input[1][y][x] * alpha
        return np.clip(color, a_min=0, a_max=255)
    except:
        print(oy, ox)
        print(y, x)


def apply_homography(x, y, h):
    un_norm = np.array(np.dot(h, np.matrix([[x], [y], [1]]))).flatten()
    return un_norm / un_norm[2]


def to_mosaic(img_input, h12, h32):
    y1, x1, _ = img_input[0].shape
    y2, x2, _ = img_input[1].shape
    y3, x3, _ = img_input[2].shape

    warped_tl1 = apply_homography(0, 0, h12)
    warped_tr1 = apply_homography(x1 - 1, 0, h12)
    warped_br1 = apply_homography(x1 - 1, y1 - 1, h12)
    warped_bl1 = apply_homography(0, y1 - 1, h12)

    warped_tl3 = apply_homography(0, 0, h32)
    warped_tr3 = apply_homography(x3 - 1, 0, h32)
    warped_br3 = apply_homography(x3 - 1, y3 - 1, h32)
    warped_bl3 = apply_homography(0, y3 - 1, h32)

    new_dim12, sy, sx, change_h = getDim(warped_tl1, warped_tr1, warped_br1, warped_bl1, np.array([0, 0, 1]),
                                         np.array([x2 - 1, 0, 1]), np.array([x2 - 1, y2 - 1, 1]),
                                         np.array([0, y2 - 1, 1]), warped_tl3, warped_tr3, warped_br3, warped_bl3)

    img_mosaic = np.zeros(shape=new_dim12)

    h12i = np.linalg.inv(h12)
    h32i = np.linalg.inv(h32)

    for y in range(sy, sy + new_dim12[0]):
        for x in range(sx, sx + new_dim12[1]):
            if x <= change_h:
                orig = apply_homography(x, y, h12i)
                ox = orig[0]
                oy = orig[1]
                if (0 <= x < 60 or 0 <= y < 60 or y2 - 61 <= y < y2) and 0 <= x < x2 and 0 <= y < y2 and 0 <= ox < x1 and 0 <= oy < y1:
                    img_mosaic[y - sy][x - sx] = alpha_blend12(x, y, ox, oy, y2, img_input)
                elif 0 <= x < x2 and 0 <= y < y2:
                    img_mosaic[y - sy][x - sx] = img_input[1][y][x]
                elif ox < 0 or ox >= x1:
                    img_mosaic[y - sy][x - sx] = [0, 0, 0]
                elif oy < 0 or oy >= y1:
                    img_mosaic[y - sy][x - sx] = [0, 0, 0]
                else:
                    img_mosaic[y - sy][x - sx] = img_input[0][int(oy)][int(ox)]
            else:
                orig = apply_homography(x, y, h32i)
                ox = orig[0]
                oy = orig[1]
                if (x2 - 61 <= x < x2 or 0 <= y < 60 or y2 - 61 <= y < y2) and 0 <= x < x2 and 0 <= y < y2 and 0 <= ox < x3 and 0 <= oy < y3:
                    img_mosaic[y - sy][x - sx] = alpha_blend32(x, y, ox, oy, y2, x2, img_input)
                elif 0 <= x < x2 and 0 <= y < y2:
                    img_mosaic[y - sy][x - sx] = img_input[1][y][x]
                elif ox < 0 or ox >= x3:
                    img_mosaic[y - sy][x - sx] = [0, 0, 0]
                elif oy < 0 or oy >= y3:
                    img_mosaic[y - sy][x - sx] = [0, 0, 0]
                else:
                    img_mosaic[y - sy][x - sx] = img_input[2][int(oy)][int(ox)]

    img_mosaic = img_mosaic.astype(dtype="uint8")

    return img_mosaic