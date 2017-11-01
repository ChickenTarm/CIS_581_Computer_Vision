import numpy as np

def getOffsets(boxes, mask, maskIndex):

    xOffset = 0;
    yOffset = 0;

    n,m = mask.shape;

    maskCenterY = n/2;
    maskCenterX = m/2;


    faceValues = boxes[0];
    leftEyeValues = boxes[1];
    rightEyeValues = boxes[2];

    leftTopCorner = faceValues[0];
    rightTopCorner = faceValues[1];
    rightBottomCorner = faceValues[2];

    faceCenterX = (rightTopCorner[0] + leftTopCorner[0])/2;
    faceCenterY = (rightBottomCorner[1] + rightTopCorner[1])/2;

    lefteyeleftTopCorner = leftEyeValues[0];
    lefteyerightTopCorner = leftEyeValues[1];
    lefteyerightBottomCorner = leftEyeValues[2];

    lefteyeCenterX = (lefteyerightTopCorner[0] + lefteyeleftTopCorner[0])/2;
    lefteyeCenterY = (lefteyerightBottomCorner[1] + lefteyerightTopCorner[1])/2;

    righteyeleftTopCorner = rightEyeValues[0];
    righteyerightTopCorner = rightEyeValues[1];
    righteyerightBottomCorner = rightEyeValues[2];

    righteyeCenterX = (righteyerightTopCorner[0] + righteyeleftTopCorner[0])/2;
    righteyeCenterY =  (righteyerightBottomCorner[1] + righteyerightTopCorner[1])/2;

    if (maskIndex == 0):
        leftEyeTopleft = leftEyeValues[0];
        xOffset = leftEyeTopleft[0] - m;
        yOffset = leftTopCorner[1];

    if (maskIndex == 1):
        rightEyeTopRight = rightEyeValues[1];
        xOffset = rightEyeTopRight[0];
        yOffset = rightTopCorner[1];
    if (maskIndex == 2):
        xOffset = faceCenterX - maskCenterX;
        yOffset = faceCenterY - maskCenterY;

    if (maskIndex == 3):
        xOffset = leftEyeValues[1][0] - m;
        yOffset = leftTopCorner[1] - maskCenterY;

    if (maskIndex == 4):
        xOffset = rightEyeValues[0][0];
        yOffset = rightTopCorner[1] - maskCenterY;
    if (maskIndex == 5):
        xOffset = faceCenterX - maskCenterX;
        yOffset = faceCenterY;
    if (maskIndex == 6):
        xOffset = lefteyeCenterX - maskCenterX;
        yOffset = lefteyeCenterY - maskCenterY;
    if (maskIndex == 7):
        xOffset = righteyeCenterX - maskCenterX;
        yOffset = righteyeCenterY - maskCenterY;
    if (maskIndex == 8):
        xOffset = faceCenterX - maskCenterX;
        yOffset = faceCenterY;

    print xOffset
    print yOffset
    if (xOffset < 0):
        xOffset = 1;
    if (yOffset < 0):
        yOffset = 1;
    return xOffset, yOffset;
