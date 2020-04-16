import threading
from queue import Queue
import logging
import time
from queue import Queue

from PyQt5.QtCore import QThread, pyqtSignal

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s')


class ClassifierThread(QThread):
    count = 0
    frame_processed = pyqtSignal(object)

    def __init__(self, group=None, target=None, name="frame_classifier",
                 args=(), kwargs=None, verbose=None):
        super(ClassifierThread, self).__init__()
        self.name = name
        self.queue = args

    @pyqtSignal(object)
    def receive(self, image):
        self.count = self.count
        self.frame_processed.emit(str("Received frame"))

    def run(self):
            logging.debug('Started classifier')




