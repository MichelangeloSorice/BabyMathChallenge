import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    # Capturing frame by frame
    ret, frame = cap.read()
    h, w, d = frame.shape
    h_start, w_end = h*70//100, w*30//100

    # Operating on the frame, conversion to greyscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    bottom_left = gray[0:h_start, 0:w_end].copy()

    # Showing frame
    cv2.imshow('frame', gray)
    cv2.imshow('frame_bottom', bottom_left)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Everything done releasing caputer object
cap.release()
cv2.destroyAllWindows()
