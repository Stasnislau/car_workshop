from PyQt5.QtWidgets import QMainWindow, QLabel, QMenuBar, QMenu, QAction
from PyQt5.QtCore import Qt
from .employee_dialog import EmployeeDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Car Workshop")

        label = QLabel("Welcome to the Car Workshop Application!")
        label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(label)

        # Create menu bar
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        # Create menus
        employee_menu = QMenu("Employee Management", self)
        ticket_menu = QMenu("Ticket Management", self)
        document_menu = QMenu("Document Handling", self)

        # Add menus to the menu bar
        menu_bar.addMenu(employee_menu)
        menu_bar.addMenu(ticket_menu)
        menu_bar.addMenu(document_menu)

        # Create menu actions (placeholder functions)
        def employee_management_placeholder():
            dialog = EmployeeDialog(self)
            dialog.exec_()

        def ticket_management_placeholder():
            print("Ticket Management selected")

        def document_handling_placeholder():
            print("Document Handling selected")

        # Add actions to the menus
        employee_menu.addAction(
            QAction("Manage Employees", self, triggered=employee_management_placeholder))
        ticket_menu.addAction(
            QAction("Manage Tickets", self, triggered=ticket_management_placeholder))
        document_menu.addAction(
            QAction("Manage Documents", self, triggered=document_handling_placeholder))
