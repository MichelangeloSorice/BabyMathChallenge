import cv2
import threading
import logging

import qimage2ndarray
from PyQt5.QtWidgets import  QWidget, QLabel, QApplication
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot, QTimer
from PyQt5.QtGui import QImage, QPixmap
from queue import Queue

from logger import QPlainTextEditLogger


logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s')


class VideoRecorderThread(QThread):
    frame_acquired = pyqtSignal(object)

    def __init__(self, group=None, target=None, name="video_recorder",
                 args=(), kwargs=None, verbose=None):
        super(VideoRecorderThread, self).__init__()
        self.name = name

        # 0 is the camera index (only one is installed)
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    def emit_frame(self):
        logging.debug("Emitting")
        ret, frame = self.cap.read()
        self.frame_acquired.emit(frame)

    def run(self):
        logging.debug("Starting")
        self.timer = QTimer()
        self.timer.timeout.connect(self.emit_frame)
        self.timer.start(1000.0/60) # video streamed at 60 fps


class Video(QThread):
    frame_acquired = pyqtSignal(object)

    def run(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if ret:
                # https://stackoverflow.com/a/55468544/6622587
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.frame_acquired.emit(rgbImage)



