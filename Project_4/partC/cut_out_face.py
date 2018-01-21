'''
  File name: cout_out_face.py
  Author: Tarmily Wen
  Date created:
'''

from scipy.spatial import ConvexHull
from matplotlib import pyplot as plt
from PIL import Image
import numpy as np
from matplotlib.path import Path
import itertools
from scipy import misc


def cut_out_face(img, face_pts):
    face_hull = ConvexHull(face_pts[0:27, :])
    l_eye_hull = ConvexHull(face_pts[36:42, :])
    r_eye_hull = ConvexHull(face_pts[42:48, :])
    # tested both larger mouth cutout around the lips and smaller mouth cutout
    # inside the lips, smaller looks more natural
    mouth_hull = ConvexHull(face_pts[60:, :])

    face_path = Path(face_pts[face_hull.vertices])
    l_eye_path = Path(face_pts[l_eye_hull.vertices + 36])
    r_eye_path = Path(face_pts[r_eye_hull.vertices + 42])
    mouth_path = Path(face_pts[mouth_hull.vertices + 60])

    y_max, x_max, channels = img.shape

    y = np.arange(0, y_max)
    x = np.arange(0, x_max)
    points = np.array(list(itertools.product(x, y)))
    l_eye_bool = l_eye_path.contains_points(points)
    r_eye_bool = r_eye_path.contains_points(points)
    mouth_bool = mouth_path.contains_points(points)
    face_bool = face_path.contains_points(points)

    cut = np.copy(img)

    cut[points[face_bool == False][:, 1], points[face_bool == False][:, 0]] = [0, 0, 0]
    cut[points[l_eye_bool][:, 1], points[l_eye_bool][:, 0]] = [0, 0, 0]
    cut[points[r_eye_bool][:, 1], points[r_eye_bool][:, 0]] = [0, 0, 0]
    cut[points[mouth_bool][:, 1], points[mouth_bool][:, 0]] = [0, 0, 0]

    # misc.imsave("cutout.png", cut)
    # misc.imsave("mask.png", mask)
    return cut

# cut_out_face(np.asarray(Image.open("Marq.png")), np.loadtxt("Marq.csv"))
# cut_out_face(np.asarray(Image.open("Smile.png")), np.loadtxt("Smile.csv"))
# cut_out_face(np.asarray(Image.open("Robot.png")), np.loadtxt("Robot.csv"))
# cut_out_face(np.asarray(Image.open("morphed_face.png")), np.loadtxt("./Faces/Smile.csv"))
