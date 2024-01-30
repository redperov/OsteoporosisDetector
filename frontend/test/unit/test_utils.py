from pathlib import Path
from unittest.mock import patch, Mock

import pytest

from frontend.src.utils import send_predict_request


class TestUtils:
    DUMMY_IMAGE_PATH = Path(r"C:\Users\perov\OneDrive\Desktop\N1.JPEG")

    @patch('requests.post')
    def test_send_predict_request_when_fails_with_status_code(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {'key': 'value'}
        mock_post.return_value = mock_response

        with pytest.raises(IOError):
            send_predict_request('', 'http://mockapi.com')

    @patch('requests.post')
    def test_send_predict_request(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'prediction': 0, 'probability': 0.9}
        mock_post.return_value = mock_response

        prediction, probability = send_predict_request(TestUtils.DUMMY_IMAGE_PATH, 'http://mock.com')
        assert prediction == 0 and probability == 0.9

