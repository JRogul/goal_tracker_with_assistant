from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QListWidget, QLineEdit, QPushButton, QDialog, QListWidgetItem
from app.controllers.goal_controller import GoalController
from app.views.styles import styles_main_window
from app.models.database_connection import *

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

        self.goal_list = QListWidget()  # List to display goals
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
        detail_window = DetailWindow(item.text(), self)
        detail_window.exec_()  

    def add_goal(self):
        title = self.title_input.text()
        description = self.description_input.text()
        ID_task = len(self.goal_list)
        print(ID_task)
        self.goal_controller.add_goal(title, description)
        self.goal_list.addItem(f"{title}")
        self.title_input.clear()
        self.description_input.clear()
        insert_task(title, description)


class DetailWindow(QDialog):
    def __init__(self, item_text, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"{item_text}")
        self.setGeometry(500, 500, 500, 500)
        layout = QVBoxLayout()
        self.label = QLabel(item_text)
        layout.addWidget(self.label)
        
        self.setLayout(layout)