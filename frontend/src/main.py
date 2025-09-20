import tkinter as tk

from frontend.src.utils import get_window_center_coordinates
from tkinter import font as tkfont

from frontend.src.pages.about_page import AboutPage
from frontend.src.pages.help_page import HelpPage
from frontend.src.pages.prediction_page import PredictionPage
from frontend.src.pages.role_page import RolePage
from frontend.src.pages.welcome_page import WelcomePage
from frontend.src.pages.training_page import TrainingPage

WINDOW_HEIGHT = 800
WINDOW_WIDTH = 550


class OSDetectionApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold")
        self.title("Osteoporosis Classifier")
        self.current_role = None  # Track the selected role (doctor/researcher)
        position_right, position_top = get_window_center_coordinates(self, WINDOW_HEIGHT, WINDOW_WIDTH)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{position_right}+{position_top}")

        # Create and pack navbar first so it appears at the top
        self.navbar_frame = None
        self.load_navbar()
        self.navbar_frame.pack(side=tk.TOP, fill=tk.X)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        self.container = container  # Store reference for later use
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (WelcomePage, RolePage, PredictionPage, TrainingPage, AboutPage, HelpPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("WelcomePage")

    def load_navbar(self):
        """
        Create the navbar frame.
        """
        self.navbar_frame = tk.Frame(self, background="#696969")
        
        home_button = tk.Button(self.navbar_frame, text='HOME', command=self.go_home,
                               bg='white', fg='black', relief='raised', bd=2,
                               activebackground='#e0e0e0', highlightbackground='#696969')
        home_button.pack(side=tk.LEFT, padx=4, pady=2)

        about_button = tk.Button(self.navbar_frame, text='ABOUT', command=lambda: self.show_frame("AboutPage"),
                                bg='white', fg='black', relief='raised', bd=2,
                                activebackground='#e0e0e0', highlightbackground='#696969')
        about_button.pack(side=tk.LEFT, padx=4, pady=2)

        help_button = tk.Button(self.navbar_frame, text='HELP', command=lambda: self.show_frame("HelpPage"),
                               bg='white', fg='black', relief='raised', bd=2,
                               activebackground='#e0e0e0', highlightbackground='#696969')
        help_button.pack(side=tk.LEFT, pady=2)

        exit_button = tk.Button(self.navbar_frame, text='EXIT', command=self.exit_to_welcome,
                               bg='white', fg='black', relief='raised', bd=2,
                               activebackground='#e0e0e0', highlightbackground='#696969')
        exit_button.pack(side=tk.RIGHT, padx=4, pady=2)

    def show_frame(self, page_name):
        """
        Show a frame for the given page name.
        """
        # Hide navbar on welcome page, show on others
        if page_name == "WelcomePage":
            if self.navbar_frame:
                self.navbar_frame.pack_forget()
        else:
            if self.navbar_frame and not self.navbar_frame.winfo_viewable():
                self.navbar_frame.pack(side=tk.TOP, fill=tk.X, before=self.container)
        
        # Update help content when showing help page
        if page_name == "HelpPage":
            help_page = self.frames["HelpPage"]
            help_page.update_help_content()
        
        frame = self.frames[page_name]
        frame.tkraise()

    def go_home(self):
        """
        Navigate to the appropriate home page based on current role.
        If no role is selected, go to welcome page.
        """
        if self.current_role:
            self.show_role_page(self.current_role)
        else:
            self.show_frame("WelcomePage")

    def exit_to_welcome(self):
        """
        Reset the current role and navigate back to the welcome page.
        This allows users to change their role selection.
        """
        self.current_role = None  # Reset the role
        self.show_frame("WelcomePage")

    def show_role_page(self, role_type):
        """
        Show the role page configured for the specified role type.
        """
        self.current_role = role_type  # Store the selected role
        role_page = self.frames["RolePage"]
        role_page.set_role(role_type)
        self.show_frame("RolePage")

    def show_test_page(self):
        """
        Show the role page configured for testing (same as doctor page but with "Model Testing" title).
        """
        role_page = self.frames["RolePage"]
        role_page.set_role("test")
        self.show_frame("RolePage")


# def to_delete():
#     import requests
#     from pathlib import Path
#     import base64
#     import json
#     filename = Path(r"C:\Users\perov\OneDrive\Desktop\N1.JPEG")
#     with open(filename, "rb") as image_file:
#         encoded_image = base64.b64encode(image_file.read()).decode('ascii')
#     data = {"image": encoded_image, "image_name": filename.stem}
#     headers = {"Content-Type": "application/json"}
#     response = requests.post("http://localhost:5001/predict_osteoporosis", data=json.dumps(data), headers=headers)
#     print(response.status_code)

if __name__ == "__main__":
    # to_delete()
    app = OSDetectionApp()
    app.mainloop()

