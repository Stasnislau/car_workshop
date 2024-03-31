from PyQt5.QtWidgets import QPushButton, QLabel, QVBoxLayout, QWidget, QMainWindow

class EmployeeView(QWidget):  # Change base class to QWidget
    def __init__(self, parent=None):  # Add parent parameter
        super().__init__(parent)

        layout = QVBoxLayout(self)

        label = QLabel("Welcome to the Employee Management System", self)
        layout.addWidget(label)

        employeeButton = QPushButton("Add Employee", self)
        employeeButton.clicked.connect(self.addEmployee)
        layout.addWidget(employeeButton)

        searchButton = QPushButton("Search Employees", self)
        searchButton.clicked.connect(self.searchEmployees)
        layout.addWidget(searchButton)

        editButton = QPushButton("Edit Employee", self)
        editButton.clicked.connect(self.editEmployee)
        layout.addWidget(editButton)

        deleteButton = QPushButton("Delete Employee", self)
        deleteButton.clicked.connect(self.deleteEmployee)
        layout.addWidget(deleteButton)

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