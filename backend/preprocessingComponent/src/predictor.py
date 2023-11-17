import numpy as np
# from tensorflow.keras.models import load_model
# import tensorflow_hub as hub
from pathlib import Path


class Predictor:
    # def __init__(self):
        # self.model = self._load_model(MODEL_PATH)

    def predict(self, images_dict):
        """
        Given a dictionary of images that represent the same object, predict the classification for each individual
        image and then return as result the class with the highest value from all the resulted predictions.
        :param images_dict: dictionary of images
        :return: class label
        """
        predictions = []

        for image_name, image in images_dict.items():
            y_probs = self.__predict(np.array([image]))
            y_pred = np.argmax(y_probs[0])
            y_prob = y_probs[0][y_pred]
            print(f"Prediction for image: {image_name} is: {y_pred} with probability: {y_prob}")
            predictions.append((y_pred, y_prob))

        return max(predictions, key=lambda t: (t[0], t[1]))

    @staticmethod
    def __predict(image):
        # TODO extract from JSON class and prob
        pass
    # @staticmethod
    # def _load_model(model_path):
    #     model = load_model(model_path, custom_objects={"KerasLayer": hub.KerasLayer})
    #     return model
