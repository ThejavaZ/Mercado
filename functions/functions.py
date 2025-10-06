import os, subprocess
from tkinter import Tk

def cls():
    os.system("cls") if os.name == "nt" else os.system("clear")

def center_screen(tk:Tk, width:int, height:int):
    screen_width = tk.winfo_screenwidth()
    screen_height = tk.winfo_screenheight()
    w_pos = int(screen_width/2 - width/2)
    h_pos = int(screen_height/2 - height/2)
    return f"{width}x{height}+{w_pos}+{h_pos}"

def download_dependences():    
    result = subprocess.run(
        ["pip", "install", "-r", "requirements.txt"],
        check=True,
        text=True,
        capture_output=True
    )
    print("✅ Dependencias instaladas correctamente.")
    print(result.stdout)  # Muestra la salida del comando


def start_env():
    os.system(r".\venv\bin\activate") if os.name == "nt" else os.system("source ./.venv/bin/activate")