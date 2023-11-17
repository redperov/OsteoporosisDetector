from flask import jsonify

from backend.predictionComponent.src.handlers.knee_detection_handler import KneeDetectionHandler
from backend.predictionComponent.src.handlers.osteoporosis_prediction_handler import OsteoporosisPredictionHandler
from backend.predictionComponent.src.utils import validate_predict_request

knee_detection_handler = KneeDetectionHandler()
osteoporosis_prediction_handler = OsteoporosisPredictionHandler()


def handle_knee_roi_detection_request(request):
    """
    Handlers a request to detect the knee ROIs in a given image.
    :param request: contains a JSON with an image to detect knee ROIs
    :return: detected knee ROIs
    """
    try:
        expected_fields = ["image", "image_name", "confidence", "overlap", "model_type"]
        request_error = validate_predict_request(request, expected_fields)

        if request_error:
            return jsonify(request_error), 400
        model_type = request.json["model_type"]

        if model_type == "upper":
            predictions = knee_detection_handler.detect_knee_roi_with_upper_model(request.json)
        else:
            predictions = knee_detection_handler.detect_knee_roi_with_lower_model(request.json)
        return jsonify({"predictions": predictions}), 200
    except Exception as e:
        print("Failed to handle knee roi detection request due to:", e)
        return jsonify({"error": "Server encountered unexpected error"}), 500


def handle_osteoporosis_predict_request(request):
    """
        Handlers a request to predict Osteoporosis in a given image.
        :param request: contains a JSON with an image to predict for Osteoporosis
        :return: class label
        """
    try:
        expected_fields = ["image", "image_name"]
        request_error = validate_predict_request(request, expected_fields)

        if request_error:
            return jsonify(request_error), 400
        prediction, probability = osteoporosis_prediction_handler.predict_osteoporosis(request.json)
        return jsonify({"prediction": int(prediction), "probability": float(probability)}), 200
    except Exception as e:
        print("Failed to handle osteoporosis prediction request due to:", e)
        return jsonify({"error": "Server encountered unexpected error"}), 500

