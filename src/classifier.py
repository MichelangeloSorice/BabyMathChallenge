import logging
import cv2 as cv
import numpy as np
import os
from keras import models
from constants import classifier as clconst


class Classifier:
    def __init__(self):
        self.model = self.load_model()
        self.x0, self.x1, self.y0, self.y1 = clconst["roi"]

        self.backSub1 = cv.createBackgroundSubtractorMOG2(varThreshold=50, detectShadows=False)
        self.op_kern = np.ones((3, 3), np.uint8)
        self.fg_mask = None
        self.learning_history = 0
        self.learning_bg, self.bg_acquired = False, False

    @staticmethod
    def load_model():
        return models.load_model(os.path.join(os.getcwd(), 'finger_detection', 'training_res', 'model.h5'))

    @staticmethod
    def prepare_data(mask):
        # Reducing crop size
        mask = cv.resize(mask, (clconst["input_shape"][0], clconst["input_shape"][1]), interpolation=cv.INTER_AREA)
        # Expanding dimensions
        mask = np.expand_dims(mask, axis=2)
        # Normalizing values
        matrix = mask[:, :, 0:1] // 255
        return matrix

    # Crops ROI region of frame
    def crop(self, frame):
        return frame[self.y0:self.y1, self.x0:self.x1]

    def reset_bg(self):
        self.backSub1 = cv.createBackgroundSubtractorMOG2(varThreshold=50, detectShadows=False)
        self.fg_mask = None
        self.learning_history = 0
        self.bg_acquired = False

    def learn_background(self, frame):
        crop = self.crop(frame)
        self.fg_mask = self.backSub1.apply(crop, self.fg_mask, -1)
        self.learning_history = self.learning_history + 1

        if self.learning_history == clconst["bg_learning_history"]:
            self.bg_acquired = True

    def apply_bgsub_morph(self, frame_crop):
        # Applying foreground mask
        self.fg_mask = self.backSub1.apply(frame_crop, self.fg_mask, 0)

        # Performing morphological transformation to reduce noise
        self.fg_mask = cv.morphologyEx(self.fg_mask, cv.MORPH_OPEN, self.op_kern, iterations=1)
        self.fg_mask = cv.morphologyEx(self.fg_mask, cv.MORPH_CLOSE, self.op_kern, iterations=2)
        self.fg_mask = cv.dilate(self.fg_mask, self.op_kern, iterations=2)

        return self.fg_mask

    def process_frame(self, frame):
        fg1 = self.apply_bgsub_morph(self.crop(frame))

        data = np.array([self.prepare_data(fg1)])
        res = np.argmax(self.model.predict(data), axis=1)
        # Writing label on roi rectangle
        cv.putText(frame, str(res[0]), (self.x0+10, self.y0-10), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        return res
