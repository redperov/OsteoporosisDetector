import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
import math


class TrainingPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        # Title
        title_label = tk.Label(self, text="Model Training", font=controller.title_font)
        title_label.pack(side="top", fill="x", pady=10)
        
        # Initialize variables
        self.selected_data_path = None
        self.selected_model = None
        self.is_animating = False
        self.arrow = None
        self.angle = 0
        
        # Create main container with scrollable frame
        self.create_ui_elements()
        
        # Animation canvas (initially hidden)
        self.canvas = tk.Canvas(self, width=200, height=200)
        self.canvas.pack_forget()

    def create_ui_elements(self):
        """Create all UI elements for the training page."""
        
        # Step 1: Data Selection
        data_frame = tk.LabelFrame(self, text="Step 1: Select Training Data", 
                                  font=("Arial", 12, "bold"), padx=10, pady=10)
        data_frame.pack(fill="x", padx=20, pady=10)
        
        self.load_data_button = tk.Button(data_frame, text="Load Training Data", 
                                         font=("Arial", 12),
                                         command=self.load_training_data)
        self.load_data_button.pack(pady=5)
        
        self.data_path_label = tk.Label(data_frame, text="No data selected", 
                                       font=("Arial", 10), fg="gray",
                                       wraplength=400, justify=tk.LEFT)
        self.data_path_label.pack(pady=5)
        
        # Step 2: Model Architecture Selection
        self.model_frame = tk.LabelFrame(self, text="Step 2: Select Model Architecture", 
                                        font=("Arial", 12, "bold"), padx=10, pady=10)
        self.model_frame.pack(fill="x", padx=20, pady=10)
        self.model_frame.pack_forget()  # Initially hidden
        
        self.model_var = tk.StringVar()
        self.cnn_radio = tk.Radiobutton(self.model_frame, text="CNN (Convolutional Neural Network)", 
                                       variable=self.model_var, value="CNN",
                                       font=("Arial", 11),
                                       command=self.on_model_selection)
        self.cnn_radio.pack(anchor="w", pady=2)
        
        self.ensemble_radio = tk.Radiobutton(self.model_frame, text="Ensemble (CNN + Decision Tree)", 
                                            variable=self.model_var, value="Ensemble",
                                            font=("Arial", 11),
                                            command=self.on_model_selection)
        self.ensemble_radio.pack(anchor="w", pady=2)
        
        # Step 3: Hyperparameter Configuration
        self.hyperparams_frame = tk.LabelFrame(self, text="Step 3: Configure Hyperparameters", 
                                              font=("Arial", 12, "bold"), padx=10, pady=10)
        self.hyperparams_frame.pack(fill="x", padx=20, pady=10)
        self.hyperparams_frame.pack_forget()  # Initially hidden
        
        # Create hyperparameter widgets (will be populated based on model selection)
        self.create_hyperparameter_widgets()
        
        # Step 4: Training Controls
        self.training_frame = tk.LabelFrame(self, text="Step 4: Start Training", 
                                           font=("Arial", 12, "bold"), padx=10, pady=10)
        self.training_frame.pack(fill="x", padx=20, pady=10)
        self.training_frame.pack_forget()  # Initially hidden
        
        self.train_button = tk.Button(self.training_frame, text="Start Training", 
                                     font=("Arial", 14, "bold"),
                                     command=self.start_training)
        self.train_button.pack(pady=10)
        
        self.stop_training_button = tk.Button(self.training_frame, text="Stop Training", 
                                             font=("Arial", 12),
                                             bg="red", fg="white",
                                             command=self.stop_training)
        self.stop_training_button.pack_forget()

    def create_hyperparameter_widgets(self):
        """Create hyperparameter input widgets."""
        
        # Common CNN parameters
        self.cnn_params_frame = tk.Frame(self.hyperparams_frame)
        
        # Learning Rate
        lr_frame = tk.Frame(self.cnn_params_frame)
        lr_frame.pack(fill="x", pady=5)
        tk.Label(lr_frame, text="Learning Rate:", font=("Arial", 11)).pack(side="left")
        self.learning_rate_var = tk.StringVar(value="0.001")
        self.learning_rate_entry = tk.Entry(lr_frame, textvariable=self.learning_rate_var, 
                                           font=("Arial", 11), width=10)
        self.learning_rate_entry.pack(side="right")
        
        # Number of Epochs
        epochs_frame = tk.Frame(self.cnn_params_frame)
        epochs_frame.pack(fill="x", pady=5)
        tk.Label(epochs_frame, text="Number of Epochs:", font=("Arial", 11)).pack(side="left")
        self.epochs_var = tk.StringVar(value="50")
        self.epochs_entry = tk.Entry(epochs_frame, textvariable=self.epochs_var, 
                                    font=("Arial", 11), width=10)
        self.epochs_entry.pack(side="right")
        
        # Optimizer
        optimizer_frame = tk.Frame(self.cnn_params_frame)
        optimizer_frame.pack(fill="x", pady=5)
        tk.Label(optimizer_frame, text="Optimizer:", font=("Arial", 11)).pack(side="left")
        self.optimizer_var = tk.StringVar(value="Adam")
        self.optimizer_combo = ttk.Combobox(optimizer_frame, textvariable=self.optimizer_var,
                                           values=["Adam", "SGD", "RMSprop", "AdaGrad"],
                                           font=("Arial", 11), width=12, state="readonly")
        self.optimizer_combo.pack(side="right")
        
        # Ensemble-specific parameters
        self.ensemble_params_frame = tk.Frame(self.hyperparams_frame)
        
        # Tree Depth (for ensemble only)
        tree_depth_frame = tk.Frame(self.ensemble_params_frame)
        tree_depth_frame.pack(fill="x", pady=5)
        tk.Label(tree_depth_frame, text="Tree Depth:", font=("Arial", 11)).pack(side="left")
        self.tree_depth_var = tk.StringVar(value="10")
        self.tree_depth_entry = tk.Entry(tree_depth_frame, textvariable=self.tree_depth_var, 
                                         font=("Arial", 11), width=10)
        self.tree_depth_entry.pack(side="right")

    def load_training_data(self):
        """Load training data folder."""
        folder_path = filedialog.askdirectory(title="Select Training Data Folder")
        if folder_path:
            self.selected_data_path = Path(folder_path)
            self.data_path_label.config(text=f"Selected: {folder_path}", fg="black")
            
            # Show next step
            self.model_frame.pack(fill="x", padx=20, pady=10)
        else:
            self.data_path_label.config(text="No data selected", fg="gray")

    def on_model_selection(self):
        """Handle model architecture selection."""
        self.selected_model = self.model_var.get()
        
        # Show hyperparameters frame
        self.hyperparams_frame.pack(fill="x", padx=20, pady=10)
        
        # Hide all parameter frames first
        self.cnn_params_frame.pack_forget()
        self.ensemble_params_frame.pack_forget()
        
        # Show appropriate parameters based on selection
        if self.selected_model == "CNN":
            self.cnn_params_frame.pack(fill="x", pady=5)
        elif self.selected_model == "Ensemble":
            self.cnn_params_frame.pack(fill="x", pady=5)
            self.ensemble_params_frame.pack(fill="x", pady=5)
        
        # Show training controls
        self.training_frame.pack(fill="x", padx=20, pady=10)

    def start_training(self):
        """Start the training process."""
        # Validate inputs
        if not self.selected_data_path:
            messagebox.showerror("Error", "Please select training data folder")
            return
        
        if not self.selected_model:
            messagebox.showerror("Error", "Please select a model architecture")
            return
        
        try:
            # Validate hyperparameters
            learning_rate = float(self.learning_rate_var.get())
            epochs = int(self.epochs_var.get())
            optimizer = self.optimizer_var.get()
            
            if self.selected_model == "Ensemble":
                tree_depth = int(self.tree_depth_var.get())
            
            # Show training popup
            self.show_training_popup()
            
            # Here you would typically start the actual training process
            print(f"Starting training with:")
            print(f"Data path: {self.selected_data_path}")
            print(f"Model: {self.selected_model}")
            print(f"Learning rate: {learning_rate}")
            print(f"Epochs: {epochs}")
            print(f"Optimizer: {optimizer}")
            if self.selected_model == "Ensemble":
                print(f"Tree depth: {tree_depth}")
            
        except ValueError as e:
            messagebox.showerror("Error", "Please enter valid numeric values for hyperparameters")

    def show_training_popup(self):
        """Show training popup window with animation."""
        # Create training popup window
        self.training_popup = tk.Toplevel(self)
        self.training_popup.title("Training in Progress")
        self.training_popup.geometry("400x380")
        
        # Center the popup window
        self.training_popup.transient(self)
        self.training_popup.grab_set()
        
        # Calculate center position
        self.training_popup.update_idletasks()
        x = (self.training_popup.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.training_popup.winfo_screenheight() // 2) - (380 // 2)
        self.training_popup.geometry(f"400x380+{x}+{y}")
        
        # Title label
        title_label = tk.Label(self.training_popup, text="Training Model...", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=15)
        
        # Animation canvas in popup
        self.popup_canvas = tk.Canvas(self.training_popup, width=180, height=180)
        self.popup_canvas.pack(pady=15)
        
        # Cancel button
        cancel_button = tk.Button(self.training_popup, text="Cancel Training", 
                                 font=("Arial", 12, "bold"),
                                 command=self.cancel_training,
                                 width=15, height=2)
        cancel_button.pack(pady=15)
        
        # Start animation
        self.is_animating = True
        self.angle = 0
        self.arrow = None
        self.add_arrow()
        
        # Handle window close event
        self.training_popup.protocol("WM_DELETE_WINDOW", self.cancel_training)

    def cancel_training(self):
        """Cancel the training process and close popup."""
        self.is_animating = False
        
        if hasattr(self, 'arrow') and self.arrow is not None:
            self.popup_canvas.delete(self.arrow)
            self.arrow = None
        
        if hasattr(self, 'training_popup'):
            self.training_popup.destroy()
        
        print("Training cancelled by user")

    def add_arrow(self):
        """Create rotating animation in popup."""
        if self.is_animating and hasattr(self, 'popup_canvas'):
            # Clear previous arrow
            if self.arrow is not None:
                self.popup_canvas.delete(self.arrow)
            
            # Calculate triangle points for rotation (adjusted for 180x180 canvas)
            center_x, center_y = 90, 90  # Center of 180x180 canvas
            radius = 40  # Smaller radius for smaller canvas
            x1 = center_x + radius * math.cos(math.radians(self.angle))
            y1 = center_y + radius * math.sin(math.radians(self.angle))
            x2 = center_x + radius * math.cos(math.radians(self.angle + 120))
            y2 = center_y + radius * math.sin(math.radians(self.angle + 120))
            x3 = center_x + radius * math.cos(math.radians(self.angle + 240))
            y3 = center_y + radius * math.sin(math.radians(self.angle + 240))
            
            # Create the rotating triangle
            self.arrow = self.popup_canvas.create_polygon(x1, y1, x2, y2, x3, y3, fill='blue')
            
            # Update angle for next frame
            self.angle = (self.angle + 10) % 360
            
            # Schedule next animation frame
            self.after(100, self.add_arrow)

    def stop_training(self):
        """Stop the training process (legacy method - now handled by cancel_training)."""
        self.cancel_training()
