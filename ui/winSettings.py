from tkinter import *
from tkinter import ttk
from models.toplevel import TopWindow

class WinSettings (TopWindow):
    def __init__(self, master):
        super().__init__(master, title="Configuracion",width=800,height=600, not_rezisable=False)


        

        btn_search = ttk.Entry(self, )
        btn_search.pack()

        btns = ttk.Frame(self, padding=10)
        btns.pack(fill="x", pady=10)

        btn_exit = ttk.Button(btns, text="Salir", command=self.destroy)
        
        btn_exit.pack(side="left", expand=True, padx=5)
        
        self.mainloop()