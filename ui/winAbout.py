from tkinter import *
from tkinter import ttk
from models.toplevel import TopWindow

class WinAbout (TopWindow):
    def __init__(self, master):
        super().__init__(master, title="Acerca de Sisa",width=600,height=400, not_rezisable=False)

        title = ttk.Label(self, text="Camaras", style=('bold', 16))
        title.pack()

        

        btn_search = ttk.Entry(self, )
        btn_search.pack()

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