''' 
Assessment table columns:

Column Name | Data Type | Description
------------|-----------|---------------------------------------------------------
testID      | TINYINT   | id (order) of the test task
input       | VARCHAR   | input data
output      | VARCHAR   | right output data, answer of the task
visible     | BOOLEAN   | if True can be shown to user
group       | TINYINT   | which type of input data this is (which group it consists to)
==================================================================================
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
   F   | Red    | Wrong answer
'''

def get_assessment(taskID) -> dict: #tskID is ID of the exersize, not of the test task
    '''
    Returns dict with the format:
    ---------------------------------------------------------
    {
        "1" : {
            "input" : "",
            "output": "",
            "visible": True, #? or False
            "group": "",
            "Loop": [
                best algorythm iterations,          #? 0
                efficient algorythm iterations,     #? 1
                normal efficiency algorythm         #? 2
            ]
        }
    }
    ----------------------------------------------------------
    So, everything less than 0 is S, between 0 and 1 is A...
    ...more than 2 is D
    '''