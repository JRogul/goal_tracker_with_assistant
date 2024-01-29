from PyQt5.QtWidgets import QCalendarWidget, QDateTimeEdit, QMainWindow, \
    QDateEdit, QLabel, QVBoxLayout, QWidget, QListWidget, QLineEdit, QPushButton, QDialog, QListWidgetItem
from PyQt5.QtGui import QFont
from app.controllers.goal_controller import GoalController
from app.ui.styles import styles_main_window
from PyQt5.QtCore import Qt, pyqtSignal, QDateTime
from app.database.database_connection import *
from datetime import datetime


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

        self.create_task_list()


        self.goal_list.itemClicked.connect(self.on_item_clicked)
        
        layout.addWidget(self.goal_list)

        self.title_input = QLineEdit() 
        self.title_input.setText('Write your goal')
        layout.addWidget(self.title_input)

        self.description_input = QLineEdit()
        self.description_input.setText('Add description')  # Input for goal description
        layout.addWidget(self.description_input)

        add_button = QPushButton('Create Goal')
        add_button.clicked.connect(self.add_goal)
        layout.addWidget(add_button)

    def create_task_list(self):
        self.goal_list = QListWidget()
        data = get_task_list_from_database()

        if len(data) != 0:
            for count, row in enumerate(data):
                item = QListWidgetItem(f"{row[1]}")
                ID_task, title, description, start_date, end_date = zip(select_task_from_database(count)[0])
                item.setData(Qt.UserRole, ID_task)
                item.setData(Qt.UserRole + 1, title)
                item.setData(Qt.UserRole + 2, description)
                self.goal_list.addItem(item)

    def on_item_clicked(self, item: QListWidgetItem):
        print(item)
        self.detail_window = DetailWindow(item)
        self.detail_window.window_closed.connect(self.onDetailWindowClosed)
        self.detail_window.show()  
        
    def onDetailWindowClosed(self, ID_task, delete_task):
        print('onDetaiLWindow')
        if delete_task:
            self.goal_list.takeItem(ID_task)

    def add_goal(self):
        self.detail_window = AddWGoalWindow()
        self.detail_window.window_closed.connect(self.onAddGoalWindowClosed)
        
        self.detail_window.show()

    def onAddGoalWindowClosed(self, title, description, start_date, end_date): # TODO
        ID_task = get_number_of_tasks_from_database()
        item = QListWidgetItem(title)
        item.setData(Qt.UserRole, ID_task)
        item.setData(Qt.UserRole + 1, title)
        item.setData(Qt.UserRole + 2, description)
        item.setData(Qt.UserRole + 3, start_date)
        item.setData(Qt.UserRole + 4, end_date)
        
        self.goal_list.addItem(item)
        self.create_task_list()

