from tkinter import Tk, PhotoImage
from functions.functions import center_screen
import os

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
            self.iconbitmap("./public/logo.ico")
        else:
            icon = PhotoImage(file="./public/logo.png")
            self.iconphoto(True, icon)