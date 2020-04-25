import numpy as np
import cv2 as cv
import os
from keras.utils.np_utils import to_categorical

path = os.getcwd()
test = os.path.join(path, "test")
dataset = os.path.join(path, "dataset")
data = list()
predictions = list()

for file in os.listdir(test):
    filepath = os.path.join(test, file)
    img = cv.imread(filepath)
    if img is None:
        print(filepath)
        continue
    # All 3 channels are identical
    matrix = np.asarray((img[:, :, 0:1] / 255), dtype=int)
    pred = int(file.split('_')[0])
    data.append(matrix)
    predictions.append(pred)

predictions = to_categorical(np.array(predictions))
print(predictions.shape)
np.save(os.path.join(dataset, 'images'), np.array(data))
np.save(os.path.join(dataset, 'predictions'), predictions)