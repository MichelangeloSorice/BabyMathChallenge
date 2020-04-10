import cv2
import threading
import logging
from queue import Queue

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s')


class VideoRecorderThread(threading.Thread):

    def __init__(self, group=None, target=None, name="video_recorder",
                 args=(), kwargs=None, verbose=None):
        super(VideoRecorderThread, self).__init__()
        self.name = name
        self.terminate_flag = threading.Event()

        # 0 is the camera index (only one is installed)
        self.cap = cv2.VideoCapture(0)

        # Queue object to communicate with classification threads
        self.p1_queue, self.p2_queue = kwargs["p1_queue"], kwargs["p2_queue"]

        if self.p1_queue is None or self.p2_queue is None:
            self.terminate_flag.set()
            logging.error('Missing required arguments, thread will exit')
        else:
            logging.debug('Starting video recording')

    def run(self):
        try:
            ret, frame = self.cap.read()
            h, w, d = frame.shape
            h_start, h_end, w_start, w_end = h*60//100, h*90//100, 0, w*30//100

            while not self.terminate_flag.is_set():
                ret, frame = self.cap.read()
                # Operating on the frame, conversion to greyscale
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                # Cropping
                bottom_left = gray[h_start:h_end, w_start:w_end].copy()

                self.p1_queue.put(bottom_left)
                self.p2_queue.put(bottom_left)
                # Showing frame
                cv2.imshow('frame', gray)
                cv2.waitKey(1)
                # Waits one second for q key press
                # if cv2.waitKey(1) & 0xFF == ord('q'):
                # break

        except ValueError:
            logging.error('An error occurred, thread will be closed')

        finally:
            # Everything done releasing captures object
            self.cap.release()
            cv2.destroyAllWindows()
            logging.debug('Terminating')


