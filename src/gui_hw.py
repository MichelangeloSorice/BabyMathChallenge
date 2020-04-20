from queue import Queue

import cv2
import qimage2ndarray
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow
from qimage2ndarray.dynqt import QtGui

from classifier import ClassifierThread
from constants import gui_constants as gui_const
from frame_capture import Video
from gui.babymath_ui import Ui_BabyMath


class BabyMathApp(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent=parent)
        self.title = 'BabyMathChallenge'
        self.ui = Ui_BabyMath()
        self.frame_queue = Queue()
        self.video = Video(self)
        self.classifier = ClassifierThread(self, name="frame_classifier", args=self.frame_queue)
        self.init_()

    def closeEvent(self, event):
        # Make it close properly
        self.video.terminate()
        self.classifier.terminate()
        QCoreApplication.quit()

    def set_image(self, frame):
        self.frame_queue.put(frame)
        # Simple way to draw rectangle for players to position their hands, probably we will use gui for this
        # cv2.rectangle(rgbImage, (0, 255), (300, 300), 1)
        img = QtGui.QImage(frame, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
        self.ui.camera_label.setPixmap(QPixmap.fromImage(img))

    def set_p1_label(self, eval):
        self.ui.p1_label.setText(eval)

    def init_(self):
        self.ui.setupUi(self)
        cma_placeholder = str(gui_const["images_dir"]+gui_const["cam_placeholder"])
        self.ui.camera_label.setPixmap(QPixmap(cma_placeholder))

        self.ui.quiter.clicked.connect(self.closeEvent)

        self.classifier.frame_processed.connect(self.set_p1_label)
        self.video.frame_acquired.connect(self.set_image)
        self.video.start()
        self.video.timer.start(gui_const["fps"])
        self.classifier.start()


# Currently stealing from
# https://stackoverflow.com/questions/44404349/pyqt-showing-video-stream-from-opencv


