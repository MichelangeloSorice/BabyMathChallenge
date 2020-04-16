import sys

import qimage2ndarray
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton, QMainWindow
from PyQt5.QtCore import pyqtSlot, QTimer, Qt, QCoreApplication
import cv2

from classifier import ClassifierThread
from frame_capture import Video
from queue import Queue

from gui.babymath_ui import Ui_BabyMath
from constants import gui_constants as gui_const

class BabyMathApp(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent=parent)
        self.title = 'BabyMathChallenge'
        self.ui = Ui_BabyMath()
        self.frame_queue = Queue()
        self.video = Video(self)
        self.classifier = ClassifierThread(self, name="frame_classifier", args=self.frame_queue)
        self.init_()

    def shutdown(self):
        self.video.terminate()
        self.classifier.terminate()
        QCoreApplication.quit()

    def set_image(self, rgbImage):
        self.frame_queue.put(rgbImage)
        self.ui.camera_label.setPixmap(QPixmap.fromImage(qimage2ndarray.array2qimage(rgbImage)))

    def set_p1_label(self, eval):
        self.ui.p1_label.setText(eval)

    def init_(self):
        self.ui.setupUi(self)
        cma_placeholder = str(gui_const["images_dir"]+gui_const["cam_placeholder"])
        self.ui.camera_label.setPixmap(QPixmap(cma_placeholder))
        self.ui.quiter.clicked.connect(self.shutdown)
        self.classifier.frame_processed.connect(self.set_p1_label)
        self.video.frame_acquired.connect(self.set_image)
        self.video.start()
        self.classifier.start()


# Currently stealing from
# https://stackoverflow.com/questions/44404349/pyqt-showing-video-stream-from-opencv


