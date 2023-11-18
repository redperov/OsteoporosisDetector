from roboflow import Roboflow


class KneeDetector:
    def __init__(self, api_key, project_name):
        self.model = self._load_model(api_key, project_name)

    def detect(self, image_path, confidence, overlap):
        predict_result = self.model.predict(str(image_path), confidence=confidence, overlap=overlap).json()
        predictions = predict_result["predictions"]
        return predictions

    @staticmethod
    def _load_model(api_key, project_name):
        rf = Roboflow(api_key=api_key)
        project = rf.workspace().project(project_name)
        model = project.version(1).model
        return model

