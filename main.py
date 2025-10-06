from functions.functions import cls, download_dependences, start_env
from ui.winMain import WinMain

class Main:
    WinMain()

start_env()
download_dependences()
cls()
Main()