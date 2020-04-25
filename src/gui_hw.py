from queue import Queue

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QMainWindow

from classifier import Classifier
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
        self.classifier = Classifier()
        self.init_()

    def closeEvent(self, event):
        # Make it close properly
        self.video.terminate()
        QCoreApplication.quit()

    def process_image(self, frame):
        if self.classifier.learning_history < 150:
            self.classifier.learn_background(frame)
            pred = ["?","?"]
        else:
            pred = self.classifier.predict(frame)

        img = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        self.ui.camera_label.setPixmap(QPixmap.fromImage(img))
        self.setlabels(pred)

    def setlabels(self, pred):
        self.ui.p1_label.setText(str(pred[0]))
        self.ui.p2_label.setText(str(pred[1]))

    def init_(self):
        self.ui.setupUi(self)
        cma_placeholder = str(gui_const["images_dir"]+gui_const["cam_placeholder"])

        self.ui.camera_label.setPixmap(QPixmap(cma_placeholder))
        self.video.frame_acquired.connect(self.process_image)
        self.video.start()
        self.video.timer.start(gui_const["fps"])


# Currently stealing from
# https://stackoverflow.com/questions/44404349/pyqt-showing-video-stream-from-opencv


