from tkinter import Toplevel,Tk, PhotoImage
from functions.functions import center_screen
import os

class TopWindow (Toplevel):
    def __init__(self, master: Tk, title, width = 500, height = 400, not_rezisable = True):
        super().__init__(master)

        self.title(title)
        self.geometry(center_screen(self, width=width, height=height))

        self.transient(master)

        self.minsize(width=width, height=height)

        if not_rezisable:
            self.resizable(False, False)


        if os.name == "nt":
            self.iconbitmap("./public/logo.ico")
        else:
            icon = PhotoImage(file="./public/logo.png")
            self.iconphoto(True, icon)

        self.focus_force()
        self.grab_set()