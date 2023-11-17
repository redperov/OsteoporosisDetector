from flask import jsonify

from backend.preprocessingComponent.src.predictor import Predictor
from backend.preprocessingComponent.src.preprocessor import Preprocessor


class PredictHandler:
    def __init__(self):
        self.preprocessor = Preprocessor()
        self.predictor = Predictor()

    def handle_predict_request(self, request):
        """
        Receives a prediction request, makes a prediction using the model and returns a response to the client.
        :param request: request JSON data
        :return: prediction response as a JSON and an HTTP status code
        """
        try:
            request_error = self.__validate_predict_request(request)

            if request_error:
                return jsonify(request_error), 400
            prediction, probability = self._predict(request.json)
            return jsonify({"prediction": int(prediction), "probability": float(probability)}), 200
        except Exception as e:
            print("Failed to handle predict request due to:", e)
            return jsonify({"error": "Server encountered unexpected error"}), 500

    def _predict(self, data):
        """
        Performs an osteoporosis prediction on the given data.
        :param data: JSON containing an image and image name
        :return: prediction and its probability
        """
        image = data["image"]
        image_name = data["image_name"]
        print("Received image for prediction:", image_name)

        knee_rois_dict = self.preprocessor.extract_knee_rois(image, image_name)
        print(f"Extracted {len(knee_rois_dict)} ROIs")

        prediction, probability = self.predictor.predict(knee_rois_dict)
        print(f"Predicted: {prediction} with probability: {probability}")
        return prediction, probability

    @staticmethod
    def __validate_predict_request(request):
        """
        Checks that the request is a valid JSON containing all the required request fields.
        :param request: client request
        :return: error message if the request is not valid, None otherwise
        """
        expected_fields = ["image"]

        if not request:
            return {"error": "Request can't be empty"}

        if not request.is_json:
            return {"error": "Request body must be JSON"}

        for field in expected_fields:
            if field not in request.json:
                return {"error": f"{field} is required"}
        return None
