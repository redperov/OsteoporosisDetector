from flask import jsonify

from backend.src.predictor import Predictor
from backend.src.preprocessor import Preprocessor

preprocessor = Preprocessor()
predictor = Predictor()


def handle_predict_request(request):
    try:
        request_error = validate_predict_request(request)

        if request_error:
            return jsonify(request_error), 400
        prediction, probability = predict(request.json)
        return jsonify({"prediction": int(prediction), "probability": float(probability)}), 200
    except Exception as e:
        print("Failed to handle predict request due to:", e)
        return jsonify({"error": "Server encountered unexpected error"}), 500


def validate_predict_request(request):
    expected_fields = ["image"]

    if not request.is_json:
        return {"error": "Request body must be JSON"}

    for field in expected_fields:
        if field not in request.json:
            return {"error": f"{field} is required"}
    return None


def predict(data):
    image = data["image"]
    image_name = data["image_name"]
    print("Received image for prediction:", image_name)

    knee_rois_dict = preprocessor.extract_knee_rois(image, image_name)
    print(f"Extracted {len(knee_rois_dict)} ROIs")

    prediction, probability = predictor.predict(knee_rois_dict)
    print(f"Predicted: {prediction} with probability: {probability}")
    return prediction, probability
    # return 0, 0.94
