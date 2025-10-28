from tkinter import *
from tkinter import ttk
from models.toplevel import TopWindow
from models.datagrid import DataGrid
from database.database import Database

class WinEvents(TopWindow):
    def __init__(self, master):
        super().__init__(master, title="Mercado - Eventos", width=800, height=600, not_rezisable=False)
        self.db = Database()

        # Contenedor principal
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # DataGrid
        dg_frame = ttk.Frame(main_frame)
        dg_frame.pack(fill="both", expand=True)

        self.datagrid = DataGrid(dg_frame, width=780, height=500)
        self.datagrid.add_columns(
            columns=["ID", "Cámara", "Fecha y Hora", "Descripción"],
            widths=[10, 100, 150, 480]
        )
        self.load_events()

        # CRUD y Salir
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill="x", pady=(0, 10))

        btn_add = ttk.Button(btn_frame, text="Agregar")
        btn_edit = ttk.Button(btn_frame, text="Editar")
        btn_delete = ttk.Button(btn_frame, text="Eliminar")
        btn_exit = ttk.Button(btn_frame, text="Salir", command=self.destroy)

        btn_add.pack(side="left", expand=True, padx=5)
        btn_edit.pack(side="left", expand=True, padx=5)
        btn_delete.pack(side="left", expand=True, padx=5)
        btn_exit.pack(side="right", expand=True, padx=5)



    def load_events(self):
        self.datagrid.clear()
        events = self.db.get_events()
        for event in events:
            self.datagrid.insert_row(
                values=[event.id, event.camera_id, event.timestamp, event.description]
            )

if __name__ == "__main__":
    from tkinter import Tk
    root = Tk()
    app = WinEvents(root)
    root.mainloop()