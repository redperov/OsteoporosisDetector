import pytest
from unittest.mock import Mock, patch
import json
from types import SimpleNamespace

from backend.preprocessingComponent.src.utils import send_post_request, validate_predict_request, \
    validate_predict_response, send_knee_rois_detection_request, send_osteoporosis_predict_request


class TestUtils:
    @patch('requests.post')
    def test_send_post_request_when_successful(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'key': 'value'}
        mock_post.return_value = mock_response

        post_response = send_post_request('http://mockapi.com', {})
        mock_post.assert_called_once_with('http://mockapi.com',
                                          data=json.dumps({}), headers={'Content-Type': 'application/json'})
        assert post_response.status_code == 200
        assert post_response.json()

    @patch('requests.post')
    def test_send_post_request_when_fails_with_status_code(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {'key': 'value'}
        mock_post.return_value = mock_response

        with pytest.raises(IOError):
            send_post_request('http://mockapi.com', {})

    def test_validate_predict_request_when_request_is_empty(self):
        request = None
        expected_fields = ['field1', 'field2']
        result = validate_predict_request(request, expected_fields)
        assert 'error' in result

    def test_validate_predict_request_when_request_is_not_a_json(self):
        request = SimpleNamespace(json=json.dumps({'field1': 1}), is_json=False)
        expected_fields = ['field1', 'field2']
        result = validate_predict_request(request, expected_fields)
        assert 'error' in result

    def test_validate_predict_request_when_request_has_missing_fields(self):
        request = SimpleNamespace(json=json.dumps({'field1': 1}), is_json=True)
        expected_fields = ['field1', 'field2']
        result = validate_predict_request(request, expected_fields)
        assert 'error' in result

    def test_validate_predict_request_when_request_is_legal(self):
        request = SimpleNamespace(json=json.dumps({'field1': 1, 'field2': 2}), is_json=True)
        expected_fields = ['field1', 'field2']
        result = validate_predict_request(request, expected_fields)
        assert result is None

    def test_validate_predict_response_when_it_has_no_json(self):
        with pytest.raises(ValueError):
            validate_predict_response({}, [])

    def test_validate_predict_response_when_there_are_missing_fields(self):
        mock_response = Mock()
        mock_response.json.return_value = {}

        with pytest.raises(ValueError):
            validate_predict_response(mock_response, ['field1'])

    def test_validate_predict_response_when_it_is_legal(self):
        mock_response = Mock()
        mock_response.json.return_value = {'field1': 1}

        # This should not raise an error
        validate_predict_response(mock_response, ['field1'])

    @patch('requests.post')
    def test_send_knee_rois_detection_request_when_predictions_are_not_returned(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_post.return_value = mock_response

        with pytest.raises(ValueError):
            send_knee_rois_detection_request("http://dummy.com", None, None,
                                                        None, None, None)

    @patch('requests.post')
    def test_send_knee_rois_detection_request_when_it_is_legal(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'predictions': []}
        mock_post.return_value = mock_response

        post_response = send_knee_rois_detection_request('http://dummy.com', None, None,
                                                         None, None, None)
        assert post_response == []

    @patch('requests.post')
    def test_send_osteoporosis_predict_request_when_prediction_and_probability_are_missing(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_post.return_value = mock_response

        with pytest.raises(ValueError):
            send_osteoporosis_predict_request('http://dummy.com', None, None)

    @patch('requests.post')
    def test_send_osteoporosis_predict_request_when_it_is_legal(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'prediction': 0, 'probability': 0.8}
        mock_post.return_value = mock_response

        post_response = send_osteoporosis_predict_request('http://dummy.com', None, None)
        assert post_response == (0, 0.8)


