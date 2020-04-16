from queue import Queue

import cv2
import qimage2ndarray
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow

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

    def shutdown(self):
        self.video.terminate()
        self.classifier.terminate()
        QCoreApplication.quit()

    def set_image(self, rgbImage):
        self.frame_queue.put(rgbImage)
        # Simple way to draw rectangle for players to position their hands, probably we will use gui for this
        # cv2.rectangle(rgbImage, (0, 255), (300, 300), 1)
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


