from flask import jsonify

from backend.src.model import load_osteoporosis_detection_model


def handle_predict_request(request):
    try:
        request_error = validate_predict_request(request)

        if request_error:
            return jsonify(request_error), 400
        prediction, accuracy = predict(request.json)
        return jsonify({"prediction": prediction, "accuracy": accuracy}), 200
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
    model = load_osteoporosis_detection_model()
    prediction = model.predict(image)
    return prediction
    # return 0, 0.94
