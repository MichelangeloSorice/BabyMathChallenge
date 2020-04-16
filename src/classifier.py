import threading
from queue import Queue
import logging
import time
from queue import Queue
from random import randint
from PyQt5.QtCore import QThread, pyqtSignal

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s')


class ClassifierThread(QThread):
    frame_processed = pyqtSignal(object)

    def __init__(self, group=None, target=None, name="frame_classifier",
                 args=(), kwargs=None, verbose=None):
        super(ClassifierThread, self).__init__()
        self.setObjectName(name)
        self.queue = args

    def run(self):
            logging.debug('Started classifier')
            count = 0
            while True:
                image = self.queue.get(block=True, timeout=None)
                count = count+1
                if count == 100:
                    count = 0
                    self.frame_processed.emit("Classified as "+str(randint(1, 5)))




