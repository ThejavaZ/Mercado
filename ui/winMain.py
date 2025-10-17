from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from models.window import Window
import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# --- Archive
from ui.winSettings import WinSettings
# --- Cataloges
from ui.winCameras import WinCameras
from ui.winEvents import WinEvents
# --- Reportes
from ui.winCamerasReport import WinCamerasRep
from ui.winEventsReport import WinEventsRep
from ui.winEvenCamRep import WinEventCamRep
# --- Preferences
from ui.winAbout import WinAbout
class WinMain (Window):
    def __init__(self):
        super().__init__(title="Mercado")
        
        self.menu = Menu()
        
        self.archive = Menu(self.menu, tearoff=False)
        self.cateloges = Menu(self.menu, tearoff=False)
        self.reports = Menu(self.menu, tearoff=False)
        self.preferences = Menu(self.menu, tearoff=False)

        self.menu.add_cascade(menu=self.archive, label="Archivo")
        self.menu.add_cascade(menu=self.cateloges, label="Catalogos")
        self.menu.add_cascade(menu=self.reports, label="Reportes")
        self.menu.add_cascade(menu=self.preferences, label="Preferencias")

        self.archive.add_command(label="Ayuda")
        self.archive.add_command(label="Configuracion", command=lambda:WinSettings(self))
        self.archive.add_command(label="Salir", command=self.destroy)
        
        self.cateloges.add_command(label="Camaras", command= lambda:WinCameras(self))
        self.cateloges.add_command(label="Eventos", command=lambda:WinEvents(self))

        self.reports.add_command(label="Reporte de Camaras", command=lambda:WinCamerasRep(self))
        self.reports.add_command(label="Reporte de Eventos", command=lambda:WinEventsRep(self))
        self.reports.add_command(label="Reporte de Evento por camara", command=lambda:WinEventCamRep(self))

        self.preferences.add_command(label="Terminos y condiciones")
        self.preferences.add_command(label="Politicias de privacidad")
        self.preferences.add_command(label="Acerca de sisa", command=lambda:WinAbout(self))

        image = Image.open(resource_path("public/logo.png"))

        image = image.resize((300, 200), resample=Image.Resampling.LANCZOS)
        image_tk = ImageTk.PhotoImage(image=image)

        label_image = ttk.Label(self, image=image_tk)
        label_image.pack(expand=True, anchor="center")


        self.config(menu=self.menu)
        self.focus_force()
        self.mainloop()