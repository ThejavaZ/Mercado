from tkinter import *
from tkinter import ttk
from models.toplevel import TopWindow

class WinCameras (TopWindow):
    def __init__(self, master):
        super().__init__(master, title="Camaras",width=800,height=600, not_rezisable=False)



        header = ttk.Frame(self, padding=10)
        header.pack(fill="x", pady=1)

        title = ttk.Label(self, text="Camaras")
        title.pack(side="top")

        search_entry = ttk.Entry(header)
        search_entry.pack(side="left",fill="x",expand=True, padx=5)

        btn_search = ttk.Button(header, text="Buscar")
        btn_search.pack(side="left", padx=5)

        btns = ttk.Frame(self, padding=10)
        btns.pack(fill="x", pady=10)

        btn_add = ttk.Button(btns, text="Agregar")
        btn_edit = ttk.Button(btns, text="Editar")
        btn_delete = ttk.Button(btns, text="Eliminar")
        btn_exit = ttk.Button(btns, text="Salir", command=self.destroy)
        
        btn_add.pack(side="left", expand=True, padx=5)
        btn_edit.pack(side="left", expand=True, padx=5)
        btn_delete.pack(side="left", expand=True, padx=5)
        btn_exit.pack(side="left", expand=True, padx=5)
        
        self.mainloop()