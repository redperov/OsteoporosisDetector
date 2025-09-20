import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import csv
from PIL import Image, ImageTk


class RolePage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.role_type = None  # Will be set to "doctor" or "researcher"
        
        # Title
        self.title_label = tk.Label(self, text="", font=controller.title_font)
        self.title_label.pack(side="top", fill="x", pady=20)
        
        # Create a frame to hold the buttons vertically
        button_frame = tk.Frame(self)
        button_frame.pack(pady=50)
        
        # First button
        self.first_button = tk.Button(button_frame, text="", width=20, height=2,
                                     font=("Arial", 14))
        self.first_button.pack(pady=10)
        
        # Second button  
        self.second_button = tk.Button(button_frame, text="", width=20, height=2,
                                      font=("Arial", 14))
        self.second_button.pack(pady=10)
        
    def set_role(self, role_type):
        """
        Configure the page based on the role type (doctor, researcher, or test).
        """
        self.role_type = role_type
        
        if role_type == "doctor":
            self.title_label.config(text="Doctor Dashboard")
            self.first_button.config(text="New Diagnosis", 
                                   command=lambda: self.controller.show_frame("PredictionPage"))
            self.second_button.config(text="Search Diagnosis",
                                    command=self.show_search_popup)
            
        elif role_type == "researcher":
            self.title_label.config(text="Researcher Dashboard")
            self.first_button.config(text="Train Model",
                                   command=lambda: self.controller.show_frame("TrainingPage"))
            self.second_button.config(text="Test Model",
                                    command=lambda: self.controller.show_test_page())
            
        elif role_type == "test":
            self.title_label.config(text="Model Testing")
            self.first_button.config(text="New Diagnosis", 
                                   command=lambda: self.controller.show_frame("PredictionPage"))
            self.second_button.config(text="Search Diagnosis",
                                    command=self.show_search_popup)
    
    def show_search_popup(self):
        """
        Show a popup window for searching diagnosis by patient ID.
        """
        # Create popup window
        popup_window = tk.Toplevel(self)
        popup_window.title("Search Diagnosis")
        popup_window.geometry("400x200")
        
        # Center the popup window
        popup_window.transient(self)
        popup_window.grab_set()
        
        # Calculate center position
        popup_window.update_idletasks()
        x = (popup_window.winfo_screenwidth() // 2) - (400 // 2)
        y = (popup_window.winfo_screenheight() // 2) - (200 // 2)
        popup_window.geometry(f"400x200+{x}+{y}")
        
        # Title label
        title_label = tk.Label(popup_window, text="Search Patient Diagnosis", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=20)
        
        # Patient ID input section
        input_frame = tk.Frame(popup_window)
        input_frame.pack(pady=10)
        
        patient_id_label = tk.Label(input_frame, text="Patient ID:", 
                                   font=("Arial", 12))
        patient_id_label.pack(side=tk.LEFT, padx=5)
        
        patient_id_entry = tk.Entry(input_frame, font=("Arial", 12), width=20)
        patient_id_entry.pack(side=tk.LEFT, padx=5)
        patient_id_entry.focus()  # Focus on the input field
        
        # Button frame
        button_frame = tk.Frame(popup_window)
        button_frame.pack(pady=20)
        
        # Search button
        search_button = tk.Button(button_frame, text="Search", 
                                 font=("Arial", 12),
                                 command=lambda: self.perform_search(patient_id_entry.get(), popup_window))
        search_button.pack(side=tk.LEFT, padx=10)
        
        # Cancel button
        cancel_button = tk.Button(button_frame, text="Cancel", 
                                 font=("Arial", 12),
                                 command=popup_window.destroy)
        cancel_button.pack(side=tk.LEFT, padx=10)
        
        # Bind Enter key to search
        patient_id_entry.bind('<Return>', 
                             lambda event: self.perform_search(patient_id_entry.get(), popup_window))
    
    def perform_search(self, patient_id, popup_window):
        """
        Perform the search for the given patient ID.
        """
        if not patient_id.strip():
            messagebox.showwarning("Invalid Input", "Please enter a Patient ID")
            return
        
        try:
            # Look for patient folder in local_data
            local_data_dir = Path("local_data")
            patient_folder = local_data_dir / str(patient_id.strip())
            
            if not patient_folder.exists():
                messagebox.showwarning("Patient Not Found", 
                                     f"No records found for Patient ID: {patient_id}")
                return
            
            # Find the most recent result files
            image_files = list(patient_folder.glob("*.jpg"))
            csv_files = list(patient_folder.glob("*.csv"))
            
            if not image_files or not csv_files:
                messagebox.showwarning("No Results", 
                                     f"No diagnosis results found for Patient ID: {patient_id}")
                return
            
            # Get the most recent files (sorted by name which includes timestamp)
            latest_image = sorted(image_files)[-1]
            latest_csv = sorted(csv_files)[-1]
            
            # Extract diagnosis from filename
            diagnosis = self.extract_diagnosis_from_filename(latest_image.name)
            
            # Close search popup
            popup_window.destroy()
            
            # Display the results
            self.display_search_results(patient_id, latest_image, latest_csv, diagnosis)
            
        except Exception as e:
            messagebox.showerror("Search Error", f"Error searching for patient: {str(e)}")
            print(f"Search error: {e}")
    
    def extract_diagnosis_from_filename(self, filename):
        """
        Extract diagnosis from filename format: YYYYMMDD_HHMMSS_Diagnosis.jpg
        """
        try:
            # Remove file extension and split by underscore
            parts = filename.replace('.jpg', '').split('_')
            if len(parts) >= 3:
                return parts[2]  # The diagnosis part
            return "Unknown"
        except:
            return "Unknown"
    
    def display_search_results(self, patient_id, image_path, csv_path, diagnosis):
        """
        Display the search results in a new window.
        """
        # Create results window
        results_window = tk.Toplevel(self)
        results_window.title(f"Patient {patient_id} - Search Results")
        results_window.geometry("500x600")
        
        # Center the window
        results_window.transient(self)
        results_window.grab_set()
        
        # Calculate center position
        results_window.update_idletasks()
        x = (results_window.winfo_screenwidth() // 2) - (500 // 2)
        y = (results_window.winfo_screenheight() // 2) - (600 // 2)
        results_window.geometry(f"500x600+{x}+{y}")
        
        # Title
        title_label = tk.Label(results_window, text=f"Patient {patient_id} - Latest Diagnosis", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Display image
        try:
            image = Image.open(image_path).resize((300, 300))
            photo = ImageTk.PhotoImage(image)
            image_label = tk.Label(results_window, image=photo)
            image_label.image = photo  # Keep a reference
            image_label.pack(pady=10)
        except Exception as e:
            error_label = tk.Label(results_window, text="Error loading image", 
                                  font=("Arial", 12), fg="red")
            error_label.pack(pady=10)
        
        # Read patient data to get prediction accuracy
        try:
            patient_data = self.read_patient_data(csv_path)
            prediction_accuracy = patient_data.get("Prediction Accuracy", "N/A")
        except:
            prediction_accuracy = "N/A"
        
        # Display diagnosis result with accuracy
        diagnosis_text = f"Diagnosis: {diagnosis}"
        if prediction_accuracy != "N/A":
            try:
                accuracy_float = float(prediction_accuracy)
                diagnosis_text += f"\nAccuracy: {accuracy_float:.1%}"
            except:
                diagnosis_text += f"\nAccuracy: {prediction_accuracy}"
        
        diagnosis_label = tk.Label(results_window, text=diagnosis_text, 
                                  font=("Arial", 14, "bold"), fg="green", justify=tk.CENTER)
        diagnosis_label.pack(pady=10)
        
        # Display file information
        info_text = f"Image: {image_path.name}\nData: {csv_path.name}\nDate: {self.extract_date_from_filename(image_path.name)}"
        info_label = tk.Label(results_window, text=info_text, 
                             font=("Arial", 12), justify=tk.LEFT)
        info_label.pack(pady=10)
        
        # Button to view patient details
        if prediction_accuracy != "N/A":  # We already have patient_data
            view_details_button = tk.Button(results_window, text="View Patient Details", 
                                          font=("Arial", 14),
                                          command=lambda: self.show_patient_details_popup(patient_id, patient_data))
            view_details_button.pack(pady=15)
        else:
            error_label = tk.Label(results_window, text="Error loading patient data", 
                                  font=("Arial", 14), fg="red")
            error_label.pack(pady=5)
        
        # Close button
        close_button = tk.Button(results_window, text="Close", 
                                command=results_window.destroy,
                                font=("Arial", 12))
        close_button.pack(pady=10)
    
    def extract_date_from_filename(self, filename):
        """
        Extract and format date from filename.
        """
        try:
            # Extract timestamp part: YYYYMMDD_HHMMSS
            parts = filename.split('_')
            if len(parts) >= 2:
                date_part = parts[0]  # YYYYMMDD
                time_part = parts[1]  # HHMMSS
                
                # Format as readable date
                year = date_part[:4]
                month = date_part[4:6]
                day = date_part[6:8]
                hour = time_part[:2]
                minute = time_part[2:4]
                
                return f"{day}/{month}/{year} {hour}:{minute}"
            return "Unknown"
        except:
            return "Unknown"
    
    def read_patient_data(self, csv_path):
        """
        Read patient data from CSV file.
        """
        patient_data = {}
        try:
            with open(csv_path, 'r') as file:
                reader = csv.reader(file)
                header = next(reader)
                data_row = next(reader)
                
                for i, value in enumerate(data_row):
                    if i < len(header):
                        patient_data[header[i]] = value
                        
        except Exception as e:
            print(f"Error reading CSV: {e}")
            
        return patient_data
    
    def show_patient_details_popup(self, patient_id, patient_data):
        """
        Show patient details in a popup window.
        """
        # Create patient details window
        details_window = tk.Toplevel(self)
        details_window.title(f"Patient {patient_id} - Detailed Information")
        details_window.geometry("600x500")
        
        # Center the window
        details_window.transient(self)
        details_window.grab_set()
        
        # Calculate center position
        details_window.update_idletasks()
        x = (details_window.winfo_screenwidth() // 2) - (600 // 2)
        y = (details_window.winfo_screenheight() // 2) - (500 // 2)
        details_window.geometry(f"600x500+{x}+{y}")
        
        # Title
        title_label = tk.Label(details_window, text=f"Patient {patient_id} - Complete Information", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Create scrollable text area for patient data
        from tkinter import scrolledtext
        data_frame = tk.Frame(details_window)
        data_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        data_text = scrolledtext.ScrolledText(data_frame, wrap=tk.WORD,
                                             font=("Arial", 12), 
                                             bg='white', fg='black')
        data_text.pack(fill="both", expand=True)
        
        # Format and display patient data
        data_text.insert(tk.INSERT, f"PATIENT INFORMATION - ID: {patient_id}\n")
        data_text.insert(tk.INSERT, "=" * 50 + "\n\n")
        
        # Group related information
        basic_info = ["Patient Id", "Gender", "Age", "Height (m)", "Weight (KG)", "BMI"]
        medical_history = ["Joint Pain", "Diabetic", "Hypothyroidism", "History of Fracture", 
                          "Family History of Osteoporosis", "Medical History"]
        lifestyle = ["Smoker", "Alcoholic", "Occupation", "Maximum Walking Distance (km)", 
                    "Daily Eating Habits"]
        women_health = ["Menopause Age", "Number of Pregnancies", "Estrogen Use"]
        clinical_data = ["T-Score Value", "Z-Score Value", "Site", "Obesity"]
        
        sections = [
            ("BASIC INFORMATION", basic_info),
            ("MEDICAL HISTORY", medical_history),
            ("LIFESTYLE FACTORS", lifestyle),
            ("WOMEN'S HEALTH", women_health),
            ("CLINICAL DATA", clinical_data)
        ]
        
        for section_title, fields in sections:
            data_text.insert(tk.INSERT, f"{section_title}:\n")
            data_text.insert(tk.INSERT, "-" * 30 + "\n")
            
            for field in fields:
                if field in patient_data:
                    value = patient_data[field]
                    data_text.insert(tk.INSERT, f"{field}: {value}\n")
            
            data_text.insert(tk.INSERT, "\n")
        
        # Add any remaining fields not in the sections above
        data_text.insert(tk.INSERT, "OTHER INFORMATION:\n")
        data_text.insert(tk.INSERT, "-" * 30 + "\n")
        
        all_section_fields = set()
        for _, fields in sections:
            all_section_fields.update(fields)
        
        for key, value in patient_data.items():
            if key not in all_section_fields:
                data_text.insert(tk.INSERT, f"{key}: {value}\n")
        
        data_text.config(state=tk.DISABLED)  # Make read-only
        
        # Close button
        close_button = tk.Button(details_window, text="Close", 
                                command=details_window.destroy,
                                font=("Arial", 12))
        close_button.pack(pady=10)
