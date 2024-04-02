from PyQt5.QtWidgets import QPushButton, QLabel, QVBoxLayout, QWidget, QMainWindow, QComboBox, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
from ..components.employee.createEmployeeDialog import CreateEmployeeDialog
from ..services.employeeService import EmployeeService
from ..components.employee.editEmployeeDialog import EditEmployeeDialog
from ..components.employee.deleteEmployeeDialog import DeleteEmployeeDialog


class EmployeeView(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.currentEmployee = None

        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(50, 50, 50, 50)  # Add some margin

        titleLabel = QLabel("Employee Management", self)
        titleLabel.setStyleSheet(
            "font-size: 24px; font-weight: bold; color: #333;")
        titleLabel.setFixedSize(300, 30)
        mainLayout.addWidget(titleLabel, alignment=Qt.AlignCenter)

        # Middle part with left and right layouts
        middleWidget = QWidget()
        middleLayout = QHBoxLayout(middleWidget)

        # Left part with buttons and dropdown
        leftWidget = QWidget()
        leftLayout = QVBoxLayout(leftWidget)
        self.employeeDropdown = QComboBox(leftWidget)
        self.employeeDropdown.setStyleSheet(
            "font-size: 14px; background-color: #fff; border: 1px solid #ccc;")

        self.employeeDropdown.setFixedSize(200, 50)
        leftLayout.addWidget(self.employeeDropdown, alignment=Qt.AlignCenter)
        self.employeeDropdown.currentIndexChanged.connect(
            self.updateCurrentEmployee)

        optionsLayout = QVBoxLayout()
        leftLayout.addLayout(optionsLayout)

        options = ["Add Employee", "Edit Employee", "Delete Employee"]
        for option in options:
            button = QPushButton(option, leftWidget)
            button.setStyleSheet(
                "font-size: 14px; background-color: #007bff; color: #fff; border: none;")
            button.clicked.connect(self.handleOptionClick)
            button.setFixedSize(200, 50)
            optionsLayout.addWidget(button, alignment=Qt.AlignCenter)

        middleLayout.addWidget(leftWidget)

        # Right part with employee information
        rightWidget = QWidget()
        rightLayout = QVBoxLayout(rightWidget)

        informationLabel = QLabel("Employee Information", rightWidget)
        informationLabel.setStyleSheet(
            "font-size: 18px; font-weight: bold; color: #333;")
        informationLabel.setFixedSize(210, 50)
        rightLayout.addWidget(informationLabel, alignment=Qt.AlignCenter)

        self.informationLabel = QLabel("No employee selected", rightWidget)
        self.informationLabel.setStyleSheet("font-size: 14px; color: #666;")
        rightLayout.addWidget(self.informationLabel, alignment=Qt.AlignCenter)

        middleLayout.addWidget(rightWidget)
        mainLayout.addWidget(middleWidget)

        # Return to Main Menu button
        returnButton = QPushButton("Return to Main Menu", self)
        returnButton.clicked.connect(self.returnToMainView)
        returnButton.setStyleSheet(
            "font-size: 14px; background-color: #6c757d; color: #fff; border: none;")
        returnButton.setFixedSize(200, 50)
        mainLayout.addWidget(returnButton, alignment=Qt.AlignCenter)

        # Fetch employees
        self.fetchEmployees()

    def handleOptionClick(self):
        senderButton = self.sender()
        if senderButton:
            optionText = senderButton.text()
            if optionText == "Add Employee":
                self.addEmployee()
            elif optionText == "Edit Employee":
                self.editEmployee()
            elif optionText == "Delete Employee":
                self.deleteEmployee()

    def updateCurrentEmployee(self):
        index = self.employeeDropdown.currentIndex()
        if index != -1:
            self.currentEmployee = self.employees[index]
            if self.currentEmployee:
                info_text = f"Name: {self.currentEmployee.name}\nHourly Rate: {self.currentEmployee.hourlyRate}"
            else:
                info_text = "No employee selected"
        else:
            info_text = "No employee selected"

        self.informationLabel.setText(info_text)

    def fetchEmployees(self):
        self.employees = EmployeeService().getEmployees()
        self.employeeDropdown.clear()
        for employee in self.employees:
            self.employeeDropdown.addItem(employee.name)

    def returnToMainView(self):
        parentWidget = self.parent
        if isinstance(parentWidget, QMainWindow):
            parentWidget.changeView("main")

    def addEmployee(self):
        CreateEmployeeDialog(self).show()

    def editEmployee(self):
        if self.currentEmployee:
            edit_dialog = EditEmployeeDialog(self, self.currentEmployee)
            edit_dialog.exec_()
        else:
            print("No employee selected")

    def deleteEmployee(self):
        if self.currentEmployee:
            dialog = DeleteEmployeeDialog(self.currentEmployee.name, self)
            if dialog.exec_():
                # User clicked "Yes"
                success, message = EmployeeService().deleteEmployee(self.currentEmployee.id)
                if success:
                    QMessageBox.information(
                        self, "Success", "Employee deleted successfully.")
                    self.fetchEmployees()  # Update employee list
                else:
                    QMessageBox.warning(self, "Error", message)
            else:
                print("Deletion canceled by user")
        else:
            print("No employee selected")
