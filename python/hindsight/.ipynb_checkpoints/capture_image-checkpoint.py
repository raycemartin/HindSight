import cv2
import numpy as np
import sys

s = 0
if len(sys.argv) > 1:
    s = sys.argv[1]

sensitivity = 15
source = cv2.VideoCapture(s)

window_name = 'Camera'
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

while cv2.waitKey(1) != 27:  # Escape
    has_frame, frame = source.read()
    frame = cv2.flip(frame, 0)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    right_img = gray[:, :int(gray.shape[1] / 2)]
    left_img = gray[:, int(gray.shape[1] / 2):]

    stereo = cv2.StereoBM_create(numDisparities=16, blockSize=31)
    disparity = stereo.compute(left_img, right_img)
    disparity = cv2.normalize(disparity, 0, 255, cv2.NORM_MINMAX)
    cv2.imshow('Disparity', disparity)
    # cv2.imshow('Left', left_img)
    # cv2.imshow('Right', right_img)
    cv2.imshow('Original', frame)
source.release()
cv2.destroyAllWindows()