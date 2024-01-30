import numpy as np
import cv2
import base64
import json
import requests


def send_post_request(url, data):
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(data), headers=headers)

    if response.status_code != 200:
        print(f"POST request to {url} failed with status code {response.status_code} "
              f"and response: {response.json()}")
        raise IOError("Failed to perform POST request")
    print(f"POST request to {url} succeeded with response: {response}")
    return response


def validate_predict_request(request, expected_fields):
    """
    Checks that the request is a valid JSON containing all the required request fields.
    :param request: client request
    :param expected_fields: fields that are expected to be in the request JSON
    :return: error message if the request is not valid, None otherwise
    """
    if not request:
        return {"error": "Request can't be empty"}

    if not request.is_json:
        return {"error": "Request body must be JSON"}

    for field in expected_fields:
        if field not in request.json:
            return {"error": f"{field} is required"}
    return None


def validate_predict_response(response, expected_fields):
    """
    Validate that the returned response from the server for the prediction request is valid.
    :param response: server prediction response
    :param expected_fields: expected fields in response JSON
    """
    try:
        data = response.json()
    except Exception:
        raise ValueError("Response from server must be a JSON")

    for field in expected_fields:
        if field not in data:
            raise ValueError(f"{field} is missing from response JSON")


def send_knee_rois_detection_request(url, raw_image, image_name, model_type, confidence, overlap):
    data = {
        "image": raw_image,
        "image_name": image_name,
        "model_type": model_type,
        "confidence": confidence,
        "overlap": overlap,
    }
    response = send_post_request(url, data)
    validate_predict_response(response, expected_fields=["predictions"])
    response_data = response.json()
    predictions = response_data["predictions"]
    return predictions


def send_osteoporosis_predict_request(url, raw_image, image_name):
    data = {
        "image": raw_image,
        "image_name": image_name,
    }
    response = send_post_request(url, data)
    validate_predict_response(response, expected_fields=["prediction", "probability"])
    response_data = response.json()
    prediction, probability = response_data["prediction"], response_data["probability"]
    return prediction, probability


def encode_image(image):
    _, buffer = cv2.imencode('.JPEG', image)
    jpeg_as_text = base64.b64encode(buffer).decode()
    return jpeg_as_text


def decode_image(raw_image):
    image_bytes = base64.b64decode(raw_image)
    np_arr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)
    image = image.astype(np.float32)
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    return image
