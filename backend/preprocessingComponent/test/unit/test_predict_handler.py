from unittest.mock import patch, Mock

from backend.preprocessingComponent.src.predict_handler import PredictHandler


class TestPredictHandler:
    def test_handle_predict_request_when_request_is_none(self):
        mock_request = None

        predict_handler = PredictHandler()
        response = predict_handler.handle_predict_request(mock_request)
        assert 'error' in response

    def test_handle_predict_request_when_request_is_missing_fields(self):
        mock_request = Mock()
        mock_request.is_json = True
        mock_request.json = {}

        predict_handler = PredictHandler()
        response = predict_handler.handle_predict_request(mock_request)
        assert 'error' in response

    @patch('backend.preprocessingComponent.src.predict_handler.extract_knee_rois')
    @patch('backend.preprocessingComponent.src.predict_handler.predict')
    def test_handle_predict_request_when_it_is_successful(self, mock_extract_knee_rois, mock_predict):
        mock_request = Mock()
        mock_request.is_json = True
        mock_request.json = {'image': None}

        mock_extract_knee_rois.return_value = {}
        mock_predict.return_value = (0, 0.8)

        predict_handler = PredictHandler()
        response = predict_handler.handle_predict_request(mock_request)
        assert 'prediction' in response and 'probability' in response


