import sqlite3 as sql
from os import path


class MainController():
    def __init__(self, db_name) -> None:
        db_path = path.dirname(path.abspath(__file__))
        db_path = db_path.replace('\db_control', '')
        self.con = sql.connect(path.join(db_path, db_name))
        self.cursor = self.con.cursor()


    def get_blocks(self):
        return [block[0] for block in self.cursor.execute('SELECT * FROM Block').fetchall()]


    def get_themes(self, block):
        return [theme[0] for theme in self.cursor.execute('SELECT * FROM Theme WHERE blockName=?', [block]).fetchall()]


    def get_theories_and_tasks(self, theme):
        info = self.cursor.execute('SELECT * FROM Theory WHERE themeName=?', [theme]).fetchall()
        info.extend(self.cursor.execute('SELECT * FROM Task WHERE themeName=?', [theme]).fetchall())
        if info == []:
            return []
        info = info.sort(key= lambda page: page[1])
        extra_info = [0] * len(info)
        for index, enum in enumerate(info):
            if len(enum) == 4:
                extra_info[index] = '[Th]' + str(enum)
            else:
                extra_info[index] = '[Ex]' + str(enum)
        return extra_info


    def set_block(self, blockName):
        block = list(self.cursor.execute('SELECT * FROM Block WHERE BlockName=?', [blockName]).fetchall())
        return block[0]


    def set_theme(self, themeName):
        theme = list(self.cursor.execute('SELECT * FROM Theme WHERE themeName=?', [themeName]).fetchall())
        return theme[0]


    def set_theory(self, theoryName):
        theory = list(self.cursor.execute('SELECT * FROM Theory WHERE theoryName=?', [theoryName]).fetchall())
        return theory[0]


    def set_task(self, taskName):
        task = list(self.cursor.execute('SELECT * FROM Task WHERE taskName=?', [taskName]).fetchall())
        return task[0]