import sqlite3 as sql
from os import path
from datetime import datetime
from ..testing_programm.testingProgramm import Tester

class AdminController():
    def __init__(self, db_name) -> None:
        db_path = path.dirname(path.abspath(__file__))
        db_path = db_path.replace('/db_control/', '')
        self.conn = sql.connect(path.join(db_path, db_name))

    def __get_themeID(self, themeName) -> str:
        return str(self.conn.execute('SELECT themeID FROM Themes WHERE themeName=?', [themeName]))

    def __get_taskID(self, taskName) -> str:
        return str(self.conn.execute('SELECT taskID FROM Practise WHERE taskName=?', [taskName]))

    def destroy(self):
        self.conn.execute('DROP DATABASE Course')
        self.conn.execute('CREATE DATABASE Course')


    def delete(self, table, id={}):
        self.conn.execute('''
            DELETE FROM ? WHERE ? = ?
        ''', [table, id])


    def backup(self):
        self.conn.execute('''
            BACKUP DATABASE testDB TO DISK = '?';
        ''', [str(datetime.now())])
    

    def add_theme(self, order, name, description=''):
        self.conn.execute('''
            INSERT INTO Themes (themeID, themeName, description)
            VALUES (?, ?, ?)
        ''', [order, name, description])


    def add_theory(self, theme, order, filePath):
        theoryID = f'{self.__get_themeID(theme)}.{str(order)}'
        with open(str(filePath), 'r', encoding='utf-8') as file:
            theoryName = file.readline()
            theoryText = '\n'.join([file.readlines()])
        self.conn.execute('''
            INSERT INTO Theory (theoryName, theoryID, themeName, theoryText)
            VALUES (?, ?, ?, ?)
        ''', [theoryName, theoryID, theme, theoryText])


    def add_task(self, theme, order, filePath):
        taskID = f'{self.__get_themeID(theme)}.{str(order)}'
        with open(filePath, 'r', encoding='utf-8') as file:
            taskName, description, inputFormat, outputFormat = file.read().split('|\n')
        self.conn.execute('''
            INSERT INTO Practise (taskName, taskID, themeName, description, inputFormat, outputFormat)
            VALUES (?, ?, ?, ?, ?, )
        ''', [taskName, taskID, theme, description, inputFormat, outputFormat])


    def add_tests(self, task, inputDataFile='', visibleTests=[0], *inputDataList):
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
                        group, inputData = test.split('||')
                        inputData = [line for line in inputData.splitlines() if line != '']
                    else:
                        inputData = [line for line in test.splitlines() if line != '']
                        group = 1
                    outputData = {'AB': mainAB(inputData), 'BC': mainBC(inputData), 
                        'CD': mainCD(inputData), 'D': mainD(inputData)}
                    if all(outputData[0][0] == answer[0] for answer in outputData.values()):  
                        self.conn.execute('''
                            INSERT INTO Assessment (taskName, testID, input, output, visible, group, AB, BC, CD, D)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', [task, testID + str(index), ' '.join(inputData)], outputData['AB'][0], 
                            index in visibleTests, group,
                            outputData['AB'][1], outputData['BC'][1], outputData['CD'][1], outputData['D'][1])
                    else:
                        raise ValueError(f'Different answers on the task: {inputData}')
        else: 
            for index, inputData in enumerate(*inputDataList):
                outputData = {'AB': mainAB(inputData), 'BC': mainBC(inputData), 
                    'CD': mainCD(inputData), 'D': mainD(inputData)}
                if all(outputData[0][0] == answer[0] for answer in outputData.values()):  
                    self.conn.execute('''
                        INSERT INTO Assessment (taskName, testID, input, output, visible, group, AB, BC, CD, D)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', [task, testID + str(index).ljust(3, '0'), ' '.join(inputData)], outputData['AB'][0], 
                        index in visibleTests, group,
                        outputData['AB'][1], outputData['BC'][1], outputData['CD'][1], outputData['D'][1])
                else:
                    raise ValueError(f'Different answers on the task: {inputData}')
        #TODO Make script for running given programms with given data or with data from inputDataFile and writing it to db


    def change_data(self, table, id, **columns):
        for column, data in columns.items():
            self.conn.execute('''

            ''', [table, id, column, data])


    def create(self):
        self.conn.execute('''
            CREATE TABLE Themes (
                themeOrder INT NOT NULL,
                themeName VARCHAR(255) NOT NULL,
                description TEXT,
                markLoop VARCHAR(1),

                PRIMARY KEY (themeName)
            )
        ''')

        self.conn.execute('''
            CREATE TABLE Theory (
                theoryName VARCHAR(255) NOT NULL,
                theoryID VARCHAR(5) NOT NULL,
                themeName VARCHAR(255) NOT NULL,
                theoryText TEXT,

                PRIMARY KEY (theoryName),
                FOREIGN KEY (themeName) REFERENCES Themes(themeName)
            )
        ''')

        self.conn.execute('''
            CREATE TABLE Practise (
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

        self.conn.execute('''
            CREATE TABLE Assessment (
                taskName VARCHAR(255) NOT NULL,
                taskID VARCHAR(9) NOT NULL,
                input VARCHAR(255),
                output VARCHAR(255),
                visible BOOLEAN,
                group VARCHAR(255),
                loopAB INT,
                loopBC INT,
                loopCD INT,
                loopD INT,
                markLoop VARCHAR(1),

                PRIMARY KEY (taskID),
                FOREIGN KEY (taskName) REFERENCES Practise(taskName)
            )
        ''')
