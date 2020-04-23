import cv2 as cv
import argparse
import os
import numpy as np


# Test script to evaluate background subtraction
parser = argparse.ArgumentParser(description='Testing OPENCV background subtraction functionality')
parser.add_argument('--algo', type=str, help='Background subtraction method (KNN, MOG2).', default='MOG2')
args = parser.parse_args()

if args.algo == 'MOG2':
    backSub = cv.createBackgroundSubtractorMOG2(varThreshold=50, detectShadows=False)
else:
    backSub = cv.createBackgroundSubtractorKNN()


# Creating a directory to store bgmasks
cwd = os.getcwd()
unlabelled = os.path.join(cwd, "unlabelled")

try:
    os.mkdir(unlabelled)
except OSError:
    print("Creation of the directory %s failed" % unlabelled)
else:
    print("Successfully created the directory %s " % unlabelled)


# 0 is the camera index (only one is installed)
cap = cv.VideoCapture(0, cv.CAP_DSHOW)
WindowName = "Main View"
view_window = cv.namedWindow(WindowName, cv.WINDOW_NORMAL)

count = 0
learning_rate = -1
fgmask = None
kernel = np.ones((3, 3), np.uint8)
kernel_holes = np.ones((4, 4), np.uint8)
keep = True

while True:
    ret, frame = cap.read()
    if not keep:
        keep = not keep
        continue
    else:
        keep = not keep

    count = count+1
    print(count)
    if count == 150 and learning_rate != 0:
        print("Stop learning --- getReady!")
        input("Press any key")
        learning_rate = 0
        count = 0

    #frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    cv.rectangle(frame, (0, 128), (202, 330), 255,  1)

    # Cropping the frame
    frame_crop = frame[128:330, 0:202]

    # Every frame is used both for calculating the foreground mask and for updating the background
    # We can modify the learning rate of the function
    fgmask = backSub.apply(frame_crop, fgmask, learning_rate)
    print(fgmask.shape)

    # Erosion, Dilatation and Morphology transformations
    # EROSION -  A pixel in the original image (either 1 or 0) will be considered 1 only if all the pixels under the
    #   kernel is 1, otherwise it is eroded (made to zero).
    # DILATION - a pixel element is '1' if at least one pixel under the kernel is '1
    # OPENING - Erosion followed by Dilation, useful to remove white noise arounf the mask
    # CLOSURE - Dilation followed by erosion, useful to remove black noise within the object
    if(learning_rate == 0):
        fgmask = cv.morphologyEx(fgmask, cv.MORPH_OPEN, kernel, iterations=1)
        fgmask = cv.morphologyEx(fgmask, cv.MORPH_CLOSE, kernel_holes, iterations=1)
        fgmask = cv.dilate(fgmask, kernel, iterations=2)

    frame_crop = cv.bitwise_and(frame_crop, frame_crop, mask=fgmask)

    # Show the current frame and the fg masks
    cv.imshow('Frame', frame)
    cv.imshow('mask', fgmask)
    cv.imshow('crop', frame_crop)

    if learning_rate == 0:
        cv.imwrite(os.path.join(unlabelled, "rh_"+str(count)+".jpg"), fgmask)

    keyboard = cv.waitKey(1)
    if keyboard == 'q' or keyboard == 27:
        break