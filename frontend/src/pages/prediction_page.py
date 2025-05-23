import tkinter as tk
from datetime import datetime
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
        self.patient_csv_path = None
        self.prediction_to_save = None
        self.image_path = None
        self.loaded_image_label = tk.Label(self)
        self.loaded_image_path_label = tk.Label(self, font=8, justify=tk.LEFT)
        self.loaded_csv_label = tk.Label(self, font=8, justify=tk.LEFT)

        self.upload_image_button = tk.Button(self, text="UPLOAD AN IMAGE", command=self.upload_image)
        self.upload_csv_button = tk.Button(self, text="UPLOAD A CSV FILE", command=self.upload_csv)
        self.fill_manually_button = tk.Button(self, text="FILL DATA MANUALLY", command=self.fill_data_manually)
        self.predict_button = tk.Button(self, text="PREDICT", command=self.predict)
        self.info_label = tk.Label(self, text="", wraplength=400, font=8, justify=tk.LEFT, pady=10)
        self.save_button = tk.Button(self, text="SAVE RESULT", command=lambda: self.save_result(
            self.image_to_save, self.patient_csv_path, self.prediction_to_save))

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
            self.upload_csv_button.pack(padx=80, side=tk.LEFT)
            self.fill_manually_button.pack(side=tk.LEFT)
        except Exception as e:
            messagebox.showerror("Error", "Error! please try again")
            print("Failed to predict on an image due to:", e)
            self.info_label.config(text='')
            self.save_button.pack_forget()

    def upload_csv(self, filename=None):
        if not filename:
            filename = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not filename:
            raise ValueError(f"Can't read a file named {filename}")
        self.patient_csv_path = filename
        self.upload_csv_button.pack_forget()
        self.fill_manually_button.pack_forget()
        self.loaded_csv_label.config(text=f'Patient CSV file:\n {filename}')
        self.loaded_csv_label.pack(pady=10)
        self.predict_button.pack()

    def fill_data_manually(self):
        popup_window = tk.Toplevel()
        popup_window.title("Enter Patient Details")

        # Center the popup window on the screen
        screen_width = popup_window.winfo_screenwidth()
        screen_height = popup_window.winfo_screenheight()
        popup_width = 400  # Adjust the desired width
        popup_height = 600  # Adjust the desired height
        x_position = (screen_width - popup_width) // 2
        y_position = (screen_height - popup_height) // 2
        popup_window.geometry(f"{popup_width}x{popup_height}+{x_position}+{y_position}")

        # Create a canvas with a vertical scrollbar
        canvas = tk.Canvas(popup_window)
        scrollbar = tk.Scrollbar(popup_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        # Configure the canvas and scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Function to update scroll region
        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        scrollable_frame.bind("<Configure>", on_configure)

        # List of additional features
        features = [
            "Patient Id", "Joint Pain", "Gender", "Age", "Menopause Age", "Height (m)", "Weight (KG)",
            "Smoker", "Alcoholic", "Diabetic", "Hypothyroidism", "Number of Pregnancies",
            "Seizer Disorder", "Estrogen Use", "Occupation", "History of Fracture", "Dialysis",
            "Family History of Osteoporosis", "Maximum Walking Distance (km)", "Daily Eating Habits",
            "Medical History", "T-Score Value", "Z-Score Value", "BMI", "Site", "Obesity"
        ]

        # Create labels and entry widgets
        widgets = {}
        for feature in features:
            frame = tk.Frame(scrollable_frame)
            label = tk.Label(frame, text=feature + ":")
            entry = tk.Entry(frame)
            label.grid(row=0, column=0, padx=10, pady=10)
            entry.grid(row=0, column=1, padx=10, pady=10)
            frame.pack(fill="x")
            widgets[feature] = entry

        # Create submit button
        submit_frame = tk.Frame(scrollable_frame)
        submit_button = tk.Button(submit_frame, text="SUBMIT",
                                  command=lambda: self.submit_patient_details(features, widgets, popup_window))
        submit_button.grid(row=0, column=0, padx=10, pady=10)
        submit_frame.pack(fill="x")

    def submit_patient_details(self, features, widgets, popup_window):
        data = {}
        for feature in features:
            data[feature] = widgets[feature].get()

        # Write the data to a CSV file
        temp_patient_details_csv_path = "temp_patient_details.csv"
        with open(temp_patient_details_csv_path, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=features)
            writer.writeheader()
            writer.writerow(data)
        self.patient_csv_path = temp_patient_details_csv_path
        # self.loaded_csv_label.config(text=f'Patient CSV file: Filled manually')
        self.upload_csv(temp_patient_details_csv_path)
        popup_window.destroy()

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

    def save_result(self, image, patient_csv, prediction):
        """
        Saves the uploaded image in a selected directory on the local machine with the predicted classification.
        :param image: image to predict on
        :param patient_csv: patient details in a CSV file
        :param prediction: classification prediction
        """
        try:
            directory = filedialog.askdirectory()
            filename = f"{uuid.uuid4()}_{prediction}"
            image_to_save_path = Path(f"{directory}/{filename}.jpg")
            csv_to_save_path = Path(f"{directory}/{filename}.csv")
            image.save(image_to_save_path)

            self.add_prediction_details_to_csv(patient_csv, csv_to_save_path, prediction)

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

    def add_prediction_details_to_csv(self, original_csv_path, modified_csv_path, prediction):
        with open(original_csv_path, "r") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            header = next(reader)  # Skip the header row (if present)

            # Add new columns
            header.append("Prediction Date")
            header.append("Prediction")

            # Create a list to store rows with the updated column
            updated_rows = []

            # Get the current date and time
            current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Iterate through each row in the CSV
            for row in reader:
                row.append(current_date)
                row.append(prediction)

                # Add the updated row to the list
                updated_rows.append(row)

        # Write the updated data to a new CSV file
        with open(modified_csv_path, "w", newline="") as output_csv:
            writer = csv.writer(output_csv)
            writer.writerow(header)  # Write the updated header
            writer.writerows(updated_rows)  # Write the updated rows

        # # Read the CSV file
        # with open(original_csv_path, 'r') as f:
        #     reader = csv.reader(f)
        #     data = list(reader)
        #
        # # Add a new column to each row
        # for row in data:
        #     row.append('new_column')
        #
        #
        # # Write the data back to the CSV file
        # with open(modified_csv_path, 'w', newline='') as f:
        #     writer = csv.writer(f)
        #     writer.writerows(data)

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
