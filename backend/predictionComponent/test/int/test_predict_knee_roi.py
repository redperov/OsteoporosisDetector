import json

import cv2
from pathlib import Path
from unittest.mock import patch, Mock

from backend.predictionComponent.src.main import app
from backend.preprocessingComponent.src.utils import encode_image


class TestFlaskPredictKneeROI:
    DUMMY_PREDICTIONS = [{'class': 'L Knee', 'class_id': 0, 'confidence': 0.9168487787246704, 'height': 348,
                          'image_path': 'N1.jpg', 'prediction_type': 'ObjectDetectionModel', 'width': 324, 'x': 674,
                          'y': 372},
                         {'class': 'R Knee', 'class_id': 1, 'confidence': 0.9031549096107483, 'height': 388,
                          'image_path': 'N1.jpg', 'prediction_type': 'ObjectDetectionModel', 'width': 324, 'x': 202,
                          'y': 370}]

    DUMMY_IMAGE_PATH = Path(r"C:\Users\perov\OneDrive\Desktop\N1.JPEG")

    def test_predict_knee_roi_when_missing_request_image_should_fail(self):
        with app.test_client() as client:
            response = client.post('/predict_knee_roi')
            assert response.status_code == 400

    @patch('backend.predictionComponent.src.predict_handler.KneeDetectionHandler.detect_knee_roi_with_upper_model')
    def test_predict_knee_roi_when_it_should_succeed(self, mock_detect_knee_roi_with_upper_model):
        mock_detect_knee_roi_with_upper_model.return_value = TestFlaskPredictKneeROI.DUMMY_PREDICTIONS

        with app.test_client() as client:
            image = cv2.imread(str(TestFlaskPredictKneeROI.DUMMY_IMAGE_PATH), 0)
            data = {'image': encode_image(image),
                    'image_name': 'N1',
                    'confidence': 50,
                    'overlap': 50,
                    'model_type': 'upper'}
            headers = {'Content-Type': 'application/json'}
            response = client.post('/predict_knee_roi', data=json.dumps(data), headers=headers)
            assert response.status_code == 200
            assert response.json['predictions'] == TestFlaskPredictKneeROI.DUMMY_PREDICTIONS
