from tkinter import *
from tkinter import ttk
from models.toplevel import TopWindow

class WinEventsRep (TopWindow):
    def __init__(self, master):
        super().__init__(master, title="Reporte de camaras",width=800,height=600, not_rezisable=False)

        btn_search = ttk.Entry(self, )
        btn_search.pack()

        btns = ttk.Frame(self, padding=10)
        btns.pack(fill="x", pady=10)

        btn_generate = ttk.Button(btns, text="Generar")
        btn_pdf = ttk.Button(btns, text="PDF")
        btn_word = ttk.Button(btns, text="WORD")
        btn_excel = ttk.Button(btns, text="EXCEL")
        btn_exit = ttk.Button(btns, text="Salir", command=self.destroy)
        
        btn_generate.pack(side="left", expand=True, padx=5)
        btn_pdf.pack(side="left", expand=True, padx=5)
        btn_word.pack(side="left", expand=True, padx=5)
        btn_excel.pack(side="left", expand=True, padx=5)
        btn_exit.pack(side="left", expand=True, padx=5)
        

        self.mainloop()