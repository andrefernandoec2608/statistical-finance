import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "personalfinance.db"
class DatabaseConnection:

    def __init__(self):
        self.db_path = DB_PATH
        self._connection = None
    
    def get_connection(self) -> sqlite3.Connection: 
        if self._connection is None:
            self._connection = sqlite3.connect(self.db_path, check_same_thread=False)
            self._connection.row_factory = sqlite3.Row
        return self._connection
    
    def __enter__(self):
        return self.get_connection()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        conn = self._connection
        if conn is not None:
            if exc_type is None:
                conn.commit()
            else:
                conn.rollback()
            conn.close()
            self._connection = None
        return False