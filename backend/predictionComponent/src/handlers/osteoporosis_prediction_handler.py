from pathlib import Path

from backend.predictionComponent.src.models.osteoporosis_predictor import OsteoporosisPredictor
from backend.preprocessingComponent.src.utils import decode_image

# Path to trained model
MODEL_PATH = Path(r"C:\Users\perov\PycharmProjects\OsteoporosisDetector\backend\predictionComponent\resources\models\acc_0.69.h5")


class OsteoporosisPredictionHandler:
    def __init__(self):
        self.model = OsteoporosisPredictor(MODEL_PATH)

    def predict_osteoporosis(self, data):
        raw_image = data["image"]
        image_name = data["image_name"]
        decoded_image = decode_image(raw_image)
        # import matplotlib.pyplot as plt
        # plt.imshow(decoded_image, cmap="gray")
        # plt.show()
        return self.model.predict(decoded_image, image_name)