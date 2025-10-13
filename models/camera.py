class Camera:
    def __init__(self, name:str, ip:str, username:str, password:str, port:int = 554, id:int = None):
        self.id = id
        self.name = name
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password

    def get_rtsp_url(self) -> str:
        """
        Construye la URL RTSP para la cámara.
        Nota: La ruta final puede variar según el fabricante (ej. /stream1, /cam/realmonitor, etc.).
        """
        return f"rtsp://{self.username}:{self.password}@{self.ip}:{self.port}/stream1"
