import sqlite3 as sql
from os import path
from datetime import datetime
from ..testing_programm.testingProgramm import Tester


#! NEEDS TO BE CHANGED AFTER EVERY DB RECONFIGURATION
TABLES_DEPENDENCY = {
    'Block': ['Theme'],
    'Theme': ['Task', 'Theory'],
    'Task': ['Test'],
    'Theory': '',
    'test': ''
}
TABLES_ORDER = ['Block', 'Theme','Theory','Task','Test']
TABLES_PRIMARY_KEYS = ['blockName', 'themeName', 'theoryName', 'taskName', 'testID']


class AdminController():
    def __init__(self, db_name: str) -> None:
        self.file_path = path.dirname(path.abspath(__file__))
        db_path = self.file_path.replace('\db_control', '')
        self.con = sql.connect(path.join(db_path, db_name))
        self.cursor = self.con.cursor()

    def save(self) -> None:
        self.con.commit()


    def __get_themeID(self, themeName: str) -> str:
        return str(self.cursor.execute('SELECT themeID FROM Themes WHERE themeName=?', [themeName]))


    def __get_taskID(self, taskName: str) -> str:
        return str(self.cursor.execute('SELECT taskID FROM Tasks WHERE taskName=?', [taskName]))


    def __id_column_name_getting(self, table: str) -> list:
        self.cursor.execute("SELECT * FROM ?", [table])
        primaryKey = [description[0] for description in self.cursor.description if description[0] in TABLES_PRIMARY_KEYS]
        return primaryKey[0]


    def destroy(self) -> None:
        self.backup()
        self.cursor.execute("PRAGMA writable_schema = 1")
        self.cursor.execute("DELETE FROM sqlite_master WHERE type IN ('table', 'index', 'trigger')")
        self.cursor.execute("PRAGMA writable_schema = 0")
        self.create()


    def delete(self, table: str, id: str) -> None:
        primaryKey = self.__id_column_name_getting(table)
        self.cursor.execute('''
            DELETE FROM ? WHERE ? = ?
        ''', [table,primaryKey, id])
        self.save()


    def backup(self) -> None:
        backup_name = str(datetime.now())[:-7].replace('-', '_').replace(' ', '_').replace(':', '-')
        bck = sql.connect(path.join(self.file_path, 'db_backups', f'{backup_name}.sqlite3'))
        with bck:
            self.con.backup(bck, pages=1)
        bck.close()


    def add_block(self, name: str, description: str) -> None:
        self.cursor.execute('''
            INSERT INTO Block (blockName, description)
            VALUES (?, ?)
        ''', [name, description])
        self.save()


    def add_theme(self, order: int, name: str, blockName: str, description='') -> None:
        self.cursor.execute('''
            INSERT INTO Themes (themeID, themeName, blockName, description)
            VALUES (?, ?, ?)
        ''', [order, name, blockName, description])
        self.save()


    def add_theory(self, theme: str, order: int, filePath='adminControllerFolder/theory_data.txt') -> None:
        theoryID = f'{self.__get_themeID(theme)}.{str(order)}'
        with open(str(filePath), 'r', encoding='utf-8') as file:
            theoryName = file.readline()
            theoryText = '\n'.join([file.readlines()])
        self.cursor.execute('''
            INSERT INTO Theory (theoryName, theoryID, themeName, theoryText)
            VALUES (?, ?, ?, ?)
        ''', [theoryName, theoryID, theme, theoryText])
        self.save()


    def add_task(self, theme: str, order: int, filePath='adminControllerFolder/task_data.txt') -> None:
        taskID = f'{self.__get_themeID(theme)}.{str(order)}'
        with open(filePath, 'r', encoding='utf-8') as file:
            taskName, description, inputFormat, outputFormat = file.read().split('|\n')
        self.cursor.execute('''
            INSERT INTO Tasks (taskName, taskID, themeName, description, inputFormat, outputFormat)
            VALUES (?, ?, ?, ?, ?, )
        ''', [taskName, taskID, theme, description, inputFormat, outputFormat])
        self.save()


    def add_tests(self, task: str, inputDataFile='adminControllerFolder/tests_data.txt', visibleTests=[0], *inputDataList) -> None:
        tester = Tester()
        scripts = ['AB', 'BD', 'CD', 'D']
        for path in scripts:
            with open(f'adminControllerFolder/script{path}.py', 'r') as file:
                code = file.read().splitlines()
            if code[0] != '#Done':
                with open(path, 'w') as file:
                    file.write(tester.parse(code))
        from adminControllerFolder.scriptAB import main as mainAB
        from adminControllerFolder.scriptBC import main as mainBC
        from adminControllerFolder.scriptCD import main as mainCD
        from adminControllerFolder.scriptD import main as mainD
        testID = f'{self.__get_taskID(task)}.'
        if inputDataFile != '':
            with open(inputDataFile, 'r', encoding='utf-8') as file:
                testData = file.read().split(';')
                for index, test in enumerate(testData):
                    if '||' in test:
                        testGroup, inputData = test.split('||')
                        inputData = [line for line in inputData.splitlines() if line != '']
                    else:
                        inputData = [line for line in test.splitlines() if line != '']
                        testGroup = 1
                    outputData = {'AB': mainAB(inputData), 'BC': mainBC(inputData), 
                        'CD': mainCD(inputData), 'D': mainD(inputData)}
                    if all(outputData[0][0] == answer[0] for answer in outputData.values()):  
                        self.cursor.execute('''
                            INSERT INTO Assessment (taskName, testID, input, output, visible, testGroup, AB, BC, CD, D)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', [task, testID + str(index), ' '.join(inputData)], outputData['AB'][0], 
                            index in visibleTests, testGroup,
                            outputData['AB'][1], outputData['BC'][1], outputData['CD'][1], outputData['D'][1])
                        self.save()
                    else:
                        raise ValueError(f'Different answers on the task: {inputData}')
        else: 
            for index, inputData in enumerate(*inputDataList):
                outputData = {'AB': mainAB(inputData), 'BC': mainBC(inputData), 
                    'CD': mainCD(inputData), 'D': mainD(inputData)}
                if all(outputData[0][0] == answer[0] for answer in outputData.values()):  
                    self.cursor.execute('''
                        INSERT INTO Assessment (taskName, testID, input, output, visible, testGroup, AB, BC, CD, D)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', [task, testID + str(index).ljust(3, '0'), ' '.join(inputData)], outputData['AB'][0], 
                        index in visibleTests, testGroup,
                        outputData['AB'][1], outputData['BC'][1], outputData['CD'][1], outputData['D'][1])
                    self.save()
                else:
                    raise ValueError(f'Different answers on the task: {inputData}')
        #TODO Make script for running given programms with given data or with data from inputDataFile and writing it to db


    def change_data(self, table: str, id: str, columns:dict) -> None:
        print('!!!!!!!!!!!!!!!')
        primaryKey = self.__id_column_name_getting(table)
        try:
            for column, data in columns.items():
                self.cursor.execute('''
                    UPDATE ? SET ?=? WHERE ?=?
                ''', [table, column, data, primaryKey, id])
                self.save()
        except sql.OperationalError:
            self.cursor.execute('''
                INSERT INTO ? (?) VALUES (?)
            ''', [table, column, data])
            self.save()


    def show(self, table: str, id: str) -> list:
        primaryKey = self.__id_column_name_getting(table)
        return list(self.cursor.execute('''
            SELECT * FROM ? WHERE ?=?
        ''', [table, primaryKey,  id]).fetchall())



    def create(self) -> None:
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Block (
                blockName VARCHAR(255) NOT NULL,
                description TEXT,
                markLoop VARCHAR(1),

                PRIMARY KEY (blockName)
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Themes (
                themeID INT NOT NULL,
                themeName VARCHAR(255) NOT NULL,
                blockName VARCHAR(255) NOT NULL,
                description TEXT,
                markLoop VARCHAR(1),

                PRIMARY KEY (themeName),
                FOREIGN KEY (blockName) REFERENCES Block(blockName)
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Theory (
                theoryName VARCHAR(255) NOT NULL,
                theoryID VARCHAR(5) NOT NULL,
                themeName VARCHAR(255) NOT NULL,
                theoryText TEXT,

                PRIMARY KEY (theoryName),
                FOREIGN KEY (themeName) REFERENCES Themes(themeName)
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Tasks (
                taskName VARCHAR(255) NOT NULL,
                taskID VARCHAR(5) NOT NULL,
                themeName VARCHAR(255) NOT NULL,
                description TEXT NOT NULL,
                inputFormat VARCHAR(255) NOT NULL,
                outputFormat VARCHAR(255) NOT NULL,
                markLoop VARCHAR(1),

                PRIMARY KEY (taskName),
                FOREIGN KEY (themeName) REFERENCES Themes(themeName)
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Assessment (
                taskName VARCHAR(255) NOT NULL,
                taskID VARCHAR(9) NOT NULL,
                input VARCHAR(255),
                output VARCHAR(255),
                visible BOOLEAN,
                testGroup VARCHAR(255),
                loopAB INT,
                loopBC INT,
                loopCD INT,
                loopD INT,
                markLoop VARCHAR(1),

                PRIMARY KEY (taskID),
                FOREIGN KEY (taskName) REFERENCES Tasks(taskName)
            )
        ''')


class AdminInfoGetter():
    def __init__(self, db_name: str) -> None:
        self.file_path = path.dirname(path.abspath(__file__))
        db_path = self.file_path.replace('\db_control', '')
        self.con = sql.connect(path.join(db_path, db_name))
        self.cursor = self.con.cursor()


    def __sql_identifying(self, string:str) -> str:
        return '"' + string.replace('"', '""') + '"'
    

    def primary_key_getting(self, table:str, parentID='') -> list:
        primaryKeys = [i[0] for i in self.cursor.execute(f'SELECT * FROM {table}').fetchall() if not i[0] is None]
        #Block TABLE doesn't have any parentID's, so....
        if table == 'Block':
            return primaryKeys
        #Other table's elements need parentIDs to be displayed
        rows = self.cursor.execute("PRAGMA foreign_key_list({})".format(self.__sql_identifying(table)))
        foreignKeys = list(rows.fetchall())
        result = []
        for primary, foreign in zip(primaryKeys, foreignKeys):
            if str(foreign) == parentID:
                result.append(primary)
        return result


    def table_names_getting(self) -> list:
        result = self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        return [str(name[0]) for name in result]