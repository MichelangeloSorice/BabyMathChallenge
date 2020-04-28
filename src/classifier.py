import logging
import cv2 as cv
import numpy as np
import os

from keras import models
from pynput.keyboard import Controller, Key

from constants import classifier as clconst

class Classifier:

    def __init__(self):
        self.model = self.load_model()
        self.p1x0, self.p1x1, self.p1y0, self.p1y1 = clconst["player1"]

        self.backSub1 = cv.createBackgroundSubtractorMOG2(varThreshold=50, detectShadows=False)
        self.op_kern = np.ones((3, 3), np.uint8)

        self.fg_maskp1 = None
        self.learning_history = 0
        self.learning_bg, self.bg_acquired = False, False

    def load_model(self):
        return models.load_model(os.path.join(os.getcwd(), 'finger_detection', 'training_res', 'model.h5'))

    def crop(self, frame):
        return frame[self.p1y0:self.p1y1, self.p1x0:self.p1x1]

    def reset_bg(self):
        self.backSub1 = cv.createBackgroundSubtractorMOG2(varThreshold=50, detectShadows=False)
        self.fg_maskp1 = None
        self.learning_history = 0
        self.bg_acquired = False

    # Applies frames to background subtractors, return true while learning, false when done
    def learn_background(self, frame):
        crop = self.crop(frame)
        self.fg_maskp1 = self.backSub1.apply(crop, self.fg_maskp1, -1)
        self.learning_history = self.learning_history+1

        if self.learning_history == clconst["bg_learning_history"]:
            self.bg_acquired = True

    def prep_data(self, mask):
        # Reducing crop size
        mask = cv.resize(mask, (40, 40), interpolation=cv.INTER_AREA)
        # Expanding dimensions
        mask = np.expand_dims(mask, axis=2)
        # Normalizing values
        matrix = mask[:, :, 0:1] // 255

        return matrix

    def apply_bgsub_morph(self, frame_crop):
        # Applying foreground mask
        self.fg_maskp1 = self.backSub1.apply(frame_crop, self.fg_maskp1, 0)

        # Performing morphological transformation to reduce noise
        self.fg_maskp1 = cv.morphologyEx(self.fg_maskp1, cv.MORPH_OPEN, self.op_kern, iterations=1)
        self.fg_maskp1 = cv.morphologyEx(self.fg_maskp1, cv.MORPH_CLOSE, self.op_kern, iterations=2)
        self.fg_maskp1 = cv.dilate(self.fg_maskp1, self.op_kern, iterations=2)

        return self.fg_maskp1

    def process_frame(self, frame):
        fg1 = self.apply_bgsub_morph(self.crop(frame))

        data = np.array([self.prep_data(fg1)])

        #cv.imshow('mask1', fg1)
        #cv.waitKey(1)

        res = np.argmax(self.model.predict(data), axis=1)
        cv.putText(frame, str(res[0]), (10, 122), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        return res




