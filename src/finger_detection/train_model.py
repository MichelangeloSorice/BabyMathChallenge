import numpy as np
import os
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten
from keras.models import Sequential

path = os.getcwd()
dataset = os.path.join(path, "dataset")

data = np.load(os.path.join(dataset, "images.npy"))
predictions = np.load(os.path.join(dataset, "predictions.npy"))

idx = np.random.permutation(len(data))
data_sh, pred_sh = data[idx], predictions[idx]


num_filters = 3
filter_size = 3
pool_size = 2

model = Sequential([
    Conv2D(num_filters, filter_size, input_shape=(202, 202, 1)),
    MaxPooling2D(pool_size=pool_size),
    Flatten(),
    Dense(6, activation='softmax'),
])

model.compile('adam', loss='categorical_crossentropy', metrics=['accuracy'])

model.fit(
    data_sh, pred_sh, validation_split=0.2, epochs=10
)

model.save_weights(os.path.join(path,'cnn_rawtest.h5'))