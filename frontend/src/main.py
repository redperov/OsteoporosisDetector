import tkinter as tk

from frontend.src.navbar import load_navbar
from frontend.src.utils import get_window_center_coordinates, load_image
from tkinter import font as tkfont

from frontend.src.pages.help_page import HelpPage
from frontend.src.pages.prediction_page import PredictionPage
from frontend.src.pages.welcome_page import WelcomePage

# from pathlib import Path
#
# WELCOME_IMAGE_PATH = Path(r"C:\Users\Danny\PycharmProjects\OsteoporosisProject\frontend\resources\download.jpg")
#
# root = tk.Tk()
# root.title("Osteoporosis detector")
#
# Set window size


#
# load_navbar(root)
#
# # Set the position of the window to the center of the screen

#
# welcome_label = tk.Label(root, text="Welcome to Osteoporosis detector", font=("Arial", 20))
# welcome_label.pack(pady=20)
#
# # Load an image and add it to a label
# welcome_image = load_image(WELCOME_IMAGE_PATH)
# image_label = tk.Label(root, image=welcome_image)
# image_label.pack(pady=20)
#
# start_button = tk.Button(root, text="START PREDICTING")
# start_button.pack(pady=20)
#
# root.mainloop()


class OSDetectionApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        WINDOW_HEIGHT = 400
        WINDOW_WIDTH = 500

        tk.Tk.__init__(self, *args, **kwargs)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold")
        self.title("Osteoporosis detector")
        load_navbar(self)
        position_right, position_top = get_window_center_coordinates(self, WINDOW_HEIGHT, WINDOW_WIDTH)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{position_right}+{position_top}")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (WelcomePage, PredictionPage, HelpPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("WelcomePage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


if __name__ == "__main__":
    app = OSDetectionApp()
    app.mainloop()
