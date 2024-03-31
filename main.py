import sys
from PyQt5.QtWidgets import QApplication

from app.mainWindow import MainWindow


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.setStyleSheet("background-color: #f0f0f0;")
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
