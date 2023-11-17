import tkinter as tk
from pathlib import Path

from frontend.src.utils import load_image


class WelcomePage(tk.Frame):
    WELCOME_IMAGE_PATH = Path(r"C:\Users\perov\PycharmProjects\OsteoporosisDetector\frontend\resources\download.jpg")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        title_label = tk.Label(self, text="Osteoporosis Detector", font=controller.title_font)
        title_label.pack(side="top", fill="x", pady=10)

        # Load an image and add it to a label
        welcome_image = load_image(WelcomePage.WELCOME_IMAGE_PATH)
        image_label = tk.Label(self, image=welcome_image)
        image_label.image = welcome_image
        image_label.pack(pady=20)

        go_to_prediction_button = tk.Button(self, text="START PREDICTING",
                                            command=lambda: controller.show_frame("PredictionPage"))
        go_to_prediction_button.pack(pady=10)

        student_and_lecturer_label = tk.Label(self, text="Student: Danny Perov\nLecturer: Dr. Maya Herman",
                                              wraplength=400, font=8, justify=tk.LEFT)
        student_and_lecturer_label.pack(pady=5)