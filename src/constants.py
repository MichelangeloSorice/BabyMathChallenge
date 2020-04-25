# Constants
gui_constants = {
    "images_dir": "./gui/images/",
    "cam_placeholder": "video-camera-icon.jpg",
    "fps": 1000.0/60
}

classifier = {
    # num_filters, filters_size, pool_size
    "model_parameters": [3, 3, 2],
    "input_shape": (202, 202, 1),
    # crop parameters for p1 and p2
    "player1": [0, 202, 128, 330],
    "player2": [0, 202, 128, 330]
}

