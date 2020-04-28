import logging
import cv2 as cv
import numpy as np
import os

from keras import models

from constants import classifier as clconst
logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s')


class Classifier:

    def __init__(self):
        self.model = self.load_model()
        self.p1x0, self.p1x1, self.p1y0, self.p1y1 = clconst["player1"]
        self.p2x0, self.p2x1, self.p2y0, self.p2y1 = clconst["player2"]

        self.backSub1 = cv.createBackgroundSubtractorMOG2(varThreshold=50, detectShadows=False)
        self.backSub2 = cv.createBackgroundSubtractorMOG2(varThreshold=50, detectShadows=False)
        self.op_kern = np.ones((3, 3), np.uint8)

        self.fg_maskp1, self.fg_maskp2 = None, None
        self.learning_history = 0
        self.learning_bg, self.bg_acquired = False, False

    def load_model(self):
        return models.load_model(os.path.join(os.getcwd(), 'finger_detection', 'training_res', 'model.h5'))

    def crop(self, frame):
        frame_cropp1 = frame[self.p1y0:self.p1y1, self.p1x0:self.p1x1]
        frame_cropp2 = frame[self.p2y0:self.p2y1, self.p2x0:self.p2x1]
        return frame_cropp1, frame_cropp2

    def reset_bg(self):
        self.backSub1 = cv.createBackgroundSubtractorMOG2(varThreshold=50, detectShadows=False)
        self.backSub2 = cv.createBackgroundSubtractorMOG2(varThreshold=50, detectShadows=False)
        self.fg_maskp1, self.fg_maskp2 = None, None
        self.learning_history = 0
        self.bg_acquired = False

    # Applies frames to background subtractors, return true while learning, false when done
    def learn_background(self, frame):
        crops = self.crop(frame)

        self.fg_maskp1 = self.backSub1.apply(crops[0], self.fg_maskp1, -1)
        self.fg_maskp2 = self.backSub2.apply(crops[1], self.fg_maskp2, -1)

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

    def apply_bgsub_morph(self, frame_crop, mask, bgsub):
        # Applying foreground mask
        mask = bgsub.apply(frame_crop, mask, 0)

        # Perdfroming morphological transformation to reduce noise
        mask = cv.morphologyEx(mask, cv.MORPH_OPEN, self.op_kern, iterations=1)
        mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, self.op_kern, iterations=2)
        mask = cv.dilate(mask, self.op_kern, iterations=2)

        return mask

    def process_frame(self, frame):
        crops = self.crop(frame)
        fg1 = self.apply_bgsub_morph(crops[0], self.fg_maskp1, self.backSub1)
        fg2 = self.apply_bgsub_morph(crops[1], self.fg_maskp2, self.backSub2)

        data = np.array([self.prep_data(fg1), self.prep_data(fg2)])

        cv.imshow('mask1', fg1)
        cv.imshow('mask2', fg2)
        cv.waitKey(1)
        res = np.argmax(self.model.predict(data), axis=1)
        print(res)
        return res




