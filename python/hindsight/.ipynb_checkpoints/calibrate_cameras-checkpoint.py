"""
--------------------------------------------------------------------------------
 File: calibrate_cameras.py
 Author: Rayce Martin
 Created: 02-07-2025
 Description: <Short description of what this script/module does>
--------------------------------------------------------------------------------
"""

import cv2
import numpy as np
import sys
import keyboard
import time
import os
import glob


class Camera:
    def __init__(self, name):
        self.name = name
        self.camera_params = []
        self.camera_matrix = []
        self.roi = ()
        self.dist = []
        self.objpoints = []
        self.imgpoints = []

    def calibrate(self):
        ### Calibration ###
        current_directory = os.getcwd()

        size_of_target = (7 * 5, 3)

        # termination criteria
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        # prepare object points, like (0,0,0), (2,0,0) ..., (6,5,0)
        objp = np.zeros(size_of_target, np.float32)
        objp[:, :2] = np.mgrid[0:7, 0:5].T.reshape(-1, 2)

        # arrays to store object points and image points from all the images
        objpoints = []  # 3d points in real space
        imgpoints = []  # 2d points in real space

        images = glob.glob(str(current_directory) + '/calibration_images/' + self.name + '_camera/*.png')

        for fname in images:

            img = cv2.imread(fname)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # find the chess board corners
            ret, corners = cv2.findChessboardCorners(gray, (7, 5), None)

            # if found, add object points, image poinrts (after refining them)
            if ret == True:
                print(fname)
                objpoints.append(objp)

                corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
                imgpoints.append(corners2)

                # draw and display corners
                cv2.drawChessboardCorners(img, (7, 5), corners2, ret)
                cv2.imshow('img', img)
                cv2.waitKey(500)

        cv2.destroyAllWindows()
        self.camera_params = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None,
                                                 None)  # ret, mtx, dist, rvecs, tvecs
        h, w = img.shape[:2]
        self.camera_matrix, self.roi = cv2.getOptimalNewCameraMatrix(self.camera_params[1], self.camera_params[2],
                                                                     (w, h), 1, (w, h))
        self.objpoints = objpoints
        self.imgpoints = imgpoints

    def undistort(self, img):
        h, w = img.shape[:2]

        undstorted = cv2.undistort(img, self.camera_params[1], self.camera_params[2], None, self.camera_matrix)

        x, y, w, h = self.roi
        undstorted = undstorted[y:y + h, x:x + w]
        cv2.imshow('Undistorted Image', undstorted)


def take_images():
    current_directory = os.getcwd()
    new_directory = os.path.join(current_directory, r'calibration_images')
    if not os.path.exists(new_directory):
        os.makedirs(new_directory)

    s = 0
    if len(sys.argv) > 1:
        s = sys.argv[1]

    i = 1
    source = cv2.VideoCapture(s)

    while cv2.waitKey(1) != 27:  # Escape to exit
        has_frame, frame = source.read()
        frame = cv2.flip(frame, 0)

        if keyboard.is_pressed('s'):  # wait for 's' key to save images
            right_img = frame[:, :int(frame.shape[1] / 2), :]
            left_img = frame[:, int(frame.shape[1] / 2):, :]
            cv2.imwrite(str(new_directory) + '/cal_right_img_' + str(i) + '.png', right_img)
            cv2.imwrite(str(new_directory) + '/cal_left_img_' + str(i) + '.png', left_img)

            i += 1
            time.sleep(.1)  # debounce key press

        cv2.imshow('Camera', frame)
    source.release()
    cv2.destroyAllWindows()


def stereo_rect():
    flags = 0
    flags |= cv2.CALIB_FIX_INTRINSIC
    # Here we fix the intrinsic camara matrixes so that only Rot, Trns, Emat and Fmat are calculated.
    # Hence intrinsic parameters are the same
    gray = np.zeros((960, 1280))
    criteria_stereo = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    # This step is performed to transformation between the two cameras and calculate Essential and Fundamenatl matrix
    retS, new_mtxL, distL, new_mtxR, distR, Rot, Trns, Emat, Fmat = cv2.stereoCalibrate(left_camera.objpoints,
                                                                                        left_camera.imgpoints,
                                                                                        right_camera.imgpoints,
                                                                                        left_camera.camera_matrix,
                                                                                        left_camera.camera_params[2],
                                                                                        right_camera.camera_matrix,
                                                                                        right_camera.camera_params[2],
                                                                                        gray.shape[::-1],
                                                                                        criteria_stereo,
                                                                                        flags)

    rectify_scale = 1
    rect_l, rect_r, proj_mat_l, proj_mat_r, Q, roiL, roiR = cv2.stereoRectify(new_mtxL,
                                                                              distL,
                                                                              new_mtxR,
                                                                              distR,
                                                                              gray.shape[::-1],
                                                                              Rot,
                                                                              Trns,
                                                                              rectify_scale, (0, 0))

    Left_Stereo_Map = cv2.initUndistortRectifyMap(new_mtxL, distL, rect_l, proj_mat_l,
                                                  gray.shape[::-1], cv2.CV_16SC2)
    Right_Stereo_Map = cv2.initUndistortRectifyMap(new_mtxR, distR, rect_r, proj_mat_r,
                                                   gray.shape[::-1], cv2.CV_16SC2)

    print("Saving paraeters ......")
    cv_file = cv2.FileStorage("improved_params2.xml", cv2.FILE_STORAGE_WRITE)
    cv_file.write("Left_Stereo_Map_x", Left_Stereo_Map[0])
    cv_file.write("Left_Stereo_Map_y", Left_Stereo_Map[1])
    cv_file.write("Right_Stereo_Map_x", Right_Stereo_Map[0])
    cv_file.write("Right_Stereo_Map_y", Right_Stereo_Map[1])
    cv_file.release()
    print("Done")

    imgL = cv2.imread(r'calibration_images/left_camera/cal_left_img_20.png')
    imgR = cv2.imread(r'calibration_images/right_camera/cal_right_img_20.png')

    cv2.imshow("Left image before rectification", imgL)
    cv2.imshow("Right image before rectification", imgR)

    Left_nice = cv2.remap(imgL, Left_Stereo_Map[0], Left_Stereo_Map[1], cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
    Right_nice = cv2.remap(imgR, Right_Stereo_Map[0], Right_Stereo_Map[1], cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)

    cv2.imshow("Left image after rectification", Left_nice)
    cv2.imshow("Right image after rectification", Right_nice)
    # cv2.waitKey(0)

    out = Right_nice.copy()
    out[:, :, 0] = Right_nice[:, :, 0]
    out[:, :, 1] = Right_nice[:, :, 1]
    out[:, :, 2] = Left_nice[:, :, 2]

    cv2.imshow("Output image", out)
    # cv2.waitKey(0)


# ret, mtx, dist, rvecs, tvecs = calibrate()


if __name__ == '__main__':
    left_camera = Camera('left')
    right_camera = Camera('right')
    # take_images()
    left_camera.calibrate()
    right_camera.calibrate()
    stereo_rect()
