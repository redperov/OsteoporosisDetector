from unittest.mock import Mock, patch
import numpy as np

from backend.preprocessingComponent.src.predictor import Predictor


class TestPredictor:
    @patch('backend.preprocessingComponent.src.predictor.send_osteoporosis_predict_request')
    def test_predict(self, mock_func):
        mock_func.return_value = (0, 0.8)

        images_dict = {'N1_L': np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])}
        response = Predictor.predict(images_dict)
        assert response == (0, 0.8)