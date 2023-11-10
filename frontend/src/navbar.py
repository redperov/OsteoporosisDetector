import tkinter as tk


def load_navbar(root):
    # Create a frame for the navigation bar
    navbar_frame = tk.Frame(root, background="#696969")
    navbar_frame.pack(side=tk.TOP, fill=tk.X)

    home_button = tk.Button(navbar_frame, text='HOME', command=lambda: root.show_frame("WelcomePage"))
    home_button.pack(side=tk.LEFT)
    home_button.pack(padx=4, pady=2)

    help_button = tk.Button(navbar_frame, text='HELP', command=lambda: root.show_frame("HelpPage"))
    help_button.pack(side=tk.LEFT)
    help_button.pack(pady=2)