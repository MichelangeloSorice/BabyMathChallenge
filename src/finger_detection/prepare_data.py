from random import shuffle
import numpy as np
import cv2 as cv
import os
from constants import classifier as cls


def dim(cur_shape, scale):
    nwidth = cur_shape[1] * scale / 100
    nheight = cur_shape[0] * scale / 100
    return int(nwidth), int(nheight)


def load_and_prepare(path):
    data, predictions = list(), list()
    raw_files = os.listdir(path)
    shuffle(raw_files)
    width, height, depth = cls["input_shape"]

    for file in raw_files:
        filepath = os.path.join(path, file)
        img = cv.imread(filepath)
        if img is None:
            print('Warning unable to load img: ')
            print(filepath)
            input('Press any key to continue: ')
            continue

        img = cv.resize(img, (width, height), interpolation=cv.INTER_AREA)

        # All 3 channels are identical
        matrix = np.asarray((img[:, :, 0:1] / 255), dtype=int)
        pred = int(file.split('_')[0])

        data.append(matrix)
        predictions.append(pred)

    return np.array(data), np.array(predictions)


# Main script
cwd = os.getcwd()
test_path = os.path.join(cwd, "test")
train_path = os.path.join(cwd, "train")
dataset = os.path.join(cwd, "dataset")

# Preparing training data
train_data, train_predictions = load_and_prepare(train_path)
print("Train set --")
print(train_data.shape)
print(train_predictions.shape)
np.save(os.path.join(dataset, 'train_data'), train_data)
np.save(os.path.join(dataset, 'train_pred'), train_predictions)

# Preparing test data
test_data, test_predictions = load_and_prepare(test_path)
print("Test set --")
print(test_data.shape)
print(test_predictions.shape)
np.save(os.path.join(dataset, 'test_data'), test_data)

np.save(os.path.join(dataset, 'test_pred'), test_predictions)