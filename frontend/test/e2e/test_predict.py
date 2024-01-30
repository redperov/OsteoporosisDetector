import subprocess
import time
# import pyautogui
import tkinter as tk
from pathlib import Path

from frontend.src.main import OSDetectionApp


class TestApp:
    def test_predict(self):
        python_exe = 'C:\\Users\perov\\anaconda3\\envs\\osteoporosis\\python.exe'
        prediction_component_process = subprocess.Popen([python_exe, '../../../backend/predictionComponent/src/main.py', '&'])
        preprocessing_component_process = subprocess.Popen([python_exe,
                                                            '../../../backend/preprocessingComponent/src/main.py', '&'])

        try:
            time.sleep(15)
            app = OSDetectionApp()
            app.frames['WelcomePage'].go_to_prediction_button.invoke()
            info_label = app.frames['PredictionPage'].info_label
            assert not info_label.cget('text')
            app.frames['PredictionPage'].upload_button.invoke()
            time.sleep(10)
            assert 'Prediction' in info_label.cget('text') and 'Probability' in info_label.cget('text')
        finally:
            prediction_component_process.kill()
            preprocessing_component_process.kill()


