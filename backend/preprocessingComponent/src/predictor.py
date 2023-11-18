from backend.preprocessingComponent.src.utils import send_osteoporosis_predict_request, encode_image

OSTEOPOROSIS_PREDICTION_URI = "http://localhost:5001/predict_osteoporosis"


class Predictor:

    @staticmethod
    def predict(images_dict):
        """
        Given a dictionary of images that represent the same object, predict the classification for each individual
        image and then return as result the class with the highest value from all the resulted predictions.
        :param images_dict: dictionary of images
        :return: class label
        """
        predictions = []

        for image_name, image in images_dict.items():
            encoded_image = encode_image(image)
            y_pred, y_prob = send_osteoporosis_predict_request(OSTEOPOROSIS_PREDICTION_URI, encoded_image, image_name)
            # y_probs = self.__predict(np.array([image]))
            # y_pred = np.argmax(y_probs[0])
            # y_prob = y_probs[0][y_pred]
            print(f"Prediction for image: {image_name} is: {y_pred} with probability: {y_prob}")
            predictions.append((y_pred, y_prob))

        return max(predictions, key=lambda t: (t[0], t[1]))
