from PIL import Image, ImageTk


def get_window_center_coordinates(root, desired_window_height, desired_window_width):
    # Get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate position coordinates
    position_top = int(screen_height / 2 - desired_window_height / 2)
    position_right = int(screen_width / 2 - desired_window_width / 2)

    return position_right, position_top


def load_image(image_path):
    """
    Loads an image from the given path.
    :param image_path: path of image to load
    :return: loaded image
    """
    image = Image.open(image_path)
    photo = ImageTk.PhotoImage(image)
    return photo