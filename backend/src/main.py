# from flask import Flask, request
#
# from backend.src.predict_handler import handle_predict_request
#
# app = Flask(__name__)
#
# # Constants
# HOST = "localhost"
# PORT = 5000
#
#
# @app.route("/")
# def index():
#     return "Welcome to Osteoporosis Detector!\n To perform a prediction use '/predict'"
#
#
# @app.route("/predict", methods=['POST'])
# def predict():
#     response = handle_predict_request(request)
#     return response
#
#
# app.run(host=HOST, port=PORT)

import tensorflow as tf
print(tf.__version__)