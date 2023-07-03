import sqlite3 as sql
from os import path

'''

'''

class AdminController():
    def __init__(self, db_name) -> None:
        db_path = path.dirname(path.abspath(__file__))
        db_path = db_path.replace('/db_control/', '')
        self.conn = sql.connect(path.join(db_path, db_name))