import os
import cv2 as cv

path = os.getcwd()
test = os.path.join(path, "test")
unlabelled = os.path.join(path, "unlabelled")

try:
    os.mkdir(test)
except OSError:
    print("Creation of the directory %s failed" % test)
else:
    print("Successfully created the directory %s " % test)

WindowName = "Main View"
view_window = cv.namedWindow(WindowName, cv.WINDOW_NORMAL)

# These two lines will force the window to be on top with focus.
cv.setWindowProperty(WindowName, cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
cv.setWindowProperty(WindowName, cv.WND_PROP_FULLSCREEN, cv.WINDOW_NORMAL)

count = 0
per_type_samples = [0, 0, 0, 0, 0]

for file in os.listdir(unlabelled):
    if file.endswith(".jpg"):
        filepath = os.path.join(unlabelled, file)
        # print(filepath)

        img = cv.imread(filepath)
        cv.imshow(view_window, img)

        # Extracting waitKey code to classify images, any code out of range implicitly means bad capture
        res = cv.waitKey(0) - 48
        if 0 <= res <= 5 and per_type_samples[res] < 100:
            testfile = os.path.join(test, str(res) + "_rh_" + str(count) + ".jpg")
            cv.imwrite(testfile, img)
            os.remove(filepath)
            count = count + 1
            per_type_samples[res] = per_type_samples[res]+1

        cv.destroyAllWindows()