class AddWGoalWindow(QWidget):
    window_closed = pyqtSignal(str, str, str, str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"Add Goal")
        self.setGeometry(250, 250, 800, 800)
        self.goal_controller = GoalController()
        layout = QVBoxLayout()
        self.item = QListWidgetItem()
        self.title_input = QLineEdit() 
        self.title_input.setText('Write your goal')
        layout.addWidget(self.title_input)

        self.description_input = QLineEdit()
        self.description_input.setText('Add description') 
        layout.addWidget(self.description_input)

        self.start_date_button = QPushButton('Set start date')
        self.start_date_button.clicked.connect(lambda: self.select_date('start'))
        self.start_date_button.setFixedWidth(100) 
        layout.addWidget(self.start_date_button)

        self.end_date_button = QPushButton('Set end date')
        self.end_date_button.clicked.connect(lambda: self.select_date('end'))
        self.end_date_button.setFixedWidth(100) 
        layout.addWidget(self.end_date_button)

        self.start_date = QDateTimeEdit(self)
        self.start_date.setDisplayFormat("yyyy-MM-dd hh:mm:ss")
        
        layout.addWidget(self.start_date)

        self.end_date = QDateTimeEdit(self)
        self.end_date.setDisplayFormat("yyyy-MM-dd hh:mm:ss")
        layout.addWidget(self.end_date)

        self.calendar = QCalendarWidget(self)
        self.calendar.setFixedSize(330, 330)
        self.calendar.hide()  
        self.calendar.clicked.connect(self.date_clicked)
        layout.addWidget(self.calendar)

        self.toggle_calendar_button = QPushButton("Toggle Calendar", self)
        self.toggle_calendar_button.clicked.connect(self.toggle_calendar)
        layout.addWidget(self.toggle_calendar_button)

        add_button = QPushButton('Add Goal')
        add_button.clicked.connect(self.add_goal)
        layout.addWidget(add_button)
        layout.addStretch()

        self.setLayout(layout)

    def select_date(self, date_type):
        self.active_date_edit = date_type
        self.calendar.setVisible(not self.calendar.isVisible())
        
    def date_clicked(self, qDate):
        
        if self.active_date_edit == 'start':
            self.start_date.setDateTime(QDateTime.currentDateTime())
            self.start_date = self.start_date.dateTime().toString("yyyy-MM-dd hh:mm:ss")
        if self.active_date_edit == 'end':
            self.end_date.setDateTime(QDateTime.currentDateTime())
            self.end_date = self.end_date.dateTime().toString("yyyy-MM-dd hh:mm:ss")
        self.calendar.setVisible(not self.calendar.isVisible())
            
    def closeEvent(self, event):
        self.window_closed.emit(self.title_input.text(), 
                                self.description_input.text(),
                                self.start_date, self.end_date)
        
        super().closeEvent(event)

    def add_goal(self):
        title = self.title_input.text()
        description = self.description_input.text()
        
        if len(title) != 0 and len(description) != 0:
            ID_task = get_number_of_tasks_from_database()
            insert_task_to_database(ID_task, title, description, self.start_date, 
                                    self.end_date)
            self.goal_controller.add_goal(title, description)
            item = QListWidgetItem(f"{title}")
            item.setData(Qt.UserRole, ID_task)
            item.setData(Qt.UserRole + 1, title)
            item.setData(Qt.UserRole + 2, description)

            item.setData(Qt.UserRole + 3, self.start_date)
            item.setData(Qt.UserRole + 4, self.end_date)
            self.close()

    def toggle_calendar(self):
        # Toggle the visibility of the calendar
        self.calendar.setVisible(not self.calendar.isVisible())
        
    def open_calendar(self):
        self.calendar_window = CalendarWindow()
        self.calendar_window.show()


class DetailWindow(QWidget):

    window_closed = pyqtSignal(int, bool)

    def __init__(self, item):
        
        super().__init__()
        self.setWindowTitle(f"{item.text()}")
        self.setGeometry(250, 250, 800, 800)
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

        self.calendar = QCalendarWidget(self)
        self.calendar.setFixedSize(330, 330)
        self.calendar.hide()  # Initially hide the calendar
        layout.addWidget(self.calendar)

        # Calendar toggle button
        self.toggle_calendar_button = QPushButton("Toggle Calendar", self)
        self.toggle_calendar_button.clicked.connect(self.toggle_calendar)
        layout.addWidget(self.toggle_calendar_button)

        self.delete_button = QPushButton("Delete Item")
        self.delete_button.clicked.connect(self.delete_item)
        layout.addWidget(self.delete_button)

        self.setLayout(layout)

    def toggle_calendar(self):
        # Toggle the visibility of the calendar
        self.calendar.setVisible(not self.calendar.isVisible())

    def delete_item(self):
        delete_task_from_database(self.item.data(Qt.UserRole))
        self.delete_task = True
        self.close()

    def closeEvent(self, event):
        delete_task = self.delete_task
        self.window_closed.emit(self.item.data(Qt.UserRole), delete_task)
        self.is_closed = True
        
        super().closeEvent(event)

    # def open_calendar(self):
    #     self.calendar_window = CalendarWindow()
    #     self.calendar_window.show()

# class CalendarWindow(QWidget):
#     def __init__(self):
#         super().__init__()

#         layout = QVBoxLayout(self)
        
#         self.calendar = QCalendarWidget(self)
#         self.calendar.clicked.connect(self.onDateClicked)
#         layout.addWidget(self.calendar)
#         print('aaaa')
#         self.setGeometry(100, 100, 100, 100)
#         self.setWindowTitle('Calendar')
#         self.show()

#     def onDateClicked(self, date):
#         print(date)
#         formatted_date = date.toString("yyyy-MM-dd")
#         self.label.setText(f"Selected Date: {formatted_date}")
#         print(self.label)