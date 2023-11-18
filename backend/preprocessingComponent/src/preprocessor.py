import numpy as np
import cv2
# from roboflow import Roboflow
import base64
from pathlib import Path
import requests
import json

from backend.preprocessingComponent.src.utils import validate_predict_response, send_knee_rois_detection_request, \
    decode_image

KNEE_ROI_DETECTION_URI = "http://localhost:5001/predict_knee_roi"
TEMP_IMAGES_DIR = Path("../../resources/temp_images")
RESHAPED_IMAGE_SIZE = (224, 224)

class Preprocessor:
    # def __init__(self):
        # rf = Roboflow(api_key="jeaBuRI3CrFlPbUFiwjn")
        # project = rf.workspace().project("knee-localization")
        # self.model_upper = project.version(1).model
        #
        # rf = Roboflow(api_key="0Od18TnlofLc2tDnGyvg")
        # project = rf.workspace().project("knee-detector")
        # self.model_lower = project.version(1).model

    def extract_knee_rois(self, raw_image, image_name):
        knee_rois_dict = {}
        # image_path = self._save_temp_image(raw_image, image_name)

        if image_name[0].isupper():
            print("Extracting ROIs from:", image_name, " Using model upper")
            bounding_boxes_dict = self._find_knee_bounding_boxes(raw_image, image_name, model_type="upper",
                                                                 confidence=50, overlap=50, max_rois=2)
        else:
            print("Extracting ROIs from:", image_name, " Using model lower")
            bounding_boxes_dict = self._find_knee_bounding_boxes(raw_image, image_name, model_type="lower",
                                                                 confidence=50, overlap=50, max_rois=1)
        print(f"Found {len(bounding_boxes_dict)} ROIs")
        # image = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
        image = decode_image(raw_image)

        for knee_side, (x1, x2, y1, y2) in bounding_boxes_dict.items():
            knee_roi_image = image[y1:y2, x1:x2]
            reshaped_knee_roi_image = self._reshape_image(knee_roi_image, RESHAPED_IMAGE_SIZE, is_rgb=True)
            roi_key_name = f"{image_name}_{knee_side}"
            print("ROI name:", roi_key_name)
            knee_rois_dict[roi_key_name] = reshaped_knee_roi_image
        print()

        return knee_rois_dict

    @staticmethod
    def _save_temp_image(encoded_image, image_name):
        image_bytes = base64.b64decode(encoded_image)
        image_path = TEMP_IMAGES_DIR / f"{image_name}.jpg"

        with open(image_path, "wb") as temp_image_file:
            temp_image_file.write(image_bytes)
        return image_path
        # image_arr = np.frombuffer(image_bytes, dtype=np.uint8)
        # image = cv2.imdecode(image_arr, flags=cv2.IMREAD_GRAYSCALE)
        # return image

    def _find_knee_bounding_boxes(self, raw_image, image_name, model_type, confidence, overlap, max_rois):
        # predict_result = model.predict(image_path, confidence=confidence, overlap=overlap).json()
        # predictions = predict_result["predictions"]
        predictions = send_knee_rois_detection_request(KNEE_ROI_DETECTION_URI, raw_image, image_name,
                                                       model_type, confidence, overlap)
        bounding_boxes_dict = {}

        # If there are move than two predictions, keep the top two according to the confidence score
        if len(predictions) > max_rois:
            print(f"Found more than {max_rois} predictions: {len(predictions)} removing unnecessary ones...")
            predictions.sort(key=lambda prediction: prediction["confidence"], reverse=True)
            predictions = predictions[:max_rois]

        for prediction in predictions:
            box = self._extract_bounding_box_coordinates(prediction)
            knee_side = self._validate_knee_roi_keys(bounding_boxes_dict, prediction["class"][0])
            bounding_boxes_dict[knee_side] = box

        return bounding_boxes_dict



    @staticmethod
    def _extract_bounding_box_coordinates(prediction):
        x1 = int(prediction['x'] - prediction['width'] / 2)
        x2 = int(prediction['x'] + prediction['width'] / 2)
        y1 = int(prediction['y'] - prediction['height'] / 2)
        y2 = int(prediction['y'] + prediction['height'] / 2)
        return x1, x2, y1, y2

    @staticmethod
    def _validate_knee_roi_keys(knee_dict, knee_side):
        if knee_side in knee_dict:
            print(f"Duplicate key {knee_side}, removing knee side!!!!!!!!!!!!!!!!!!")
            return '?'
        return knee_side

    @staticmethod
    def _reshape_image(image, shape, is_rgb=False):
        reshaped_img = image.reshape(image.shape[0], image.shape[1], 1)
        reshaped_img = reshaped_img / 255.0
        reshaped_img = reshaped_img.astype(np.float32)
        reshaped_img = cv2.resize(reshaped_img, shape)

        if is_rgb:
            reshaped_img = cv2.cvtColor(reshaped_img, cv2.COLOR_GRAY2RGB)
        return reshaped_img
        # resized_images_dict = {image_name: cv2.resize(image, RESHAPED_IMAGE_SIZE)
        #                        for image_name, image in images_dict.items()}
        # reshaped_images_dict = {image_name: image.reshape(image.shape[0], image.shape[1], image.shape[2], 1)
        #                         for image_name, image in resized_images_dict.items()}
        # return reshaped_images_dict




