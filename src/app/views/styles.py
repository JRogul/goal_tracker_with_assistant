styles_main_window = """
            QMainWindow {
                background-color: #F2F3F4;
            }
            QLabel {
                font-size: 16px;
                color: #333;
            }
            QPushButton {
                background-color: #007BFF;
                border-style: none;
                padding: 10px;
                color: white;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QLineEdit {
                padding: 5px;
                border: 1px solid #CCC;
                
            }
            QLineEdit {
                border: 1px solid #CCC;
                padding: 5px;
            }
            QListWidget {
                background-color: #f0f0f0;
                border: 1px solid #dcdcdc;
                show-decoration-selected: 1; /* highlight items when selected */
            }
            QListWidget::item {
                padding: 5px;
            }

            QListWidget::item:selected {
                background-color: #0056b3
                }
            QVBoxLayout::item:selected {
                background-color: #0056b3
                }
        """