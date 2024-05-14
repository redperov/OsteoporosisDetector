import tkinter as tk


class HelpPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        title_label = tk.Label(self, text="How to use", font=controller.title_font)
        title_label.pack(side="top", fill="x", pady=10)

        help_text = ('This is a program meant to classify whether a patient suffers from Osteoporosis,'
                     'Osteopenia or from neither. The program works on X-ray images of the knee ares.\n\n'
                     'You can perform testing by clicking the "START TESTING" button. '
                     'Then, choose a knee X-ray image and a patient CSV file from your computer and upload it to '
                     'the program. The program will then return a classification. '
                     'You can perform training by clicking the "START TRAINING" button. '
                     'Then, you can choose to retrain the model on a delta of data or on a full dataset by pressing'
                     ' either "DELTA TRAINING" or "FULL TRAINING" correspondingly.')
        text_label = tk.Label(self, text=help_text, wraplength=400, font=8, justify=tk.LEFT)
        text_label.pack()