import tkinter as tk
from tkinter import scrolledtext


class AboutPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        # Title
        title_label = tk.Label(self, text="About Osteoporosis Classification System", 
                              font=controller.title_font)
        title_label.pack(side="top", fill="x", pady=10)

        # Create scrollable text area for the content
        text_frame = tk.Frame(self)
        text_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        text_area = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, 
                                            font=('Arial', 12), 
                                            height=20, width=60)
        text_area.pack(fill="both", expand=True)
        
        # Comprehensive about content
        about_content = """UNDERSTANDING OSTEOPOROSIS

What is Osteoporosis?
Osteoporosis is a bone disease that occurs when the body loses too much bone, makes too little bone, or both. This results in bones becoming weak and brittle, making them more likely to break from minor falls or even mild stresses like bending over or coughing.

Key Facts:
• Affects over 200 million people worldwide
• More common in women after menopause
• Often called a "silent disease" because bone loss occurs without symptoms
• Can lead to fractures of the hip, spine, and wrist

Bone Density Classifications:
• NORMAL: Healthy bone density with T-score above -1.0
• OSTEOPENIA: Low bone density (T-score between -1.0 and -2.5)
• OSTEOPOROSIS: Severe bone loss (T-score below -2.5)

Risk Factors:
• Age (especially over 50)
• Gender (women at higher risk)
• Family history of osteoporosis
• Low calcium and vitamin D intake
• Sedentary lifestyle
• Smoking and excessive alcohol consumption


ABOUT THIS SYSTEM

Technology Overview:
Our Osteoporosis Classification System uses advanced artificial intelligence and machine learning algorithms to analyze knee X-ray images and detect signs of bone density loss. The system provides automated screening that can assist healthcare professionals in early detection and diagnosis.

How It Works:
1. Image Analysis: AI algorithms examine knee X-ray images for patterns indicative of bone density changes
2. Pattern Recognition: The system identifies subtle changes in bone structure and density
3. Classification: Results are categorized as Normal, Osteopenia, or Osteoporosis
4. Confidence Scoring: Each diagnosis includes a confidence level to assist clinical decision-making

System Capabilities:
• Rapid analysis of X-ray images (results in seconds)
• High accuracy through deep learning algorithms
• Standardized assessment reducing human error
• Integration with patient data for comprehensive analysis
• Support for multiple image formats (JPEG, PNG)

Clinical Applications:
• Early screening and detection
• Monitoring disease progression
• Treatment response evaluation
• Population health screening programs
• Research and clinical studies

User Roles:
• DOCTORS: Use the system for patient diagnosis and clinical decision support
• RESEARCHERS: Train and test models, analyze performance metrics, conduct studies

Data Requirements:
• High-quality knee X-ray images
• Patient demographic and clinical data in CSV format
• Proper image positioning and exposure settings
• DICOM or standard image formats


IMPORTANT DISCLAIMER

This system is designed to assist healthcare professionals and should not replace clinical judgment. All results should be interpreted by qualified medical personnel in conjunction with other clinical findings, patient history, and additional diagnostic tests.

For research purposes, this system provides valuable tools for model development, validation, and performance analysis in the field of automated bone density assessment.

System developed by Danny Perov under the supervision of Dr. Maya Herman - 2025"""

        text_area.insert(tk.INSERT, about_content)
        text_area.config(state=tk.DISABLED)  # Make it read-only