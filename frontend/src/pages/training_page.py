import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import uuid
from pathlib import Path
import requests
import json
import base64

from frontend.src.utils import send_predict_request, convert_prediction_to_class
import math


class TrainingPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Training", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        self.delta_training_button = tk.Button(self, text="DELTA TRAINING", command=self.delta_training)
        self.delta_training_button.pack(pady=10)
        self.full_training_button = tk.Button(self, text="FULL TRAINING", command=self.full_training)
        self.full_training_button.pack(pady=10)
        self.stop_training_button = tk.Button(self, text="STOP TRAINING", command=self.stop_training)
        self.stop_training_button.pack_forget()

        self.canvas = tk.Canvas(self, width=200, height=200)
        self.canvas.pack()
        self.arrow = None
        self.angle = 0
        self.is_animating = False

    def delta_training(self):
        self.is_animating = True
        self.add_arrow()

    def full_training(self):
        self.is_animating = True
        self.add_arrow()

    def add_arrow(self):
        self.canvas.pack()
        if self.is_animating:
            if self.arrow is not None:
                self.canvas.delete(self.arrow)
            x1 = 100 + 50 * math.cos(math.radians(self.angle))
            y1 = 100 + 50 * math.sin(math.radians(self.angle))
            x2 = 100 + 50 * math.cos(math.radians(self.angle + 120))
            y2 = 100 + 50 * math.sin(math.radians(self.angle + 120))
            x3 = 100 + 50 * math.cos(math.radians(self.angle + 240))
            y3 = 100 + 50 * math.sin(math.radians(self.angle + 240))
            self.arrow = self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, fill='blue')
            self.angle = (self.angle + 10) % 360
            self.after(100, self.add_arrow)

            self.delta_training_button.pack_forget()
            self.full_training_button.pack_forget()
            self.stop_training_button.pack()

    def stop_training(self):
        self.is_animating = False

        if self.arrow is not None:
            self.canvas.delete(self.arrow)  # Delete the arrow from the canvas
            self.canvas.pack_forget()
            self.arrow = None
        self.delta_training_button.pack(pady=10)
        self.full_training_button.pack(pady=10)
        self.stop_training_button.pack_forget()

    def upload_image(self):
        """
        Uploads an image from the local machine and sends it to the server to make a classification prediction.
        """
        self.info_label.config(text='Loading...')
        self.save_button.pack_forget()
        try:
            # self.info_label.config(text="Loading...")
            # filename = Path(r"C:\Users\perov\OneDrive\Desktop\N1.JPEG")
            filename = filedialog.askopenfilename(initialdir="/", title="Select an Image",
                                                  filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
            filename = Path(filename)
            self._display_predict_result(filename)
        except Exception as e:
            messagebox.showerror("Error", "Error! please try again")
            print("Failed to predict on an image due to:", e)
            self.info_label.config(text='')
            self.save_button.pack_forget()

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
                                f"Image was successfully saved to: {image_to_save_path}")

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
