styles_main_window = """
            QMainWindow {
    background-color: #F0F0F0; /* Light gray background */
}

/* Style for labels */
QLabel {
    font-family: Arial, sans-serif;
    font-size: 14px;
    color: #333333; /* Dark gray text */
}

/* Style for line edits */
QLineEdit {
    font-family: Arial, sans-serif;
    font-size: 12px;
    padding: 5px;
    border: 1px solid #CCCCCC; /* Light gray border */
    border-radius: 4px;
}

/* Style for push buttons */
QPushButton {
    font-family: Arial, sans-serif;
    font-size: 12px;
    color: white;
    background-color: #007BFF; /* Blue background */
    border-style: none;
    padding: 10px;
    border-radius: 4px;
}

QPushButton:hover {
    background-color: #0056b3; /* Darker blue on hover */
}

/* Style for list widgets */
QListWidget {
    font-family: Arial, sans-serif;
    font-size: 12px;
    background-color: #FFFFFF; /* White background */
    border: 1px solid #CCCCCC; /* Light gray border */
    border-radius: 4px;
    show-decoration-selected: 1; /* Highlight items when selected */
}

QListWidget::item {
    padding: 5px;
}

QListWidget::item:selected {
    background-color: #0056b3; /* Dark blue when selected */
    color: white;
}

/* Dialog styles (if you use QDialog) */
QDialog {
    background-color: #FFFFFF; /* White background for dialogs */
}
        """