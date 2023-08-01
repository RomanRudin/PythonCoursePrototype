from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QListWidget, \
    QPushButton, QLabel, QLineEdit, QTextEdit
from ..db_control.administrationController import AdminController, AdminInfoGetter, \
    TABLES_DEPENDENCY, TABLES_ORDER


class adminPanel(QWidget):
    def __init__(self, db_name):
        super().__init__()
        self.controller = AdminController(db_name)
        mainLayout = QVBoxLayout()

        self.navPanel = NavPanel(db_name)
        mainLayout.addWidget(self.navPanel)

        dangerZoneLayout = QHBoxLayout()
        self.destroyButton = QPushButton("DESTROY")
        self.destroyButton.setDisabled(True)
        self.destroyButton.clicked.connect(self.controller.destroy)
        dangerZoneLayout.addWidget(self.destroyButton)
        self.backupButton = QPushButton('BACKUP')
        self.backupButton.clicked.connect(self.controller.backup)
        dangerZoneLayout.addWidget(self.backupButton)
        self.createButton = QPushButton('RECREATE')
        self.destroyButton.setDisabled(True)
        self.createButton.clicked.connect(self.controller.create)
        dangerZoneLayout.addWidget(self.createButton)
        mainLayout.addLayout(dangerZoneLayout)

        self.workspace = Workscpace(db_name)
        mainLayout.addWidget(self.workspace)

        self.navPanel._NavPanel__create_link(self.workspace)
        self.workspace._Workscpace__create_link(self.navPanel)

        self.setLayout(mainLayout)
    



class NavPanel(QWidget):
    def __init__(self, db_name) -> None:
        super().__init__()
        mainLayout = QHBoxLayout()
        self.tables = AdminInfoGetter(db_name).table_names_getting()
        self.navBars = []

        for table in self.tables:
            self.navBars.append(NavPart(db_name, table, self))
            mainLayout.addWidget(self.navBars[-1])

        self.navBars[0].update('')

        self.setLayout(mainLayout)


    def __create_link(self, object):
        self.panel = object


    def update_deleted(self, entry):
        index = TABLES_ORDER.index(entry)
        currentTableList = self.navBars[index].list
        selectedTableItem = currentTableList.selectedItems()[0]
        if not selectedTableItem:
            self.clear_following(preentry for preentry in TABLES_DEPENDENCY \
                if entry in TABLES_DEPENDENCY[preentry])
            return
        currentTableList.takeItem(currentTableList.row(selectedTableItem))
        self.clear_following(entry)


    def update(self, entry, id):
        index = TABLES_ORDER.index(entry)
        currentTable = self.navBars[index]
        currentTable.clear()
        currentTable.update(id)


    def update_next(self, entry, id):
        if TABLES_DEPENDENCY[entry] != '':
            for table in TABLES_DEPENDENCY[entry]:
                index = TABLES_ORDER.index(table)
                self.navBars[index].update(id)


    def clear_following(self, entry):
        if TABLES_DEPENDENCY[entry] != '':
            for table in TABLES_DEPENDENCY[entry]:
                index = TABLES_ORDER.index(table)
                self.navBars[index].clear()
                self.clear_following(table)




class NavPart(QWidget):
    def __init__(self, db_name, table, parent) -> None:
        super().__init__()
        self.navPanel = parent 
        self.table = table
        self.infoLoader = AdminInfoGetter(db_name)

        mainLayout = QVBoxLayout()

        label = QLabel(self.table)
        mainLayout.addWidget(label)
        
        self.list = QListWidget()
        mainLayout.addWidget(self.list)
        self.list.itemClicked.connect(self.choose)

        self.button = QPushButton('+ Add')
        self.button.setDisabled(True)
        mainLayout.addWidget(self.button)
        self.button.clicked.connect(self.add)

        self.setLayout(mainLayout)


    def clear(self):
        self.list.clear()
        self.button.setDisabled(True)


    def choose(self):
        rowID = self.list.selectedItems()[0].text() 
        self.navPanel.clear_following(self.table)
        self.navPanel.update_next(self.table, rowID)
        self.navPanel.panel.open_row(self.table, rowID)


    def add(self): #TODO
        self.navPanel.panel.clear()
        self.navPanel.panel.construct(self.table)
        self.navPanel.clear_following(self.table)


    def update(self, parentID):
        items = self.infoLoader.primary_key_getting(self.table, parentID)
        if len(items) > 0:
            self.list.addItems(items)
            self.button.setDisabled(False)
        else:
            self.clear()
            self.button.setDisabled(False)




