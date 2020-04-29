import cv2 as cv
import os
import numpy as np
from keras import models


def pred(mask):
    mask = np.expand_dims(mask, axis=2)
    matrix = mask[:, :, 0:1] // 255
    data = np.array([matrix])
    pred = np.argmax(model.predict(data), axis=1)
    return str(pred[0])

def create_data_folder():
    # Creating a directory to store bgmasks
    cwd = os.getcwd()
    unlabelled = os.path.join(cwd, "unlabelled")

    try:
        os.mkdir(unlabelled)
    except OSError:
        print("Creation of the directory %s failed" % unlabelled)
    else:
        print("Successfully created the directory %s " % unlabelled)

    return cwd, unlabelled


def load_from(cwd):
    return models.load_model(os.path.join(cwd, 'training_res', 'model.h5'))


# Erosion, Dilatation and Morphology transformations
# EROSION -  A pixel in the original image (either 1 or 0) will be considered 1 only if all the pixels under the
#   kernel is 1, otherwise it is eroded (made to zero).
# DILATION - a pixel element is '1' if at least one pixel under the kernel is '1
# OPENING - Erosion followed by Dilation, useful to remove white noise arounf the mask
# CLOSURE - Dilation followed by erosion, useful to remove black noise within the object
def morph(fgmask):
    fgmask = cv.morphologyEx(fgmask, cv.MORPH_OPEN, kernel, iterations=1)
    fgmask = cv.morphologyEx(fgmask, cv.MORPH_CLOSE, kernel, iterations=2)
    return cv.dilate(fgmask, kernel, iterations=2)


# Creating folder for captures
cwd, unlabelled = create_data_folder()

# Starting video capture
cap = cv.VideoCapture(0)

# Variables used for foreground mask creation
backSub1 = cv.createBackgroundSubtractorMOG2(varThreshold=50, detectShadows=False)
learning_rate = -1
kernel = np.ones((3, 3), np.uint8)
fgmask1 = None

# Loading neural network model
model = load_from(cwd)

count = 0
# If set to true captures are collected
collect = False

while True:
    ret, frame = cap.read()
    count = count+1

    if count == 200 and learning_rate != 0:
        print("Stop learning --- getReady!")
        learning_rate = 0
        count = 0

    # Drawing detection area
    cv.rectangle(frame, (0, 128), (202, 330), (0, 0, 255),  1)

    # Cropping the frame on detection area
    frame_cropp1 = frame[128:330, 0:202]

    # Every frame is used both for calculating the foreground mask and for updating the background
    # We can modify the learning rate of the function
    fgmask1 = backSub1.apply(frame_cropp1, fgmask1, learning_rate)

    pred_p1 = "Learning BG..."

    if learning_rate == 0:
        fgmask1 = morph(fgmask1)
        res_1 = cv.resize(fgmask1, (40, 40), interpolation=cv.INTER_AREA)

        if model is not None:
            pred_p1 = pred(res_1)
        else:
            pred_p1 = "?"

        if collect:
            f = os.path.join(unlabelled, "rh_"+str(count)+".jpg")
            cv.imwrite(f, res_1)

    cv.putText(frame, pred_p1, (10, 122), cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    # Show the current frame and the fg masks
    cv.imshow('MASK 1', fgmask1)
    cv.imshow('Frame', frame)

    keyboard = cv.waitKey(1)
    if keyboard == 27:
        break

cv.destroyAllWindows()
cap.release()