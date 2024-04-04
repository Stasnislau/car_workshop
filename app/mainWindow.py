from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QRect, Qt
from .views.employeeView import EmployeeView
from .views.mainView import MainView
from .views.documentView import DocumentView
from .views.ticketView import TicketView


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.changeView("main")

        self.setWindowTitle("Car Workshop")
        self.showMaximized()

    def changeView(self, view):
        currentView = self.centralWidget()
        if currentView:
            currentView.deleteLater()
        viewToBeSet = None
        if view == "employee":
            viewToBeSet = EmployeeView(self)
        elif view == "main":
            viewToBeSet = MainView(self)
        elif view == "ticket":
            viewToBeSet = TicketView(self)
        elif view == "document":
            viewToBeSet = DocumentView(self)
        else:
            return
        self.setCentralWidget(viewToBeSet)
        self.show()
