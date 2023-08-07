from appData.graphics.GUI.mainWindow import MainWindow
from PyQt5.QtWidgets import QApplication
from sys import argv, exit

git_repo = ''

if __name__ == "__main__":
    # try:
        # controller = CMDController()
        # controller.pull(git_repo)
        app = QApplication([argv]) 
        with open(r'appData\graphics\styles\mainWindow.qss', 'r') as file:     
            app.setStyleSheet(file.read())  
        main = MainWindow()
        main.setWindowTitle('Python Course')
        main.resize(1200, 800)
        main.show()        
        exit(app.exec_())
    # except Exception as e:
    #     with open('logs/debug_log.txt', 'w') as file:
    #         file.write(str(e))