
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import cv2
from PIL import Image, ImageTk
from ultralytics import YOLO

from models.camera import Camera
from database.database import Database

class WinCameras(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Administrador de Cámaras")
        self.geometry("1280x720")
        self.grab_set()

        # --- Inicialización de variables ---
        self.db = Database()
        self.cameras_map = {}
        self.video_thread = None
        self.stop_thread = threading.Event()
        
        # Cargar modelo YOLO una vez
        try:
            self.yolo_model = YOLO('models/best.pt')
        except Exception as e:
            messagebox.showerror("Error de Modelo", f"No se pudo cargar el modelo YOLO 'models/best.pt'.\n{e}")
            self.destroy()
            return

        # --- Layout Principal ---
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)

        # --- Panel Izquierdo (Listado de Cámaras) ---
        left_pane = ttk.Frame(main_frame, padding=5)
        left_pane.grid(row=0, column=0, sticky="ns", padx=(0, 5))

        ttk.Label(left_pane, text="Cámaras", font=("Helvetica", 12, "bold")).pack(pady=5)
        
        self.camera_listbox = tk.Listbox(left_pane, exportselection=False, width=30)
        self.camera_listbox.pack(fill=tk.BOTH, expand=True)
        self.camera_listbox.bind("<<ListboxSelect>>", self._on_camera_select)

        # --- Panel Derecho (Visualización) ---
        right_pane = ttk.Frame(main_frame, padding=5)
        right_pane.grid(row=0, column=1, sticky="nsew")
        
        self.video_label = ttk.Label(right_pane, text="Seleccione una cámara para iniciar la visualización", 
                                     font=("Helvetica", 14), anchor="center", background="black", foreground="white")
        self.video_label.pack(fill=tk.BOTH, expand=True)

        # --- Panel Inferior (Botones) ---
        button_frame = ttk.Frame(self, padding=10)
        button_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.add_button = ttk.Button(button_frame, text="Agregar", command=self._show_add_edit_window)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.edit_button = ttk.Button(button_frame, text="Editar", state="disabled", command=lambda: self._show_add_edit_window(edit_mode=True))
        self.edit_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = ttk.Button(butPIL._tkinter_finderton_frame, text="Eliminar", state="disabled", command=self._delete_camera)
        self.delete_button.pack(side=tk.LEFT, padx=5)
        
        self.exit_button = ttk.Button(button_frame, text="Salir", command=self.close_window)
        self.exit_button.pack(side=tk.RIGHT, padx=5)

        self.protocol("WM_DELETE_WINDOW", self.close_window)
        self._populate_camera_list()

    def close_window(self):
        """Detiene el hilo de video y cierra la ventana de forma segura."""
        self._stop_video_thread()
        self.destroy()

    def _populate_camera_list(self):
        """Carga las cámaras de la BD y las muestra en el Listbox."""
        self._stop_video_thread()
        self.camera_listbox.delete(0, tk.END)
        self.cameras_map.clear()
        
        cameras = self.db.get_all_cameras()
        for cam in cameras:
            self.camera_listbox.insert(tk.END, cam.name)
            self.cameras_map[cam.name] = cam
        
        self._on_camera_select(None)

    def _on_camera_select(self, event):
        """Maneja la selección de una cámara en el Listbox."""
        selected_indices = self.camera_listbox.curselection()
        if selected_indices:
            self.edit_button.config(state="normal")
            self.delete_button.config(state="normal")
            
            selected_name = self.camera_listbox.get(selected_indices[0])
            camera = self.cameras_map[selected_name]
            self._start_video_thread(camera)
        else:
            self.edit_button.config(state="disabled")
            self.delete_button.config(state="disabled")
            self._stop_video_thread()

    def _start_video_thread(self, camera):
        """Inicia el hilo para el procesamiento de video."""
        if self.video_thread is not None:
            self._stop_video_thread()

        self.stop_thread.clear()
        self.video_thread = threading.Thread(target=self._video_loop, args=(camera,), daemon=True)
        self.video_thread.start()

    def _stop_video_thread(self):
        """Señala al hilo de video que se detenga."""
        if self.video_thread and self.video_thread.is_alive():
            self.stop_thread.set()
            self.video_thread.join(timeout=1) # Espera un poco a que el hilo termine
        self.video_thread = None
        self.video_label.config(image=None, text="Seleccione una cámara para iniciar la visualización")
        self.video_label.image = None


    def _video_loop(self, camera: Camera):
        """El ciclo principal de captura y procesamiento de video que corre en un hilo."""
        cap = None
        try:
            rtsp_url = camera.get_rtsp_url()
            self.video_label.after(0, lambda: self.video_label.config(text=f"Conectando a {camera.name}..."))
            
            cap = cv2.VideoCapture(rtsp_url)
            if not cap.isOpened():
                self.video_label.after(0, lambda: self.video_label.config(text=f"Error al conectar con la cámara {camera.name}"))
                return

            while not self.stop_thread.is_set():
                ret, frame = cap.read()
                if not ret:
                    break

                # Realizar detección
                results = self.yolo_model(frame, verbose=False)
                annotated_frame = results[0].plot()

                # Convertir para Tkinter
                h, w, _ = annotated_frame.shape
                aspect_ratio = w / h
                
                label_w = self.video_label.winfo_width()
                label_h = self.video_label.winfo_height()

                new_w = label_w
                new_h = int(new_w / aspect_ratio)

                if new_h > label_h:
                    new_h = label_h
                    new_w = int(new_h * aspect_ratio)

                # Prevenir error si la ventana no está visible aún
                if new_w > 0 and new_h > 0:
                    resized_frame = cv2.resize(annotated_frame, (new_w, new_h))
                    rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
                    
                    pil_image = Image.fromarray(rgb_frame)
                    tk_image = ImageTk.PhotoImage(image=pil_image)
                    
                    # Actualizar UI desde el hilo principal
                    self.video_label.after(0, self._update_video_label, tk_image)

        except Exception as e:
            print(f"Error en el hilo de video: {e}") # Log para depuración
        finally:
            if cap:
                cap.release()
            if not self.stop_thread.is_set():
                 self.video_label.after(0, lambda: self.video_label.config(text=f"Se perdió la conexión con {camera.name}"))

    def _update_video_label(self, tk_image):
        """Función auxiliar para actualizar el label de video en el hilo principal."""
        if not self.stop_thread.is_set():
            self.video_label.config(image=tk_image, text="")
            self.video_label.image = tk_image

    def _delete_camera(self):
        """Elimina la cámara seleccionada."""
        selected_indices = self.camera_listbox.curselection()
        if not selected_indices:
            return
        
        selected_name = self.camera_listbox.get(selected_indices[0])
        cam_to_delete = self.cameras_map[selected_name]

        if messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de que desea eliminar la cámara '{selected_name}'?"):
            self.db.delete_camera(cam_to_delete.id)
            self._populate_camera_list()

    def _show_add_edit_window(self, edit_mode=False):
        """Muestra una ventana Toplevel para agregar o editar una cámara."""
        
        selected_cam = None
        if edit_mode:
            selected_indices = self.camera_listbox.curselection()
            if not selected_indices:
                return
            selected_name = self.camera_listbox.get(selected_indices[0])
            selected_cam = self.cameras_map[selected_name]

        # --- Ventana Emergente ---
        win = tk.Toplevel(self)
        win.title("Editar Cámara" if edit_mode else "Agregar Cámara")
        win.grab_set()
        
        form_frame = ttk.Frame(win, padding=20)
        form_frame.pack(expand=True, fill=tk.BOTH)

        fields = ["Nombre", "IP", "Usuario", "Contraseña", "Puerto"]
        entries = {}

        for i, field in enumerate(fields):
            ttk.Label(form_frame, text=f"{field}:").grid(row=i, column=0, sticky="w", pady=2, padx=5)
            entry = ttk.Entry(form_frame, width=40)
            entry.grid(row=i, column=1, sticky="ew", pady=2, padx=5)
            entries[field] = entry

        # Pre-llenar datos si es modo edición
        if edit_mode and selected_cam:
            entries["Nombre"].insert(0, selected_cam.name)
            entries["IP"].insert(0, selected_cam.ip)
            entries["Usuario"].insert(0, selected_cam.username)
            entries["Contraseña"].insert(0, selected_cam.password)
            entries["Puerto"].insert(0, str(selected_cam.port))

        def on_save():
            try:
                name = entries["Nombre"].get()
                ip = entries["IP"].get()
                user = entries["Usuario"].get()
                pwd = entries["Contraseña"].get()
                port = int(entries["Puerto"].get())

                if not all([name, ip, user]):
                    messagebox.showerror("Error", "Nombre, IP y Usuario son campos obligatorios.", parent=win)
                    return

                new_cam = Camera(
                    id=selected_cam.id if edit_mode else None,
                    name=name, ip=ip, username=user, password=pwd, port=port
                )

                if edit_mode:
                    self.db.update_camera(new_cam)
                else:
                    self.db.add_camera(new_cam)
                
                self._populate_camera_list()
                win.destroy()

            except ValueError:
                messagebox.showerror("Error", "El puerto debe ser un número.", parent=win)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar la cámara.\nError: {e}", parent=win)

        save_button = ttk.Button(form_frame, text="Guardar", command=on_save)
        save_button.grid(row=len(fields), columnspan=2, pady=10)
