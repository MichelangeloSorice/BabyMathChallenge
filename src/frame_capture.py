import logging

import cv2
from PyQt5.QtCore import QThread, pyqtSignal, QTimer

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s')


class Video(QThread):
    frame_acquired = pyqtSignal(object)

    def __init__(self, group=None, target=None, name="video_recorder",
                 args=(), kwargs=None, verbose=None):
        super(Video, self).__init__()
        self.name = name

        # 0 is the camera index (only one is installed)
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        self.timer = QTimer()

        # Basic parameters for drawing on frame
        self.x0, self.y0, self.x1, self.y1 = None, None, None, None

    def setup_frame(self):
        frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.x0 = 0
        self.y0 = 202
        print("Frame height width -", frame_height, frame_width)
        self.x1, self.y1 = 128, 330

    def emit_frame(self):
        ret, frame = self.cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.rectangle(frame, (self.x0, self.y0), (self.x1, self.y1), 255,  1)
        self.frame_acquired.emit(frame)

    def run(self):
        logging.debug("Starting video recorder")
        self.timer.timeout.connect(self.emit_frame)
        self.setup_frame()




