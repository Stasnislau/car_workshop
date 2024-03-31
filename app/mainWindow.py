from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QRect, Qt
from .views.employeeView import EmployeeView
from .views.mainView import MainView


class MainWindow(QMainWindow):
    current_view = None

    def __init__(self):
        super().__init__()
        self.employeeView = EmployeeView()
        self.mainView = MainView(self)
        self.changeView(self.mainView)

        self.setWindowTitle("Car Workshop")
        self.setGeometry(0, 0, 1920, 1080)
        screenGeometry = QApplication.desktop().screenGeometry()
        windowGeometry = self.geometry()
        windowCenterPoint = windowGeometry.center()
        screenCenterPoint = screenGeometry.center()
        windowCenterPoint.setX(
            screenCenterPoint.x() - round(windowGeometry.width() / 2))
        windowCenterPoint.setY(
            screenCenterPoint.y() - round(windowGeometry.height() / 2))
        self.move(windowCenterPoint)

    def changeView(self, view):
        self.setCentralWidget(view)
        self.show()
