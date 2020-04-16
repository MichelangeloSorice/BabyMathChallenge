from frame_capture import VideoRecorderThread
from classifier import ClassifierThread

from queue import Queue
import logging
import signal
import time

logging.basicConfig(level=logging.INFO,
                    format='(%(threadName)-9s) %(message)s')


class ServiceExit(Exception):
    """ Custom exception used to gracefully trigger the clean exit of all running threads """
    pass


def service_shutdown(signum, frame):
    logging.debug('Caught signal %d' % signum)
    raise ServiceExit


def main():
    # Register the signal handlers
    signal.signal(signal.SIGTERM, service_shutdown)
    signal.signal(signal.SIGINT, service_shutdown)

    frame_queues = {
        "display_queue": Queue(),
        "p1_queue": Queue(),
        "p2_queue": Queue()
    }

    logging.debug('BabyMathChallenge - Starting!')

    try:
        video_recorder = VideoRecorderThread(None, name='video_recorder', kwargs=frame_queues)
        p1_classifier = ClassifierThread(None, name='p1_classifier', kwargs={"frames_queue": frame_queues['p1_queue']})
        p2_classifier = ClassifierThread(None, name='p2_classifier', kwargs={"frames_queue": frame_queues['p2_queue']})

        video_recorder.start()
        p1_classifier.start()
        p2_classifier.start()

        while True:
            time.sleep(1)

    except ServiceExit:
        video_recorder.terminate_flag.set()
        p1_classifier.terminate_flag.set()
        p2_classifier.terminate_flag.set()

        video_recorder.join()
        p1_classifier.join()
        p2_classifier.join()

    logging.debug('BabyMathChallenge - Terminating')


# Lets run
main()
