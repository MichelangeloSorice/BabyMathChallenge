import logging

import cv2
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from constants import classifier as clconst

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s')


class Video(QThread):
    frame_acquired = pyqtSignal(object)

    def __init__(self, group=None, target=None, name="video_recorder",
                 args=(), kwargs=None, verbose=None):
        super(Video, self).__init__()
        self.name = name

        # 0 is the camera index (only one is installed)
        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer()

        # Basic parameters for drawing on frame
        self.p1x0, self.p1x1, self.p1y0, self.p1y1 = clconst["player1"]

    def emit_frame(self):
        ret, frame = self.cap.read()
        cv2.rectangle(frame, (self.p1x0, self.p1y0), (self.p1x1, self.p1y1), (0, 0, 255),  1)
        self.frame_acquired.emit(frame)

    def run(self):
        logging.debug("Starting video recorder")
        self.timer.timeout.connect(self.emit_frame)




