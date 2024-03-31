from PyQt5.QtWidgets import QPushButton, QLabel, QVBoxLayout, QWidget, QMainWindow
from PyQt5.QtCore import QRect, Qt


class EmployeeView(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        layout = QVBoxLayout(self)

        titleLabel = QLabel("Employee Management", self)
        titleLabel.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(titleLabel, alignment=Qt.AlignCenter)

        optionsLayout = QVBoxLayout()
        layout.addLayout(optionsLayout)

        options = ["Add Employee", "Search Employees",
                   "Edit Employee", "Delete Employee"]
        for option in options:
            button = QPushButton(option, self)
            button.clicked.connect(self.handleOptionClick)
            optionsLayout.addWidget(button)

        returnButton = QPushButton("Return to Main Menu", self)
        returnButton.clicked.connect(self.returnToMainView)
        layout.addWidget(returnButton, alignment=Qt.AlignCenter)

    def handleOptionClick(self):
        senderButton = self.sender()
        if senderButton:
            optionText = senderButton.text()
            if optionText == "Add Employee":
                self.addEmployee()
            elif optionText == "Search Employees":
                self.searchEmployees()
            elif optionText == "Edit Employee":
                self.editEmployee()
            elif optionText == "Delete Employee":
                self.deleteEmployee()

    def returnToMainView(self):
        parentWidget = self.parent
        if isinstance(parentWidget, QMainWindow):
            parentWidget.changeView("main")

    def addEmployee(self):
        # Functionality to add an employee
        pass

    def searchEmployees(self):
        # Functionality to search for employees
        pass

    def editEmployee(self):
        # Functionality to edit an employee
        pass

    def deleteEmployee(self):
        # Functionality to delete an employee
        pass
