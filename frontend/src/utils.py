import base64
import json

import requests
from PIL import Image, ImageTk


def get_window_center_coordinates(root, desired_window_height, desired_window_width):
    # Get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate position coordinates
    position_top = int(screen_height / 2 - desired_window_height / 2)
    position_right = int(screen_width / 2 - desired_window_width / 2)

    return position_right, position_top


def load_image(image_path):
    """
    Loads an image from the given path.
    :param image_path: path of image to load
    :return: loaded image
    """
    image = Image.open(image_path)
    photo = ImageTk.PhotoImage(image)
    return photo


def send_predict_request(filename, url):
    """
    Performs a post request to the server to make a prediction on the received image.
    :param filename: path to image for prediction
    :return: predicted class and prediction probability
    """
    # TODO add rotation mark while waiting for response from server
    with open(filename, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('ascii')
    data = {"image": encoded_image, "image_name": filename.stem}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    if response.status_code != 200:
        print(f"POST request failed with status code {response.status_code} "
              f"and response: {response.json()}")
        raise IOError("Failed to perform POST request")
    print(f"POST request succeeded with response: {response.json()}")
    validate_predict_response(response)
    prediction, probability = extract_predict_response(response.json())
    return prediction, probability


def convert_prediction_to_class(prediction):
    """
    Convert the prediction to a textual class.
    :param prediction: predicted number class
    :return: predicted class string
    """
    if prediction == 0:
        return "Osteoporosis"
    elif prediction == 1:
        return "Osteopenia"
    elif prediction == 2:
        return "Healthy"
    else:
        raise ValueError(f"Illegal prediction value: {prediction}")


def validate_predict_response(response):
    """
    Validate that the returned response from the server for the prediction request is valid.
    :param response: server prediction response
    """
    expected_fields = ["prediction", "probability"]

    try:
        data = response.json()
    except ValueError:
        raise ValueError("Response from server must be a JSON")

    for field in expected_fields:
        if field not in data:
            raise ValueError(f"{field} is missing from response JSON")


def extract_predict_response(data):
    """
    Extracts fields from the prediction response.
    :param data: server response data
    :return: prediction response fields
    """
    return data["prediction"], data["probability"]