import tkinter as tk
from pathlib import Path

from frontend.src.utils import load_image


class WelcomePage(tk.Frame):
    # WELCOME_IMAGE_PATH = Path(r"C:\Users\perov\PycharmProjects\OsteoporosisDetector\frontend\resources\download.jpg")
    WELCOME_IMAGE_PATH = Path(r"frontend/resources/download.jpg")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        title_label = tk.Label(self, text="Osteoporosis Classification System", font=controller.title_font)
        title_label.pack(side="top", fill="x", pady=10)

        # Load an image and add it to a label
        welcome_image = load_image(WelcomePage.WELCOME_IMAGE_PATH)
        image_label = tk.Label(self, image=welcome_image)
        image_label.image = welcome_image
        image_label.pack(pady=20)

        # self.go_to_prediction_button = tk.Button(self, text="START TESTING",
        #                                          command=lambda: controller.show_frame("PredictionPage"))
        # self.go_to_prediction_button.pack(pady=10)
        # self.go_to_testing_button = tk.Button(self, text="START TRAINING",
        #                                       command=lambda: controller.show_frame("TrainingPage"))
        # self.go_to_testing_button.pack(pady=10)
        intro_label = tk.Label(self, text="AI-powered bone health analysis at your fingertips. Simply upload a knee X-ray image and patient data to receive instant, accurate osteoporosis screening results.",
                               wraplength=309, font=("Arial", 18), justify=tk.LEFT)
        intro_label.pack(pady=10)

        # Create a frame to hold the buttons horizontally
        button_frame = tk.Frame(self)
        button_frame.pack(pady=20)
        
        # Calculate button width to fit within image width (309px) with padding
        # Assuming some padding between buttons and frame edges
        button_width = int((309 - 30) / 2)  # 30px total padding (10px each side + 10px between)
        
        researcher_button = tk.Button(button_frame, text="Researcher", width=15, 
                                    font=("Arial", 12),
                                    command=lambda: controller.show_role_page("researcher"))
        researcher_button.pack(side=tk.LEFT, padx=5)
        
        doctor_button = tk.Button(button_frame, text="Doctor", width=15,
                                font=("Arial", 12),
                                command=lambda: controller.show_role_page("doctor"))
        doctor_button.pack(side=tk.LEFT, padx=5)

        student_and_supervisor_label = tk.Label(self, text="Student:      Danny Perov\nSupervisor: Dr. Maya Herman",
                                              wraplength=309, font=("Arial", 14), justify=tk.LEFT)
        student_and_supervisor_label.pack(pady=30)
        year_label = tk.Label(self, text="2025", font=("Arial", 14), justify=tk.LEFT)
        year_label.pack()
