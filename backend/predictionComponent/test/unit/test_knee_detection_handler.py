from unittest.mock import patch
import numpy as np

from backend.predictionComponent.src.handlers.knee_detection_handler import KneeDetectionHandler


class TestKneeDetectionHandler:
    @patch('backend.predictionComponent.src.handlers.knee_detection_handler.KneeDetector')
    def test_detect_knee_roi_with_upper_model(self, mock_obj):
        mock_obj.return_value.detect.return_value = {}

        knee_detection_handler = KneeDetectionHandler()
        result = knee_detection_handler.detect_knee_roi_with_upper_model(data={'image': np.array([[0, 0, 0]]),
                                                                               'image_name': 'N1',
                                                                               'confidence': 50,
                                                                               'overlap': 50})
        assert result == {}

    @patch('backend.predictionComponent.src.handlers.knee_detection_handler.KneeDetector')
    def test_detect_knee_roi_with_lower_model(self, mock_obj):
        mock_obj.return_value.detect.return_value = {}

        knee_detection_handler = KneeDetectionHandler()
        result = knee_detection_handler.detect_knee_roi_with_lower_model(data={'image': np.array([[0, 0, 0]]),
                                                                               'image_name': 'N1',
                                                                               'confidence': 50,
                                                                               'overlap': 50})
        assert result == {}
