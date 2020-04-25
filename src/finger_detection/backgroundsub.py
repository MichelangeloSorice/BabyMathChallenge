import cv2 as cv
import argparse
import os
import numpy as np
from keras import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout


def pred(fgmask):
    fgmask = np.expand_dims(fgmask, axis=2)
    fgmask = np.asarray((fgmask / 255), dtype=int)
    data = np.array([fgmask])
    pred = np.argmax(model.predict(data), axis=1)
    print(pred)


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
cap = cv.VideoCapture(0)
WindowName = "Main View"
view_window = cv.namedWindow(WindowName, cv.WINDOW_NORMAL)

num_filters = 2
filter_size = 2
pool_size = 2

model = Sequential([
    Conv2D(32, kernel_size=(3, 3), input_shape=(202, 202, 1), activation='relu'),
    Conv2D(64, kernel_size=(3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Dropout(0.25),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(6, activation='softmax'),
])

model.load_weights(os.path.join(cwd, "cnn_rawtest.h5"))

count = 0
learning_rate = -1
fgmask = None
kernel = np.ones((3, 3), np.uint8)
kernel_holes = np.ones((4, 4), np.uint8)
keep = True
collect = False


while True:
    ret, frame = cap.read()
    if not keep:
        keep = not keep
        continue
    else:
        keep = not keep

    count = count+1
    # print(count)

    if count == 150 and learning_rate != 0:
        print("Stop learning --- getReady!")
        input("Press any key")
        learning_rate = 0
        count = 0

    cv.rectangle(frame, (0, 128), (202, 330), 255,  1)

    # Cropping the frame
    frame_crop = frame[128:330, 0:202]

    # Every frame is used both for calculating the foreground mask and for updating the background
    # We can modify the learning rate of the function
    fgmask = backSub.apply(frame_crop, fgmask, learning_rate)

    # Erosion, Dilatation and Morphology transformations
    # EROSION -  A pixel in the original image (either 1 or 0) will be considered 1 only if all the pixels under the
    #   kernel is 1, otherwise it is eroded (made to zero).
    # DILATION - a pixel element is '1' if at least one pixel under the kernel is '1
    # OPENING - Erosion followed by Dilation, useful to remove white noise arounf the mask
    # CLOSURE - Dilation followed by erosion, useful to remove black noise within the object
    if learning_rate == 0:
        fgmask = cv.morphologyEx(fgmask, cv.MORPH_OPEN, kernel, iterations=1)
        fgmask = cv.morphologyEx(fgmask, cv.MORPH_CLOSE, kernel, iterations=2)
        fgmask = cv.dilate(fgmask, kernel, iterations=2)

    # Show the current frame and the fg masks
    cv.imshow('Frame', frame)
    cv.imshow('mask', fgmask)

    if learning_rate == 0 and not collect:
        f = os.path.join(unlabelled, "rh_"+str(count)+".jpg")
        cv.imwrite(f, fgmask)
        img = cv.imread(f)
        matrix = np.asarray((img[:, :, 0:1] / 255), dtype=int)
        data = np.array([matrix])
        pred = np.argmax(model.predict(data), axis=1)
        print(pred)
    elif learning_rate == 0:
        f = os.path.join(unlabelled, "rh_"+str(count)+".jpg")
        cv.imwrite(f, fgmask)

    keyboard = cv.waitKey(1)
    if keyboard == 'q' or keyboard == 27:
        break