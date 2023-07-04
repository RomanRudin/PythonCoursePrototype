import sqlite3 as sql
from os import path

class AdminController():
    def __init__(self, db_name) -> None:
        db_path = path.dirname(path.abspath(__file__))
        db_path = db_path.replace('/db_control/', '')
        self.conn = sql.connect(path.join(db_path, db_name))


    def destroy(self):
        self.conn.execute('DROP DATABASE Course')
        self.conn.execute('CREATE DATABASE Course')


    def delete(self, table, id):
        self.conn.execute('''

        ''', )
    

    def add_theme(self, order, name, description=''):
        self.conn.execute('''

        ''', )


    def add_theory(self, theme, order, filePath):
        with open(str(filePath), 'r', encoding='utf-8') as file:
            theoryName = file.readline()
            theoryText = '\n'.join([file.readlines()])
        self.conn.execute('''

        ''', )


    def add_task(self, theme, order, filePath):
        with open(filePath, 'r', encoding='utf-8') as file:
            taskName, description, inputFormat, outputFormat = file.read().split('|\n')
        self.conn.execute('''

        ''', )


    def add_tests(self, task, scripts=[], inputDataFile='', *inputData):
        if not inputDataFile is None:
            with open(inputDataFile, 'r', encoding='utf-8') as file:
                testData = file.read().split(';')
                for test in testData:
                    inputData = [line for line in test.splitlines()]

        #TODO Make script for running given programms with given data or with data from inputDataFile and writing it to db


    def change_data(self, table, id, **columns):
        for column, data in columns.items():
            self.conn.execute('''

            ''', [column, data])


    def create(self):
        self.conn.execute('''
            CREATE TABLE Themes (
                themeOrder INT NOT NULL,
                themeName VARCHAR(255) NOT NULL,
                description TEXT,
                markLoop VARCHAR(1),
                markCond VARCHAR(1),

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
                markCond VARCHAR(1),

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
                conditionAB INT,
                conditionBC INT,
                conditionCD INT,
                conditionD INT,
                markLoop VARCHAR(1),
                markCond VARCHAR(1),

                PRIMARY KEY (taskID),
                FOREIGN KEY (taskName) REFERENCES Practise(taskName)
            )
        ''')
