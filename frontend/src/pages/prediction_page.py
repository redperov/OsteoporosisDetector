import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import uuid
from pathlib import Path
import requests
import json
import base64

from frontend.src.utils import send_predict_request, convert_prediction_to_class

PREDICTOR_URI = "http://localhost:5000/predict"


class PredictionPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Predictor", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        self.upload_button = tk.Button(self, text="UPLOAD AN IMAGE", command=self.upload_image)
        self.upload_button.pack()

        self.info_label = tk.Label(self, text="", wraplength=400, font=8, justify=tk.LEFT, pady=10)
        self.info_label.pack()

        self.image_to_save = None
        self.prediction_to_save = None
        self.save_button = tk.Button(self, text="SAVE RESULT", command=lambda: self.save_result(
            self.image_to_save, self.prediction_to_save))
        self.save_button.pack_forget()

    def upload_image(self):
        """
        Uploads an image from the local machine and sends it to the server to make a classification prediction.
        """
        self.info_label.config(text='Loading...')
        try:
            # self.info_label.config(text="Loading...")
            # filename = Path(r"C:\Users\perov\OneDrive\Desktop\N1.JPEG")
            # TODO uncomment
            filename = filedialog.askopenfilename(initialdir="/", title="Select an Image",
                                                  filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
            filename = Path(filename)
            self._display_predict_result(filename)
        except Exception as e:
            # self.info_label.config(text="")
            messagebox.showerror("Error", "Error! please try again")
            print("Failed to predict on an image due to:", e)
            self.info_label.config(text='')
        # finally:
            # self.info_label.config(text="")

    def save_result(self, image, prediction):
        """
        Saves the uploaded image in a selected directory on the local machine with the predicted classification.
        :param image: image to predict on
        :param prediction: classification prediction
        """
        try:
            directory = filedialog.askdirectory()
            filename = f"{uuid.uuid4()}_{prediction}"
            image_to_save_path = Path(f"{directory}/{filename}.jpg")
            image.save(image_to_save_path)
            messagebox.showinfo("Save succeeded",
                                f"Image was successfully save to: {image_to_save_path}")

            # Clear prediction result after saving the image
            self.info_label.config(text="")
            self.save_button.pack_forget()
        except Exception as e:
            messagebox.showerror("Save failed", "Failed saving image")
            print("Failed to save image due to:", e)

    def _display_predict_result(self, filename):
        """
        Sends the prediction request to the server and then displays the prediction on the window for the user to view.
        :param filename: path to image for prediction
        """
        if not filename:
            return
        image = Image.open(filename)

        try:
            prediction, probability = send_predict_request(filename, PREDICTOR_URI)
        except Exception as e:
            messagebox.showerror("Prediction failed",
                                 "Failed to perform prediction, try again")
            print(f"Failed to predict due to:", e)
            return
        prediction_class = convert_prediction_to_class(prediction)

        probability = round(float(probability), 3)
        self.info_label.config(text=f"Selected image: {filename}\n\n"
                                    f"Prediction: {prediction_class}\n\n"
                                    f"Probability: {probability}")
        print("Image selected:", filename)
        self.image_to_save = image
        self.prediction_to_save = prediction_class
        self.save_button.pack()
