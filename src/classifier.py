import logging
import cv2 as cv
import numpy as np
import os
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten
from keras.models import Sequential
from constants import classifier as clconst
logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s')


class Classifier:

    def __init__(self):
        self.model = self.load_model()
        self.p1x0, self.p1x1, self.p1y0, self.p1y1 = clconst["player1"]
        self.p2x0, self.p2x1, self.p2y0, self.p2y1 = clconst["player2"]

        self.backSub = cv.createBackgroundSubtractorMOG2(varThreshold=50, detectShadows=False)
        self.op_kern = np.ones((3, 3), np.uint8)
        self.cl_kern = np.ones((4, 4), np.uint8)
        self.fg_mask = None
        self.learning_history = 0

    def learn_background(self, frame):
        frame_crop = frame[self.p1y0:self.p1y1, self.p1x0:self.p1x1]
        self.fg_mask = self.backSub.apply(frame_crop, self.fg_mask, -1)
        self.learning_history = self.learning_history+1

    def load_model(self):
        num_filters, filter_size, pool_size = clconst["model_parameters"]

        model = Sequential([
            Conv2D(num_filters, filter_size, input_shape=clconst["input_shape"]),
            MaxPooling2D(pool_size=pool_size),
            Flatten(),
            Dense(6, activation='softmax'),
        ])

        model.load_weights(os.path.join(os.getcwd(), "finger_detection", "cnn_rawtest.h5"))
        return model

    def predict(self, frame):
        frame_crop = frame[self.p1y0:self.p1y1, self.p1x0:self.p1x1]

        self.fg_mask = self.backSub.apply(frame_crop, self.fg_mask, 0)

        self.fg_mask = cv.morphologyEx(self.fg_mask, cv.MORPH_OPEN, self.op_kern, iterations=1)
        self.fg_mask = cv.morphologyEx(self.fg_mask, cv.MORPH_CLOSE, self.cl_kern, iterations=1)
        self.fg_mask = cv.dilate(self.fg_mask, self.op_kern, iterations=2)

        cv.imshow('mask', self.fg_mask)
        cv.waitKey(1)

        # Normalizing and adding third dimension is required
        self.fg_mask = self.fg_mask//255
        self.fg_mask = np.expand_dims(self.fg_mask, axis=2)
        data = np.array([self.fg_mask, self.fg_mask])

        pred = np.argmax(self.model.predict(data), axis=1)
        print(pred)

        return pred




