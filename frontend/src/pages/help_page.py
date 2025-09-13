import tkinter as tk


class HelpPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        # Title
        self.title_label = tk.Label(self, text="How to use", font=controller.title_font)
        self.title_label.pack(side="top", fill="x", pady=10)

        # Role-specific help text (will be updated when page is shown)
        self.text_label = tk.Label(self, text="", wraplength=400, font=("Arial", 12), justify=tk.LEFT)
        self.text_label.pack(padx=20, pady=20)
        
    def update_help_content(self):
        """
        Update the help content based on the current user role.
        """
        current_role = self.controller.current_role
        
        if current_role == "doctor":
            self.title_label.config(text="Doctor Guide")
            help_text = ('Welcome Doctor! This system helps you diagnose osteoporosis conditions from knee X-ray images.\n\n'
                        'HOW TO USE:\n'
                        '1. From your Doctor Dashboard, choose:\n'
                        '   • "New Diagnosis" - Analyze a new patient\'s X-ray\n'
                        '   • "Search Diagnosis" - Look up previous diagnoses\n\n'
                        '2. For New Diagnosis:\n'
                        '   • Upload a knee X-ray image (JPEG, PNG formats)\n'
                        '   • Upload patient CSV file with relevant medical data\n'
                        '   • Click "Predict" to get the diagnosis\n\n'
                        '3. Results will show:\n'
                        '   • Osteoporosis - Severe bone density loss\n'
                        '   • Osteopenia - Mild bone density loss\n'
                        '   • Normal - Healthy bone density\n\n'
                        'The system provides confidence levels to help with your clinical decision-making.')
                        
        elif current_role == "researcher":
            self.title_label.config(text="Researcher Guide")
            help_text = ('Welcome Researcher! This system allows you to train and test osteoporosis detection models.\n\n'
                        'HOW TO USE:\n'
                        '1. From your Researcher Dashboard, choose:\n'
                        '   • "Train Model" - Improve the AI model with new data\n'
                        '   • "Test Model" - Evaluate model performance\n\n'
                        '2. For Model Training:\n'
                        '   • Select "Delta Training" for incremental updates\n'
                        '   • Select "Full Training" for complete model retraining\n'
                        '   • Upload labeled datasets in the required format\n\n'
                        '3. For Model Testing:\n'
                        '   • Use "New Diagnosis" to test individual cases\n'
                        '   • Use "Search Diagnosis" to review test results\n'
                        '   • Analyze model accuracy and performance metrics\n\n'
                        '4. Data Requirements:\n'
                        '   • Knee X-ray images (JPEG, PNG)\n'
                        '   • Properly labeled CSV files with ground truth\n'
                        '   • Consistent image quality and format')
                        
        else:
            # Default help for users who haven't selected a role yet
            self.title_label.config(text="System Overview")
            help_text = ('This is an Osteoporosis Classification System that analyzes knee X-ray images.\n\n'
                        'SYSTEM PURPOSE:\n'
                        'Classify whether a patient suffers from:\n'
                        '• Osteoporosis (severe bone density loss)\n'
                        '• Osteopenia (mild bone density loss)\n'
                        '• Normal (healthy bone density)\n\n'
                        'USER ROLES:\n'
                        '• Doctor - Diagnose patients using the trained model\n'
                        '• Researcher - Train and test the AI models\n\n'
                        'To get started, return to the welcome page and select your role.\n'
                        'You will then see role-specific instructions and options.\n\n'
                        'The system works with knee X-ray images and patient data files in CSV format.')
        
        self.text_label.config(text=help_text)