from flask import Flask, request

from backend.predictionComponent.src.predict_handler import handle_knee_roi_detection_request, \
    handle_osteoporosis_predict_request

app = Flask(__name__)

# Constants
HOST = "localhost"
PORT = 5001


@app.route("/")
def welcome():
    return "Welcome to the classification component"


@app.route("/predict_knee_roi", methods=['POST'])
def predict_knee_roi():
    response = handle_knee_roi_detection_request(request)
    return response


@app.route("/predict_osteoporosis", methods=['POST'])
def predict_osteoporosis():
    response = handle_osteoporosis_predict_request(request)
    return response


app.run(host=HOST, port=PORT)
