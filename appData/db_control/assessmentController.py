import sqlite3 as sql

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
            "loop": [
                very efficient algorythm iterations,    #? 0
                efficient algorythm iterations,         #? 1
                normal efficiency algorythm,            #? 2
                low efficiency algorythm                #? 3
            ],
            "condition": [
                very efficient algorythm iterations,    #? 0
                efficient algorythm iterations,         #? 1
                normal efficiency algorythm,            #? 2
                low efficiency algorythm                #? 3
            ]
        }
    }
    ----------------------------------------------------------
    So, everything less than 0 is S, between 0 and 1 is A, 
    between 1 and 2 is B, between 2 and 3 is C,
    more than 3 is D
    '''