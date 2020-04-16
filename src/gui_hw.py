import sys

import qimage2ndarray
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtCore import pyqtSlot, QTimer, Qt
import cv2

from classifier import ClassifierThread
from frame_capture import VideoRecorderThread, Video
from queue import Queue

class BabyMathApp(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'BabyMathChallenge'
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 480
        self.frame_queue = Queue()
        self.label = QLabel(self)
        self.label_classifier = QLabel(self)
        self.button = QPushButton("Quiter")
        self.init_ui()

    def set_image(self, rgbImage):
        h, w, ch = rgbImage.shape
        bytesPerLine = ch * w
        convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
        p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
        self.frame_queue.put(rgbImage)
        self.label.setPixmap(QPixmap.fromImage(p))

    def classifier_out(self, message):
        self.label_classifier.setText(message)

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.resize(1800, 1200)

        layout = QVBoxLayout()
        # Attach label to box layout
        self.label_classifier.setText("HELLO")
        layout.addWidget(self.label)
        layout.addWidget(self.label_classifier)
        layout.addWidget(self.button)
        self.setLayout(layout)
        video = Video(self)
        classifier = ClassifierThread(self, name="frame_classifier", args=self.frame_queue)
        self.connect(video.frame_acquired, classifier.receive, )
        classifier.frame_processed.connect(self.classifier_out)
        video.frame_acquired.connect(self.set_image)
        video.start()
        classifier.start()

        self.show()


app = QApplication([])
window = BabyMathApp()

app.exec_()


# Currently stealing from
# https://stackoverflow.com/questions/44404349/pyqt-showing-video-stream-from-opencv


