import sqlite3

class Database:
    def __init__(self, path:str = "./database.db"):
        self.path = path
    
    def connection(self):
        try:
            with sqlite3.connect(database=self.path):
                return True
        except Exception as ex:
            return print(f"Error: {ex}")

    def query(self):
        try:
            self.connection()
            cursor = self
        except Exception as ex:
            return print(f"Error: {ex}")