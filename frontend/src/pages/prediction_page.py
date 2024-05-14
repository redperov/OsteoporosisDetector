import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import uuid
from pathlib import Path
import requests
import json
import base64
import csv

from frontend.src.utils import send_predict_request, convert_prediction_to_class

PREDICTOR_URI = "http://localhost:5000/predict"
DISPLAYED_IMAGE_SIZE = 230

class PredictionPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Predictor", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        self.image_to_save = None
        self.prediction_to_save = None
        self.image_path = None
        self.loaded_image_label = tk.Label(self)
        self.loaded_image_path_label = tk.Label(self, font=8, justify=tk.LEFT)
        self.loaded_csv_label = tk.Label(self, font=8, justify=tk.LEFT)

        self.upload_image_button = tk.Button(self, text="UPLOAD AN IMAGE", command=self.upload_image)
        self.upload_csv_button = tk.Button(self, text="UPLOAD A CSV FILE", command=self.upload_csv)
        self.predict_button = tk.Button(self, text="PREDICT", command=self.predict)
        self.info_label = tk.Label(self, text="", wraplength=400, font=8, justify=tk.LEFT, pady=10)
        self.save_button = tk.Button(self, text="SAVE RESULT", command=lambda: self.save_result(
            self.image_to_save, self.prediction_to_save))

        self.upload_image_button.pack()
        self.predict_button.pack_forget()
        self.info_label.pack_forget()
        self.save_button.pack_forget()
        self.loaded_image_label.pack_forget()
        self.loaded_image_path_label.pack_forget()
        self.loaded_csv_label.pack_forget()

    def upload_image(self):
        """
        Uploads an image from the local machine and sends it to the server to make a classification prediction.
        """
        # self.info_label.config(text='Loading...')
        self.save_button.pack_forget()
        try:
            # self.info_label.config(text="Loading...")
            # filename = Path(r"C:\Users\perov\OneDrive\Desktop\N1.JPEG")
            filename = filedialog.askopenfilename(initialdir="/", title="Select an Image",
                                                  filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
            self._display_image(filename)
            self.image_path = Path(filename)
            self.upload_image_button.pack_forget()
            self.loaded_image_path_label.config(text=f'Patient image:\n{filename}')
            self.loaded_image_path_label.pack()
            self.upload_csv_button.pack(pady=10)
        except Exception as e:
            messagebox.showerror("Error", "Error! please try again")
            print("Failed to predict on an image due to:", e)
            self.info_label.config(text='')
            self.save_button.pack_forget()

    def upload_csv(self):
        filename = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not filename:
            raise ValueError(f"Can't read a file named {filename}")
        data = []
        with open(filename, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                # row.append("new data")  # Add new data to each row
                data.append(row)
        self.upload_csv_button.pack_forget()
        self.loaded_csv_label.config(text=f'Patient CSV file:\n {filename}')
        self.loaded_csv_label.pack(pady=10)
        self.predict_button.pack()

    def predict(self):
        self.info_label.pack()
        self.info_label.config(text="Loading...")
        try:
            self._display_predict_result(self.image_path)
        except Exception as e:
            self.info_label.config(text="")
            raise e
        # self.info_label.config(text="")
        self.predict_button.pack_forget()

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
            self.loaded_image_label.pack_forget()
            self.loaded_image_path_label.pack_forget()
            self.loaded_csv_label.pack_forget()
            self.info_label.config(text="")
            self.info_label.pack_forget()
            self.save_button.pack_forget()
            self.upload_image_button.pack()
        except Exception as e:
            messagebox.showerror("Save failed", "Failed saving image")
            print("Failed to save image due to:", e)

    def _display_image(self, filename):
        image = Image.open(filename).resize((DISPLAYED_IMAGE_SIZE, DISPLAYED_IMAGE_SIZE))
        photo = ImageTk.PhotoImage(image)
        self.loaded_image_label.config(image=photo)
        self.loaded_image_label.image = photo  # keep a reference!
        self.loaded_image_label.pack()

    def _display_predict_result(self, filename):
        """
        Sends the prediction request to the server and then displays the prediction on the window for the user to view.
        :param filename: path to image for prediction
        """
        if not filename:
            return
        image = Image.open(filename)
        try:
            # TODO undo
            # prediction, probability = send_predict_request(filename, PREDICTOR_URI)
            prediction, probability = 2, 0.8
        except Exception as e:
            messagebox.showerror("Prediction failed",
                                 "Failed to perform prediction, try again")
            print(f"Failed to predict due to:", e)
            self.info_label.config(text='')
            return
        prediction_class = convert_prediction_to_class(prediction)

        probability = round(float(probability), 3)
        self.info_label.config(text=f"Prediction: {prediction_class}\n\n"
                                    f"Probability: {probability}")
        print("Image selected:", filename)
        self.image_to_save = image
        self.prediction_to_save = prediction_class
        self.save_button.pack()
