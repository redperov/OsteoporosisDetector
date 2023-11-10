from tensorflow.keras.models import load_model
import tensorflow_hub as hub
from pathlib import Path

MODEL_PATH = Path(r"C:\Users\Danny\PycharmProjects\OsteoporosisProject\backend\resources\acc_0.828_2023_09_09_053222.h5")


def load_osteoporosis_detection_model():
    model = load_model(MODEL_PATH, custom_objects={"KerasLayer": hub.KerasLayer})
    return model
