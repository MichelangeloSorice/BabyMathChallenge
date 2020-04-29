import cv2
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QMainWindow

from classifier import Classifier
from constants import gui_constants as gui_const
from frame_capture import Video
from gui.babymath_ui import Ui_BabyMath


class FingerDetectionApp(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent=parent)

        self.ui = Ui_BabyMath()

        self.video = Video(self)
        self.classifier = Classifier()
        self.learning_bg = False

        self.init_()

    def closeEvent(self, event):
        self.video.cap.release()
        self.video.terminate()
        QCoreApplication.quit()

    def start_bgacquisition(self):
        self.classifier.reset_bg()
        self.learning_bg = True
        self.ui.dialog.setText("Acquiring background...")

    def process_image(self, frame):
        if self.learning_bg:
            self.classifier.learn_background(frame)
            if self.classifier.bg_acquired:
                self.learning_bg = False
                self.ui.dialog.setText("Background acquired, READY!")

        elif self.classifier.bg_acquired:
            self.classifier.process_frame(frame)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)

        self.ui.camera_label.setPixmap(QPixmap.fromImage(img))

    def init_(self):
        self.ui.setupUi(self)

        self.video.frame_acquired.connect(self.process_image)
        self.video.start()
        self.video.timer.start(gui_const["fps"])
        self.ui.dialog.setText("Acquire BG to detect fingers!")
        self.ui.detectbg_btn.clicked.connect(self.start_bgacquisition)



