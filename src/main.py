import sys
from PyQt5.QtWidgets import QApplication
from app.views.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    main_window = MainWindow()
    main_window.setGeometry(500, 500, 500, 500)
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()