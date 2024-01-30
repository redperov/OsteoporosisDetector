import cv2
import json
from pathlib import Path
from unittest.mock import patch

from backend.preprocessingComponent.src.main import app
from backend.preprocessingComponent.src.utils import encode_image


class TestFlaskPredict:
    DUMMY_PREDICTIONS = [{'class': 'L Knee', 'class_id': 0, 'confidence': 0.9168487787246704, 'height': 348,
                    'image_path': 'N1.jpg', 'prediction_type': 'ObjectDetectionModel', 'width': 324, 'x': 674,
                    'y': 372},
                         {'class': 'R Knee', 'class_id': 1, 'confidence': 0.9031549096107483, 'height': 388,
                    'image_path': 'N1.jpg', 'prediction_type': 'ObjectDetectionModel', 'width': 324, 'x': 202,
                    'y': 370}]

    DUMMY_IMAGE_PATH = Path(r"C:\Users\perov\OneDrive\Desktop\N1.JPEG")

    def test_welcome_message(self):
        with app.test_client() as client:
            response = client.get('/')
            assert response.data == b"Welcome to Osteoporosis Detector!\n To perform a prediction use '/predict'"
        #

    def test_predict_when_missing_request_image_should_fail(self):
        with app.test_client() as client:
            response = client.post('/predict')
            assert response.status_code == 400

    @patch('backend.preprocessingComponent.src.preprocessor.send_knee_rois_detection_request')
    @patch('backend.preprocessingComponent.src.predictor.send_osteoporosis_predict_request')
    def test_predict_when_it_should_succeed(self, mock_send_osteoporosis_predict_request,
                                            mock_send_knee_rois_detection_request):
        mock_send_knee_rois_detection_request.return_value = TestFlaskPredict.DUMMY_PREDICTIONS
        mock_send_osteoporosis_predict_request.return_value = (0, 0.7)

        with app.test_client() as client:
            image = cv2.imread(str(TestFlaskPredict.DUMMY_IMAGE_PATH), 0)
            data = {'image': encode_image(image), 'image_name': 'N1'}
            headers = {'Content-Type': 'application/json'}
            response = client.post('/predict', data=json.dumps(data), headers=headers)
            assert response.status_code == 200
            assert response.json['prediction'] == 0 and response.json['probability'] == 0.7