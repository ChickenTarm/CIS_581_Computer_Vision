"""
    File name: stream_vid.py
    Author: Hongrui Zheng
    This script is an example of streaming from an ip camera
"""

import sys, os, cv2, imageio
import numpy as np

address = 'http://192.168.1.161/live'

cap = cv2.VideoCapture(address)
while True:
    ret, frame = cap.read()
    if not ret:
        break
    cv2.imshow('cam', frame)
    k = cv2.waitKey()
    if k == 32:
        break