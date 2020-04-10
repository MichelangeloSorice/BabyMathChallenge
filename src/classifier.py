import threading
from queue import Queue
import logging
import time
from queue import Queue

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s')


class ClassifierThread(threading.Thread):
    def __init__(self, group=None, target=None, name="frame_classifier",
                 args=(), kwargs=None, verbose=None):
        super(ClassifierThread, self).__init__()
        self.name = name
        self.terminate_flag = threading.Event()
        self.frames_queue = kwargs["frames_queue"]

    def run(self):
        logging.debug('Started classifier')

        while not self.terminate_flag.is_set():
            logging.debug('Reading -  frames from queue')
            self.frames_queue.get()
            time.sleep(2)

        logging.debug('Terminating classifier')

