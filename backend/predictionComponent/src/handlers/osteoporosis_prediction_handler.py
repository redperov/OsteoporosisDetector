from pathlib import Path

from backend.predictionComponent.src.models.osteoporosis_predictor import OsteoporosisPredictor

# Path to trained model
MODEL_PATH = Path("../../resources/models/acc_0.828.h5")


class OsteoporosisPredictionHandler:
    def __init__(self):
        self.model = OsteoporosisPredictor(MODEL_PATH)

    def predict_osteoporosis(self, data):
        image = data["image"]
        image_name = data["image_name"]
        return self.model.predict(image, image_name)