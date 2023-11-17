import base64
from pathlib import Path
from backend.predictionComponent.src.models.knee_detector import KneeDetector

UPPER_MODEL_API_KEY = "jeaBuRI3CrFlPbUFiwjn"
UPPER_MODEL_PROJECT_NAME = "knee-localization"

LOWER_MODEL_API_KEY = "0Od18TnlofLc2tDnGyvg"
LOWER_MODEL_PROJECT_NAME = "knee-detector"

TEMP_IMAGES_DIR = Path("../../resources/temp_images")


class KneeDetectionHandler:
    def __init__(self):
        self.upper_model = KneeDetector(UPPER_MODEL_API_KEY, UPPER_MODEL_PROJECT_NAME)
        self.lower_model = KneeDetector(LOWER_MODEL_API_KEY, LOWER_MODEL_PROJECT_NAME)

    def detect_knee_roi_with_upper_model(self, data):
        image_path, confidence, overlap = self.__extract_request_fields(data)
        return self.upper_model.detect(image_path, confidence, overlap)

    def detect_knee_roi_with_lower_model(self, data):
        image_path, confidence, overlap = self.__extract_request_fields(data)
        return self.lower_model.detect(image_path, confidence, overlap)

    def __extract_request_fields(self, data):
        image, image_name, confidence, overlap = data['image'], data['image_name'], data['confidence'], data['overlap']
        image_path = self._save_temp_image(image, image_name)
        return image_path, confidence, overlap

    @staticmethod
    def _save_temp_image(encoded_image, image_name):
        image_bytes = base64.b64decode(encoded_image)
        image_path = TEMP_IMAGES_DIR / f"{image_name}.jpg"

        with open(image_path, "wb") as temp_image_file:
            temp_image_file.write(image_bytes)
        return image_path
