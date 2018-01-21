import imageio
from scipy import misc


def myvideomosaic(img_mosaic):

    for i in range(0, len(img_mosaic)):
        im = img_mosaic[i]
        resized = misc.imresize(im, size=(2160, 3840), interp='cubic')
        img_mosaic[i] = resized

    imageio.mimsave('result.mp4', img_mosaic, format='MP4', fps=25)