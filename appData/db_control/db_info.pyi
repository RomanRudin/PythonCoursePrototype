'''
============================| DATABASE STRUCTURE |====================================

Block TABLE columns:

Column Name |   Data Type   | Description
------------|---------------|---------------------------------------------------------
blockName   |    VARCHAR    | Name of the theme
description |     TEXT      | description of the theme of the course
markLoop    | 1 sym VARCHAR | user's saved mark of the whole theme for loop efficiency
PRIMARY KEY = blockName
======================================================================================

-
Themes TABLE columns:

Column Name |   Data Type   | Description
------------|---------------|---------------------------------------------------------
themeID     |   small INT   | id (order) of the theme
themeName   |    VARCHAR    | Name of the theme
blockName   |    VARCHAR    | Name of the block theme is related to 
description |     TEXT      | description of the theme of the course
markLoop    | 1 sym VARCHAR | user's saved mark of the whole theme for loop efficiency
PRIMARY KEY = themeName
REFERENCES: blockName to Block TABLE
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
taskID      | 5 sym VARCHAR | id with the format of themeID.taskID (ex. 11.02)
themeName   |    VARCHAR    | Name of the theme, which contains this task
description |      TEXT     | description of the task of the theme
inputFormat |    VARCHAR    | description of the input format for the task
outputFormat|    VARCHAR    | description of the output format for the task
markLoop    | 1 sym VARCHAR | user's saved mark of the task for loop efficiency
PRIMARY KEY = taskName
REFERENCES: themeName to Themes TABLE
======================================================================================


Assessment TABLE columns:

Column Name |   Data Type   | Description
------------|---------------|---------------------------------------------------------
taskName    |    VARCHAR    | Name of the theme, which contains this theory part
testID      | 9 sym VARCHAR | id with the format of themeID.taskID.testID (ex. 11.02.95)
input       |    VARCHAR    | input data
output      |    VARCHAR    | right output data, answer of the task
visible     |    BOOLEAN    | if True can be shown to user
testGroup       |    VARCHAR    | which type of input data this is (which testGroup it consists to)
loop columns|    VARCHAR    | difficulty, given by testing programm to my algorythms 
markLoop    | 1 sym VARCHAR | user's saved mark of the test for loop efficiency
PRIMARY KEY = testID
REFERENCES: taskName to Practise TABLE
======================================================================================
Loop / cycle efficiency columns, all INTEGER type with number of iterations inside them. 
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

    def save() -> None: '''
        Commits changes of the DB
    '''

    def delete(self, table: str, id: str) -> None: '''
        Deletes row in given table and id
         - id is a PRIMARY KEY of given table
    '''

    def create(self) -> None: '''
        Creates all the tables, that were described before
    '''
    
    def add_block(self, name: str, description: str) -> None: '''
        Adds block of themes
    '''

    def add_theme(self, order: int, name: str, blockName:str, description: str) -> None: '''
        Adds theme
         - order is a themeID
         - name is a themeName
         - blovkName is a name of the block theme is connected to
         - description is a description 
    '''

    def add_theory(self, theme: str, order: int, filePath: str): '''
        Adds theory part to Theory TABLE into given theme.
         - theme is a themeNmae of the theme you add new theory article to
         - order is a theoryID (order) of this article
         - filePath is a path to the file to read info from:
                default is 'adminControllerFolder/theory_data.txt'
            = thoeryName is the first line of file
            = theoryText is in all other lines of file
    '''

    def add_task(self, theme: str, order: int, filePath: str): '''
        Adds tasks to Practise TABLE into given theme.
         - theme is a themeNmae of the theme you add new task to
         - order is a taskID (order) of this task
         - filePath is a path to the file to read info from:
                default is 'adminControllerFolder/theory_data.txt'
            = taskName, description, inputFormat, outputFormat are all in one file,
                separated of each other by pip symbol (|) at the end of the line
    '''

    def add_tests(self, theme: str, task: str, scripts: list, inputDataFile: str, *inputData): '''
        Adds tests to Assessment TABLE into given task. 
         - inputDataFile is a path to a text file woth the list of inputs to the 
                scripts to get answers of my programms to. 
                default is 'adminControllerFolder/theory_data.txt'
            = semicolon symbol (;) needs to be used for splitting different tests, so
                they can have multiple lines 
            = double pipe symbol (||) needs to be used for getting special group to test
         - *inputData is a list of inputs to the scriptsto get answers of my programms to
    '''

    def change_data(self, table: str, id: str, columns:dict): '''
        Changes data to given in given table, row. *columns must have a format of:
        {columnName: newData}
    '''

    def show(self, table, id) -> list: '''
        Returns row of the table with the primary key == id
         - table is a table where search is going on
         - id is an identificator of the row (primary key) to look for row
    '''



class AdminInfoGetter(): #gives info about tables and row. Used in NavBar in adminWindow
    def sql_identifying(self, string:str) -> str: '''
        String formatter for good selection and fetching
    '''
    

    def primary_key_getting(self, table:str, parentID='') -> list:'''
        If table is not the highest in Tables hierarchy (in this version - if it is not 
            'Block' table) returns all the primary keys of the rows, taht were referencing
            to parentID primary key in parent table. Else just returns all the primary keys.
             - table is a table primary keys from which programm needs
             - parentID is a primary key of the parent table chosen by user
    '''


    def table_names_getting(self) -> list:'''
        returns list of all the existsing tables names
    '''