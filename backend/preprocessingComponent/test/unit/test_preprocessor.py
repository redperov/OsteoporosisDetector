from unittest.mock import Mock, patch
import numpy as np

from backend.preprocessingComponent.src.preprocessor import Preprocessor
from backend.preprocessingComponent.src.utils import encode_image

# class TestPreprocessor:
predictions = [{'class': 'L Knee', 'class_id': 0, 'confidence': 0.9168487787246704, 'height': 348,
                'image_path': 'N1.jpg', 'prediction_type': 'ObjectDetectionModel', 'width': 324, 'x': 674, 'y': 372},
               {'class': 'R Knee', 'class_id': 1, 'confidence': 0.9031549096107483, 'height': 388,
                'image_path': 'N1.jpg', 'prediction_type': 'ObjectDetectionModel', 'width': 324, 'x': 202, 'y': 370}]


@patch('backend.preprocessingComponent.src.preprocessor.send_knee_rois_detection_request')
def test_extract_knee_rois_should_succeed(mock_func):
    mock_func.return_value = predictions
    # mock_func.return_value = TestPreprocessor.predictions
    preprocessor = Preprocessor()
    result = preprocessor.extract_knee_rois(encode_image(np.array([[0, 0, 0,], [0, 0, 0], [0, 0, 0]])), 'N1')
    assert 'N1_L' in result and 'N1_R' in result
