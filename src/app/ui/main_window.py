from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QListWidget, QLineEdit, QPushButton, QDialog, QListWidgetItem
from PyQt5.QtGui import QFont
from app.controllers.goal_controller import GoalController
from app.ui.styles import styles_main_window
from PyQt5.QtCore import Qt, pyqtSignal
from app.database.database_connection import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Goal Tracker')
        self.setStyleSheet(styles_main_window)
        self.goal_controller = GoalController()
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()
        self.central_widget.setLayout(layout)

        self.goal_list = QListWidget()
        data = get_task_list_from_database()
        
        for count, row in enumerate(data):
            item = QListWidgetItem(f"{row[1]}")
            ID_task, title, description = select_task_from_database(count)[0]
            item.setData(Qt.UserRole, ID_task)
            item.setData(Qt.UserRole + 1, title)
            item.setData(Qt.UserRole + 2, description)
            self.goal_list.addItem(item)

        self.goal_list.itemClicked.connect(self.on_item_clicked)
        
        layout.addWidget(self.goal_list)

        self.title_input = QLineEdit() 
        self.title_input.setText('Write your goal')
        layout.addWidget(self.title_input)

        self.description_input = QLineEdit()
        self.description_input.setText('Add addictional text')  # Input for goal description
        layout.addWidget(self.description_input)

        add_button = QPushButton('Add Goal')
        add_button.clicked.connect(self.add_goal)
        layout.addWidget(add_button)

    def on_item_clicked(self, item: QListWidgetItem):
        print(item)
        self.detail_window = DetailWindow(item)
        self.detail_window.window_closed.connect(self.onDetailWindowClosed)
        self.detail_window.show()  
        
    def onDetailWindowClosed(self, ID_task, delete_task):
        print('onDetaiLWindow')
        if delete_task:
            self.goal_list.takeItem(ID_task)

       # TODO fix refreshing after deleting

    def add_goal(self):
        
        title = self.title_input.text()
        description = self.description_input.text()
        print(title, description)
        print(len(title))
        if len(title) != 0 and len(description) != 0:
            insert_task_to_database(title, description)
            ID_task = len(self.goal_list)
            self.goal_controller.add_goal(title, description)
            item = QListWidgetItem(f"{title}")
            item.setData(Qt.UserRole, ID_task)
            item.setData(Qt.UserRole + 1, title)
            item.setData(Qt.UserRole + 2, description)
            self.goal_list.addItem(item)
        self.title_input.clear()
        self.description_input.clear()
        

class DetailWindow(QWidget):

    window_closed = pyqtSignal(int, bool)

    def __init__(self, item):

        

        super().__init__()
        self.setWindowTitle(f"{item.text()}")
        self.setGeometry(500, 500, 500, 500)
        self.item = item
        self.delete_task = False

        layout = QVBoxLayout()
        item_id = item.data(Qt.UserRole)
        additional_data1 = item.data(Qt.UserRole + 1)
        additional_data2 = item.data(Qt.UserRole + 2)

        # Creating formatted text for the label
        label_text = (f"Item ID: {item_id}<br>"
                      f"Your task: {additional_data1}<br>"
                      f"Description of the task: {additional_data2}")

        self.label = QLabel(label_text)
        self.label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.label.setStyleSheet("QLabel { font-size: 14px; }")  # Optional styling
        layout.addWidget(self.label)

        self.delete_button = QPushButton("Delete Item")
        self.delete_button.clicked.connect(self.delete_item)
        layout.addWidget(self.delete_button)

        self.setLayout(layout)

    def delete_item(self):
        delete_task_from_database(self.item.data(Qt.UserRole))
        self.delete_task = True

    def closeEvent(self, event):
        delete_task = self.delete_task
        self.window_closed.emit(self.item.data(Qt.UserRole), delete_task)
        self.is_closed = True
        
        super().closeEvent(event)
       