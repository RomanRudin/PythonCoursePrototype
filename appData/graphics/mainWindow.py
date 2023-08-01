from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QPushButton, QLabel, QTextEdit
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
        self.theme_list.addItems(self.controller.get_themes(block))
        self.__clear_content()
        self.content.addWidget(ContentBlock(self.controller.set_block(block)))



    def theme_clicked(self):
        theme = self.theme_list.selectedItems()[0].text() 
        self.task_and_theory_list.clear()
        self.task_and_theory_list.addItems(self.controller.get_theories_and_tasks(theme))
        self.__clear_content()
        try:
            self.content.addWidget(ContentTheme(self.controller.set_theme(theme)))
        except Exception as e:
            print(e)
            raise ''


    def theory_and_task_determinant(self):
        determinant = self.task_and_theory_list.selectedItems()[0].text() 
        self.__clear_content()
        match determinant[:4]:
            case '[Th]':
                self.theory_clicked(determinant[4:])
            case '[Ex]':
                self.task_clicked(determinant[4:])
            case _:
                raise 'Wrong determination of task/theory'
        

    def theory_clicked(self, theory):
        self.content.addWidget(ContentTheory(self.controller.set_theory(theory)))


    def task_clicked(self, task):
        self.content.addWidget(ContentTask(self.controller.set_task(task)))


    def __clear_content(self):
        while self.content.count():
            widget = self.content.takeAt(0).widget()
            widget.setParent(None)
            widget.deleteLater()
    


class ContentBlock(QWidget):
    def __init__(self, args) -> None:
        super().__init__()
        name, description, mark = args

        if mark is None:
            mark = ''

        main_layout = QVBoxLayout()
        info_layout = QHBoxLayout()

        info_layout.addWidget(QLabel(str(name)))
        info_layout.addWidget(QLabel(str(mark)))

        main_layout.addLayout(info_layout)
        main_layout.addWidget(QLabel(str(description)))

        self.setLayout(main_layout)
    


class ContentTheme(QWidget):
    def __init__(self, args) -> None:
        super().__init__()
        name, id, relation, description, mark = args

        if mark is None:
            mark = ''

        main_layout = QVBoxLayout()
        info_layout = QHBoxLayout()

        info_layout.addWidget(QLabel(str(name)))
        info_layout.addWidget(QLabel(str(id)))
        info_layout.addWidget(QLabel(str(mark)))

        main_layout.addLayout(info_layout)
        main_layout.addWidget(QLabel(str(description)))

        self.setLayout(main_layout)
    


class ContentTheory(QWidget):
    def __init__(self, args) -> None:
        super().__init__()
        name, id, relation, text = args

        main_layout = QVBoxLayout()
        info_layout = QHBoxLayout()

        info_layout.addWidget(QLabel(str(name)))
        info_layout.addWidget(QLabel(str(id)))

        main_layout.addLayout(info_layout)
        main_layout.addWidget(QLabel(str(text)))

        self.setLayout(main_layout)
    


class ContentTask(QWidget):
    def __init__(self, args) -> None:
        super().__init__()
        name, id, relation, text, inputFormat, outputFormat, mark = args

        if mark is None:
            mark = ''

        main_layout = QVBoxLayout()
        text_tests_layout = QHBoxLayout()
        info_layout = QHBoxLayout()
        text_layout = QHBoxLayout()
        input_output_layout = QHBoxLayout()

        self.testsList = QListWidget()
        self.codeEdit = QTextEdit()
        self.checkCode = QPushButton('Check')
        self.checkCode.clicked.connect(self.send_code)

        info_layout.addWidget(QLabel(str(name)))
        info_layout.addWidget(QLabel(str(id)))
        info_layout.addWidget(QLabel(str(mark)))

        input_output_layout.addWidget(QLabel(str(inputFormat)))
        input_output_layout.addWidget(QLabel(str(outputFormat)))

        text_layout.addWidget(QLabel(str(text)))
        text_layout.addLayout(input_output_layout)

        text_tests_layout.addLayout(text_layout)
        text_tests_layout.addWidget(self.testsList)

        main_layout.addLayout(info_layout)
        main_layout.addLayout(text_tests_layout)
        main_layout.addWidget(self.codeEdit)
        main_layout.addWidget(self.checkCode)

        self.setLayout(main_layout)


    def send_code(self):
        pass

