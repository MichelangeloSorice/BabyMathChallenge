import os
from random import shuffle
import cv2 as cv
from constants import classifier as cls


'''
Script for manual classification of unlabelled ROI captures
'''

# Setting up directories
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


per_type_samples = [0, 0, 0, 0, 0, 0]
already_classified = os.listdir(test)
count = len(already_classified)

for name in already_classified:
    split = name.split("_")
    val = int(split[0])
    count = max(count, int(split[-1].split(".")[0]))
    per_type_samples[val] = per_type_samples[val]+1

print(per_type_samples)
print(count)

todo = os.listdir(unlabelled)
shuffle(todo)


for file in todo:
    if file.startswith('.'):
        continue
    if file.endswith(".jpg"):
        filepath = os.path.join(unlabelled, file)
        # print(filepath)

        img = cv.imread(filepath)
        cv.imshow(view_window, img)

        # Extracting waitKey code to classify images, any code out of range implicitly means bad capture
        res = cv.waitKey(0) - 48
        if 0 <= res <= 5 and per_type_samples[res] < 200:
            testfile = os.path.join(test, str(res) + "_lh_" + str(count) + ".jpg")
            cv.imwrite(testfile, img)
            count = count + 1
            per_type_samples[res] = per_type_samples[res]+1
            if per_type_samples[res] == 200:
                break

        os.remove(filepath)
        cv.destroyAllWindows()
