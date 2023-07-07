import sqlite3 as sql
from os import path
from datetime import datetime
from ..testing_programm.testingProgramm import Tester

class AdminController():
    def __init__(self, db_name) -> None:
        self.file_path = path.dirname(path.abspath(__file__))
        db_path = self.file_path.replace('\db_control', '')
        self.con = sql.connect(path.join(db_path, db_name))
        self.cursor = self.con.cursor()

    def save(self):
        self.con.commit()

    def __get_themeID(self, themeName) -> str:
        return str(self.cursor.execute('SELECT themeID FROM Themes WHERE themeName=?', [themeName]))

    def __get_taskID(self, taskName) -> str:
        return str(self.cursor.execute('SELECT taskID FROM Practise WHERE taskName=?', [taskName]))

    def destroy(self):
        self.backup()
        self.cursor.execute("PRAGMA writable_schema = 1")
        self.cursor.execute("DELETE FROM sqlite_master WHERE type IN ('table', 'index', 'trigger')")
        self.cursor.execute("PRAGMA writable_schema = 0")
        self.create()


    def delete(self, table, id={}):
        self.cursor.execute('''
            DELETE FROM ? WHERE ? = ?
        ''', [table, id])
        self.save()


    def backup(self):
        backup_name = str(datetime.now())[:-7].replace('-', '_').replace(' ', '_').replace(':', '-')
        bck = sql.connect(path.join(self.file_path, 'db_backups', f'{backup_name}.sqlite3'))
        with bck:
            self.con.backup(bck, pages=1)
        bck.close()
    

    def add_theme(self, order, name, description=''):
        self.cursor.execute('''
            INSERT INTO Themes (themeID, themeName, description)
            VALUES (?, ?, ?)
        ''', [order, name, description])
        self.save()


    def add_theory(self, theme, order, filePath='adminControllerFolder/theory_data.txt'):
        theoryID = f'{self.__get_themeID(theme)}.{str(order)}'
        with open(str(filePath), 'r', encoding='utf-8') as file:
            theoryName = file.readline()
            theoryText = '\n'.join([file.readlines()])
        self.cursor.execute('''
            INSERT INTO Theory (theoryName, theoryID, themeName, theoryText)
            VALUES (?, ?, ?, ?)
        ''', [theoryName, theoryID, theme, theoryText])
        self.save()


    def add_task(self, theme, order, filePath='adminControllerFolder/task_data.txt'):
        taskID = f'{self.__get_themeID(theme)}.{str(order)}'
        with open(filePath, 'r', encoding='utf-8') as file:
            taskName, description, inputFormat, outputFormat = file.read().split('|\n')
        self.cursor.execute('''
            INSERT INTO Practise (taskName, taskID, themeName, description, inputFormat, outputFormat)
            VALUES (?, ?, ?, ?, ?, )
        ''', [taskName, taskID, theme, description, inputFormat, outputFormat])
        self.save()


    def add_tests(self, task, inputDataFile='adminControllerFolder/tests_data.txt', visibleTests=[0], *inputDataList):
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


    def change_data(self, table, id, **columns):
        for column, data in columns.items():
            self.cursor.execute('''

            ''', [table, id, column, data])
            self.save()


    def create(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Themes (
                themeID INT NOT NULL,
                themeName VARCHAR(255) NOT NULL,
                description TEXT,
                markLoop VARCHAR(1),

                PRIMARY KEY (themeName)
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
            CREATE TABLE IF NOT EXISTS Practise (
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
                FOREIGN KEY (taskName) REFERENCES Practise(taskName)
            )
        ''')
