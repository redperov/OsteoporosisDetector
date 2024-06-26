from flask import Flask, request

from backend.preprocessingComponent.src.predict_handler import PredictHandler

app = Flask(__name__)

# Constants
HOST = "localhost"
PORT = 5000

predict_handler = PredictHandler()


@app.route("/", methods=['GET'])
def index():
    return "Welcome to Osteoporosis Classifier!\n To perform a classification use '/predict'"


@app.route("/predict", methods=['POST'])
def predict():
    response = predict_handler.handle_predict_request(request)
    return response


app.run(host=HOST, port=PORT)