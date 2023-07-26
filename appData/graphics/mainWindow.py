from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QPushButton, QLabel
from ..db_control.mainController import MainController

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = MainController('db.sqlite3')
        main_layout = QHBoxLayout()

        self.content = QVBoxLayout()

        list_layout = QHBoxLayout()
    
        self.block_list = QListWidget()
        self.block_list.addItems(self.controller.get_blocks())
        self.block_list.clicked.connect(self.block_clicked)
        list_layout.addWidget(self.block_list)

        self.theme_list = QListWidget()
        self.theme_list.clicked.connect(self.theme_clicked)
        list_layout.addWidget(self.theme_list)

        self.task_and_theory_list = QListWidget()
        self.task_and_theory_list.clicked.connect(self.theory_and_task_determinant)
        list_layout.addWidget(self.task_and_theory_list)

        main_layout.addLayout(list_layout)
        main_layout.addLayout(self.content)

        self.setLayout(main_layout)


    def block_clicked(self):
        block = self.block_list.selectedItems()[0].text() 
        self.theme_list.clear()



    def theme_clicked(self):
        block = self.theme_list.selectedItems()[0].text() 
        self.task_and_theory_list.clear()


    def theory_and_task_determinant(self):
        determinant = self.task_and_theory_list.selectedItems()[0].text() 
        match determinant[:4]:
            case '[Th]':
                self.theory_clicked(determinant[4:])
            case '[Ex]':
                self.task_clicked(determinant[4:])
            case _:
                raise 'Wrong determination of task/theory'
        

    def theory_clicked(self, theory):
        pass
    

    def task_clicked(self, task):
        pass


    def clear_Content(self):
        self.__delete_items_of_layout(self.content)



    def __delete_items_of_layout(self, layout) -> None:
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.__delete_items_of_layout(item.layout())
    


class ContentBlock(QWidget):
    def __init__(self) -> None:
        super().__init__()
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
    


class ContentTheme(QWidget):
    def __init__(self) -> None:
        super().__init__()
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
    


class ContentTheory(QWidget):
    def __init__(self) -> None:
        super().__init__()
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
    


class ContentTask(QWidget):
    def __init__(self) -> None:
        super().__init__()
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

