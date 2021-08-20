import tensorflow as tf
import numpy as np
from flask import current_app
from PIL import Image


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ServerModel(metaclass=Singleton):

    def __init__(self):
        self.model = tf.keras.models.load_model(current_app.config['MODEL_DIR'] + '/server_model')
        assert isinstance(self.model, tf.keras.Model)

    def __call__(self, img):
        assert isinstance(img, Image.Image)
        img = np.array(img.crop((0, 0, 256, 256)))[None, :, :, :]
        img = np.transpose(img, axes=[3, 1, 2, 0])
        predictions = self.model.predict(img)
        return [(np.argmax(p), np.around(max(p) * 100, decimals=2)) for p in predictions]