class Workscpace(QWidget):
    def __init__(self, db_name):
        super().__init__()
        self.controller = AdminController(db_name)
        self.construction = {}
        self.name = ''

        self.mainLayout = QVBoxLayout()

        self.content = QHBoxLayout()
        self.mainLayout.addLayout(self.content)

        self.buttonLayout = QHBoxLayout()

        self.saveButton = QPushButton('Save')
        self.saveButton.clicked.connect(self.save_row)
        self.buttonLayout.addWidget(self.saveButton)

        self.deleteButton = QPushButton('Delete')
        self.deleteButton.clicked.connect(self.delete_row)
        self.buttonLayout.addWidget(self.deleteButton)

        self.mainLayout.addLayout(self.buttonLayout)
        self.__disable_buttons_and_clean_info(True)
        self.setLayout(self.mainLayout)


    def __create_link(self, object):
        self.panel = object
    

    def construct(self, table, data=None):
        self.table = table
        self.construction = {}
        match table:
            case 'Block':
                extraLayout = QVBoxLayout()

                self.name = QLineEdit()
                self.description = TextEdit()

                extraLayout.addWidget(self.name)
                extraLayout.addWidget(self.description)

                if not data is None:
                    self.name.setText(str(data[0]))
                    self.description.setText(str(data[1]))

                self.construction = {
                    'blockName': self.name,
                    'description': self.description,
                }
                self.content.addLayout(extraLayout)


            case 'Theme':
                extraLayout = QVBoxLayout()

                self.name = QLineEdit()
                self.id = QLineEdit()
                self.relation = QLineEdit()
                self.relation.setDisabled(True)

                extraLayout.addWidget(self.relation)
                extraLayout.addWidget(self.name)
                extraLayout.addWidget(self.id)

                self.description = TextEdit()

                self.content.addLayout(extraLayout)
                self.content.addWidget(self.description)

                if not data is None:
                    self.id.setText(str(data[0][-2:]))
                    self.name.setText(str(data[1]))
                    self.relation.setText(str(data[2]))
                    self.description.setText(str(data[3]))
                else:
                    self.relation.setText(self.panel.navBars[0].list.selectedItems()[0].text())

                self.construction = {
                    'themeID': self.id,
                    'themeName': self.name,
                    'blockName': self.relation,
                    'description': self.description,
                }


            case 'Theory':
                extraLayout = QVBoxLayout()

                self.name = QLineEdit()
                self.id = QLineEdit()
                self.relation = QLineEdit()
                self.relation.setDisabled(True)

                extraLayout.addWidget(self.relation)
                extraLayout.addWidget(self.name)
                extraLayout.addWidget(self.id)

                self.text = TextEdit()

                self.content.addLayout(extraLayout)
                self.content.addWidget(self.text)

                if not data is None:
                    self.id.setText(str(data[0][-2:]))
                    self.name.setText(str(data[1]))
                    self.relation.setText(str(data[2]))
                    self.text.setText(str(data[3]))
                else:
                    self.relation.setText(self.panel.navBars[1].list.selectedItems()[0].text())

                self.construction = {
                    'theoryName': self.name,
                    'theoryID': self.id,
                    'themeName': self.relation,
                    'theoryText': self.text,
                }


            case 'Task':
                leftLayout = QVBoxLayout()
                rightLayout = QVBoxLayout()

                self.name = QLineEdit()
                self.id = QLineEdit()
                self.relation = QLineEdit()
                self.relation.setDisabled(True)

                leftLayout.addWidget(self.relation)
                leftLayout.addWidget(self.name)
                leftLayout.addWidget(self.id)

                self.description = TextEdit()

                self.input = TextEdit()
                self.output = TextEdit()

                rightLayout.addWidget(self.input)
                rightLayout.addWidget(self.output)

                self.content.addLayout(leftLayout)
                self.content.addWidget(self.description)
                self.content.addLayout(rightLayout)

                if not data is None:
                    self.name.setText(str(data[1]))
                    self.id.setText(str(data[0][-2:]))
                    self.relation.setText(str(data[2]))
                    self.description.setText(str(data[3]))
                    self.input.setText(str(data[4]))
                    self.output.setText(str(data[5]))
                else:
                    self.relation.setText(self.panel.navBars[1].list.selectedItems()[0].text())

                self.construction = {
                    'taskName': self.name,
                    'taskID': self.id,
                    'themeName': self.relation,
                    'description': self.description,
                    'inputFormat': self.input,
                    'outputFormat': self.output,
                }


            case 'Test': #TODOTODOTODOTODOTODOTODOTODOTODOTODOTODOTODOTODOTODO
                pass


            case _:
                raise ValueError("Unexpected construction type (Table doesn't exist)")
        self.__disable_buttons_and_clean_info(False)


    def open_row(self, table, rowID):
        self.clear()
        data = self.controller.show(table, rowID)
        self.construct(table, data)
        self.rowID = rowID
        self.table = table


    def save_row(self):
        if self.rowID == '':
            self.rowID = self.name.text()
        self.controller.change_data(self.table, self.rowID, \
            {key: '"' + value.text() + '"' for key, value in self.construction.items()})
        self.panel.update(self.table, self.rowID)
        self.__disable_buttons_and_clean_info(True)


    def delete_row(self):
        self.controller.delete(self.table, self.rowID)
        self.panel.update_deleted(self.table)
        self.saveButton.setDisabled(True)
        self.deleteButton.setDisabled(True)
        self.clear()
        self.construction = {}
        self.__disable_buttons_and_clean_info(True)


    def clear(self):
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

    def __disable_buttons_and_clean_info(self, arg: bool) -> None:
        self.saveButton.setDisabled(arg)
        self.deleteButton.setDisabled(arg)
        if arg:
            self.rowID = ''
            self.table = ''



class TextEdit(QTextEdit):
    def __init_subclass__(cls) -> None:
        return super().__init_subclass__()
    def text(self) -> str:
        return self.toPlainText()