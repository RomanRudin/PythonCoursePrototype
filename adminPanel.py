from appData.graphics.GUI.adminWindow import adminPanel, AdminController
from PyQt5.QtWidgets import QApplication
from sys import argv, exit

mode = 'app' # 'cmd' or 'app'

if __name__ == "__main__":
    if mode == 'cmd':
        controller = AdminController('db.sqlite3')
        controller.add_block('test1', '1')
        controller.add_block('test2', '2')
        controller.add_block('test3', '3')

    elif mode == 'app':
        app = QApplication([argv]) 
    
        main = adminPanel('db.sqlite3')
        main.setWindowTitle('Admin Panel')
        main.resize(1600, 900)

        main.show()
        main.showMaximized()

        exit(app.exec_())