import tkinter as tk


class HelpPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        title_label = tk.Label(self, text="How to use", font=controller.title_font)
        title_label.pack(side="top", fill="x", pady=10)

        help_text = ('This is a program meant to predict whether a patient suffers from Osteoporosis,'
                     'Osteopenia or from neither. The program works on X-ray temp_images of the knee ares.\n\n'
                     'Go to the prediction page and click the "START PREDICTING" button. '
                     'Then, choose a knee X-ray image from your computer and upload it to '
                     'the program. The program will then return a prediction on whether the patient '
                     'in the image suffers from Osteoporosis, Osteopenia or is healthy.')
        text_label = tk.Label(self, text=help_text, wraplength=400, font=8, justify=tk.LEFT)
        text_label.pack()