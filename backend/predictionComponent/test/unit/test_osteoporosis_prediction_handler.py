from unittest.mock import patch
import numpy as np

from backend.predictionComponent.src.handlers.osteoporosis_prediction_handler import OsteoporosisPredictionHandler


class TestOsteoporosisPredictionHandler:
    @patch('backend.predictionComponent.src.handlers.osteoporosis_prediction_handler.OsteoporosisPredictor')
    @patch('backend.predictionComponent.src.handlers.osteoporosis_prediction_handler.decode_image')
    def test_predict_osteoporosis(self, mock_func, mock_obj):
        mock_obj.return_value.predict.return_value = (0, 0.7)
        mock_func.return_value = None

        osteoporosis_prediction_handler = OsteoporosisPredictionHandler()
        result = osteoporosis_prediction_handler.predict_osteoporosis(data={'image': np.array([[0, 0, 0]]),
                                                                            'image_name': 'N1'})
        assert result == (0, 0.7)
