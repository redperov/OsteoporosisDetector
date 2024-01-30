import json

import cv2
from pathlib import Path
from unittest.mock import patch, Mock

from backend.predictionComponent.src.main import app
from backend.preprocessingComponent.src.utils import encode_image


class TestFlaskPredictOsteoporosis:
    DUMMY_IMAGE_PATH = Path(r"C:\Users\perov\OneDrive\Desktop\N1.JPEG")

    def test_predict_osteoporosis_when_missing_request_image_should_fail(self):
        with app.test_client() as client:
            response = client.post('/predict_osteoporosis')
            assert response.status_code == 400

    @patch('backend.predictionComponent.src.predict_handler.OsteoporosisPredictionHandler.predict_osteoporosis')
    def test_predict_osteoporosis_when_it_should_succeed(self, mock_predict_osteoporosis):
        mock_predict_osteoporosis.return_value = (0, 0.9)

        with app.test_client() as client:
            image = cv2.imread(str(TestFlaskPredictOsteoporosis.DUMMY_IMAGE_PATH), 0)
            data = {'image': encode_image(image), 'image_name': 'N1'}
            headers = {'Content-Type': 'application/json'}
            response = client.post('/predict_osteoporosis', data=json.dumps(data), headers=headers)
            assert response.status_code == 200
            assert response.json['prediction'] == 0 and response.json['probability'] == 0.9