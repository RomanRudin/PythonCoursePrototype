'''
============================| DATABASE STRUCTURE |====================================
Themes TABLE columns:

Column Name |   Data Type   | Description
------------|---------------|---------------------------------------------------------
themeID     |   small INT   | id (order) of the theme
themeName   |    VARCHAR    | Name of the theme
description |     TEXT      | description of the theme of the course
markLoop    | 1 sym VARCHAR | user's saved mark of the whole theme for loop efficiency
markCond    | 1 sym VARCHAR | user's saved mark of the whole theme for condition efficiency
PRIMARY KEY = themeName
======================================================================================


Theory TABLE columns:

Column Name |   Data Type   | Description
------------|---------------|---------------------------------------------------------
theoryName  |    VARCHAR    | id (order) of the theme
theoryID    | 5 sym VARCHAR | id with the format of themeID.theoryID (ex. 11.02)
themeName   |    VARCHAR    | Name of the theme, which contains this theory part
theoryText  |      TEXT     | description of the theme of the course
PRIMARY KEY = theoryName
REFERENCES: themeName to Themes TABLE
======================================================================================


Practise TABLE columns:

Column Name |   Data Type   | Description
------------|---------------|---------------------------------------------------------
taskName    |    VARCHAR    | id (order) of the theme
taskID      | 4 sym VARCHAR | id with the format of themeID.taskID (ex. 11.02)
themeName   |    VARCHAR    | Name of the theme, which contains this task
description |      TEXT     | description of the task of the theme
inputFormat |    VARCHAR    | description of the input format for the task
outputFormat|    VARCHAR    | description of the output format for the task
markLoop    | 1 sym VARCHAR | user's saved mark of the task for loop efficiency
markCond    | 1 sym VARCHAR | user's saved mark of the task for condition efficiency
PRIMARY KEY = taskName
REFERENCES: themeName to Themes TABLE
======================================================================================


Assessment table columns:

Column Name |   Data Type   | Description
------------|---------------|---------------------------------------------------------
taskName    |    VARCHAR    | Name of the theme, which contains this theory part
testID      | 9 sym VARCHAR | id with the format of themeID.taskID.testID (ex. 11.02.95)
input       |    VARCHAR    | input data
output      |    VARCHAR    | right output data, answer of the task
visible     |    BOOLEAN    | if True can be shown to user
group       |    VARCHAR    | which type of input data this is (which group it consists to)
loop/cond columns |   INT   | difficulty, given by testing programm to my algorythms 
markLoop    | 1 sym VARCHAR | user's saved mark of the test for loop efficiency
markCond    | 1 sym VARCHAR | user's saved mark of the test for condition efficiency
PRIMARY KEY = testID
REFERENCES: taskName to Practise TABLE
======================================================================================
Loop / cycle efficiency columns, all INTEGER type with number of iterations inside them. 
Condition efficiency columns (the same as loop) #? Don't really know if I gonna do that
P.S. Letter = Column Name,  Color = color, displayed for user with the mark itself, L = light
----------------------------------------------------------------------------------
Letter | Color  | Description
----------------------------------------------------------------------------------
   S   | LBlue  | For the best result, better then what my code did
   A   | LGreen | Very efficient algorithm
   B   | Green  | Efficient algorithm
   C   | Yellow | Normal efficiency algorythm
   D   | Orange | Low efficiency algorythm
   E   | Red    | Wrong answer
'''

class AdminController:
    def destroy(self) -> None: '''
        Drops an old DB and creates a new one
    '''

    def delete(self, table: str, id: str) -> None: '''
        Deletes row in given table and id
         - id is a PRIMARY KEY of given table
    '''

    def create(self) -> None: '''
        Creates all the tables, that were described before
    '''

    def add_theme(self, order: int, name: str, description: str) -> None: '''
        Adds theme
         - order is a themeID
         - name is a themeName
         - description is a description 
    '''

    def add_theory(self, theme: str, order: int, filePath: str): '''
        Adds theory part to Theory TABLE into given theme.
         - theme is a themeNmae of the theme you add new theory article to
         - order is a theoryID (order) of this article
         - filePath is a path to the file to read info from:
            = thoeryName is the first line of file
            = theoryText is in all other lines of file
    '''

    def add_task(self, theme: str, order: int, filePath: str): '''
        Adds tasks to Practise TABLE into given theme.
         - theme is a themeNmae of the theme you add new task to
         - order is a taskID (order) of this task
         - filePath is a path to the file to read info from:
            = taskName, description, inputFormat, outputFormat are all in one file,
                separated of each other by pip symbol (|) at the end of the line
    '''

    def add_tests(self, theme: str, task: str, scripts: list, inputDataFile: str, *inputData): '''
        Adds tests to Assessment TABLE into given task. 
         - scripts is a list of paths to default programms made by me to make samples 
                for comparing user programms efficiency with
         - inputDataFile is a path to a text file woth the list of inputs to the 
                scripts to get answers of my programms to. 
            = semicolon symbol (;) needs to be used for splitting different tests, so
                they can have multiple lines 
                #TODO Make comparing of results of different programms to exclude mistakes and make notiffications about them
         - *inputData is a list of inputs to the scriptsto get answers of my programms to
    '''

    def change_data(self, table: str, id: str, **columns): '''
        Changes data to given in given table, row. ***columns must have a format of:
        {columnName: newData}
    '''