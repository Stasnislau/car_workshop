from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QRect, Qt
from .employeeView import EmployeeView
from .ticketView import TicketView
from .documentView import DocumentView


class MainView(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.employeeNavigationButton = QPushButton(self)
        self.employeeNavigationButton.setGeometry(QRect(100, 250, 500, 500))
        self.employeeNavigationButton.setIcon(
            QIcon("assets/employee_icon.jpg"))
        self.employeeNavigationButton.setIconSize(
            self.employeeNavigationButton.size())
        self.employeeNavigationButton.clicked.connect(self.showEmployeeView)

        self.ticketNavigationButton = QPushButton(self)
        self.ticketNavigationButton.setGeometry(QRect(700, 250, 500, 500))
        self.ticketNavigationButton.setIcon(QIcon("assets/ticket_icon.jpg"))
        self.ticketNavigationButton.setIconSize(
            self.ticketNavigationButton.size())
        self.ticketNavigationButton.clicked.connect(self.showTicketView)

        self.documentNavigationButton = QPushButton(self)
        self.documentNavigationButton.setGeometry(QRect(1300, 250, 500, 500))
        self.documentNavigationButton.setIcon(
            QIcon("assets/documents_icon.jpg"))
        self.documentNavigationButton.setIconSize(
            self.documentNavigationButton.size())
        self.documentNavigationButton.clicked.connect(self.showDocumentView)

        self.employeeLabel = QLabel("Employee management", self)
        self.employeeLabel.setGeometry(QRect(100, 750, 500, 50))
        self.employeeLabel.setAlignment(Qt.AlignCenter)
        self.employeeLabel.setStyleSheet("font-size: 20px;")

        self.ticketLabel = QLabel("Ticket management", self)
        self.ticketLabel.setGeometry(QRect(700, 750, 500, 50))
        self.ticketLabel.setAlignment(Qt.AlignCenter)
        self.ticketLabel.setStyleSheet("font-size: 20px;")

        self.documentLabel = QLabel("Document management", self)
        self.documentLabel.setGeometry(QRect(1300, 750, 500, 50))
        self.documentLabel.setAlignment(Qt.AlignCenter)
        self.documentLabel.setStyleSheet("font-size: 20px;")

    def showEmployeeView(self):
        self.parent.changeView("employee")
        pass

    def showTicketView(self):
        self.parent.changeView("ticket")
        pass

    def showDocumentView(self):
        self.parent.changeView("document")
        pass
