import numpy as np
from tensorflow.keras.models import load_model
import tensorflow_hub as hub


class OsteoporosisPredictor:
    def __init__(self, model_path):
        self.model = self._load_model(model_path)

    def predict(self, image, image_name):
        y_probs = self.model.predict(np.array([image]))
        y_pred = np.argmax(y_probs[0])
        y_prob = y_probs[0][y_pred]
        print(f"Prediction for image: {image_name} is: {y_pred} with probability: {y_prob}")

        return y_pred, y_prob

    @staticmethod
    def _load_model(model_path):
        model = load_model(model_path, custom_objects={"KerasLayer": hub.KerasLayer})
        return model
