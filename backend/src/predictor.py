import numpy as np
from tensorflow.keras.models import load_model
import tensorflow_hub as hub
from pathlib import Path

MODEL_PATH = Path(r"C:\Users\perov\PycharmProjects\OsteoporosisDetector\backend\resources\models\acc_0.828.h5")


class Predictor:
    def __init__(self):
        self.model = self._load_model()

    def predict(self, images_dict):
        predictions = []

        for image_name, image in images_dict.items():
            y_probs = self.model.predict(np.array([image]))
            y_pred = np.argmax(y_probs[0])
            y_prob = y_probs[0][y_pred]
            print(f"Prediction for image: {image_name} is: {y_pred} with probability: {y_prob}")
            predictions.append((y_pred, y_prob))

        return max(predictions, key=lambda t: (t[0], t[1]))

    @staticmethod
    def _load_model():
        model = load_model(MODEL_PATH, custom_objects={"KerasLayer": hub.KerasLayer})
        return model
