from tkinter import Tk, PhotoImage
from functions.functions import center_screen
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Window (Tk):
    def __init__(self, title, width = 800, height = 600, max_size = True):
        super().__init__()
        self.title(title)
        self.geometry(center_screen(self, width=width, height=height))

        self.minsize(width=width, height=height)
        if os.name == "nt":
            self.state("zoomed")
        else:
            self.attributes("-zoomed",True)

        if os.name == "nt":
            self.iconbitmap(resource_path("public/logo.ico"))
        else:
            icon = PhotoImage(file=resource_path("public/logo.png"))
            self.iconphoto(True, icon)