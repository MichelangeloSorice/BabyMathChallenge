import numpy as np
import os

from keras.callbacks import EarlyStopping
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, AveragePooling2D, Dropout
from keras.models import Sequential

path = os.getcwd()
dataset = os.path.join(path, "dataset")

# loading data
data = np.load(os.path.join(dataset, "images.npy"))
predictions = np.load(os.path.join(dataset, "predictions.npy"))

# Shuffling data
idx = np.random.permutation(len(data))
data_sh, pred_sh = data[idx], predictions[idx]


overfitCallback = EarlyStopping(monitor='loss', min_delta=0, patience=4)

num_filters = 2
filter_size = 2
pool_size = 2

model = Sequential([
    Conv2D(32, kernel_size=(3, 3), input_shape=(202, 202, 1), activation='relu'),
    Conv2D(64, kernel_size=(3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Dropout(0.25),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(6, activation='softmax'),
])

model.compile('adam', loss='categorical_crossentropy', metrics=['accuracy'])

model.fit(
    data_sh, pred_sh, validation_split=0.3, epochs=12, callbacks=[overfitCallback]
)

model.save_weights(os.path.join(path,'cnn_rawtest.h5'))