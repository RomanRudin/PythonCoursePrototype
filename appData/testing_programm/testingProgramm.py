from json import load
from ..db_control.assessmentController import get_assessment



class Tester():
    def __init__(self) -> None:
        self.marks = []
        self.marks_distribution = ['S', 'A', 'B', 'C', 'D']
        with open('parse_mode.json', 'r') as file:
            self.iterators = load(file)


    #Executes with the change of the excersize, writes data from DB to self.assessmentData
    def change_task(self, taskID):
        self.assessmentData = get_assessment(taskID)
    

    #returns marks of the effficiency of the programm + final mark
    #TODO make it possible to have multiple efficiency tester marks
    def get_efficiency(self) -> tuple: # -> list, str
        with open('.../userData/currentCode.py', 'r') as file:
            code = file.read().splitlines()
        with open('.../userData/currentCode.py', 'w') as file:
            file.write(self.parse(code))
        self.marks = []
        main_mark_list = []
        from ...userData.currentCode import main
        for testData in self.assessmentData.values():
            answer, loopIterations = main(testData["input"]) 
            if answer == testData["output"]:
                index_loop = 4
                while loopIterations <= testData['loop'][index_loop] and index_loop >= 0:
                    index_loop -= 1
                self.marks.append(self.marks_distribution[index_loop]) 
                main_mark_list.append(index_loop)               
            else:
                self.marks.append('F')
                main_mark_list.append([100000, 100000])
        main_mark = sum(i for i in main_mark_list) / len(main_mark_list)
        for mark in main_mark:
            if mark < 1:
                main_mark = 'S'
            elif mark == 1:
                main_mark = 'A'
            elif 1 < mark <= 2:
                main_mark = 'B'
            elif 2 < mark <= 3:
                main_mark = 'C'
            elif 3 < mark <= 4:
                main_mark = 'D'
            elif mark > 4:
                main_mark = 'E'
        
        return main_mark, self.marks
            
        
        
                




    #includes counters of the efficiency into the algorythm
    '''
    After every loop / if statement inside the body of the statement variables implementation adds. On the first lines of code iteration_variable = 0 adds #? 0
    Last print is gonna be detected as the answer for code, so I have printStatementFound flag to change print on answerToTestTask only once. But if there can be many answers inside one
     print statement, so I don''t delete ( ans ) with peint and answer becomes tuple. But this way in every exersize output format needs to be in the format of print(a, b, c) #? 1 
    Every input statement is changed to element of testTaskInputData list with replacing 'input(' and ')' #? 2
    Finally, all the code is now inside main() function with the arguments of *testTaskInputData list. This function returns answer of the code and all the iteration counting variables #? 3
    ''' 
    def parse(self, code): #TODO PLEASE THIS WON'T EVEN WORK PROPERLY, NEEDS TO BE CHANGED COMPLETELY, cause it will work like n ** 2 + n instead of n ** 2 
        #? On the other hand - I'm going to write those code examples with data and marks will be given, depending only on my result, so this function will work correctly most of the time 
        printStatementFound = False                                                                             #? 1
        inputCounter = 0
        for index, line in enumerate(reversed(code)):
            line.ljust(1, '\t')                                                                                 #? 3
            for variable, iterator in self.iterators.items():                                                   #? 0
                if iterator in line:                                                                            #? 0
                    code.insert(len(code) - index + 1, f'{variable} += 1'.ljust(line.count('\t') + 1, '\t'))    #? 0
            if (not printStatementFound) and ("print(" in line):                                                #? 1 
                line = line.replace('print', 'answerToTestTask = ', 1)                                          #? 1
            if 'input(' in line:                                                                                #? 2
                line = line.replace('input(', f'testTaskInputData[{inputCounter}]')                             #? 2
                line = line.replace(')', '', 1)                                                                 #? 2
                inputCounter += 1                                                                               #? 2
        code.insert(0, 'def main(*testTaskInputData):')                                                         #? 3
        for variable, iterator in self.iterators.items():                                                       #? 0
            code.insert(1, f'{variable} = 0')                                                                   #? 0
        returner = 'return answerToTestTask, '                                                                  #? 3
        for variable in self.iterators.keys():                                                                  #? 3
            returner += f'{variable}, '                                                                         #? 3
        code.append(returner)                                                                                   #? 3
        return '\n'.join(code)
                

