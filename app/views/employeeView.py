from PyQt5.QtWidgets import QPushButton, QLabel, QVBoxLayout, QWidget, QMainWindow, QComboBox, QHBoxLayout, QMessageBox, QFormLayout, QSizePolicy, QGridLayout
from PyQt5.QtCore import Qt, QSize
from ..components.employee.createEmployeeDialog import CreateEmployeeDialog
from ..services.employeeService import EmployeeService
from ..components.employee.editEmployeeDialog import EditEmployeeDialog
from ..components.employee.deleteEmployeeDialog import DeleteEmployeeDialog
from ..components.schedules.employeeSchedule import EmployeeSchedule


class EmployeeView(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.currentEmployee = None

        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(50, 50, 50, 50)

        titleLabel = QLabel("Employee Management", self)
        titleLabel.setStyleSheet(
            "font-size: 24px; font-weight: bold; color: #333;")
        mainLayout.addWidget(titleLabel, alignment=Qt.AlignCenter)

        # Middle part with left and right layouts
        middleWidget = QWidget()
        middleLayout = QHBoxLayout(middleWidget)

        # Left part with buttons and dropdown
        leftWidget = QWidget()
        leftWidget.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Fixed)
        leftLayout = QFormLayout(leftWidget)
        leftLayout.setContentsMargins(0, 0, 0, 0)
        leftLayout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        leftLayout.setFormAlignment(Qt.AlignCenter)
        leftLayout.setLabelAlignment(Qt.AlignRight)
        self.employeeDropdown = QComboBox(leftWidget)

        self.employeeDropdown.setStyleSheet(
            "font-size: 14px; background-color: #fff; border: 1px solid #ccc;")
        self.employeeDropdown.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Fixed)
        leftLayout.addRow(self.employeeDropdown)
        self.employeeDropdown.currentIndexChanged.connect(
            self.updateCurrentEmployee)

        optionsLayout = QGridLayout()
        leftLayout.addRow(optionsLayout)

        leftLayout.setContentsMargins(0, 0, 0, 0)

        options = ["Add Employee", "Edit Employee", "Delete Employee"]
        for i, option in enumerate(options):
            button = QPushButton(option, leftWidget)
            button.setStyleSheet(
                "font-size: 14px; background-color: #007bff; color: #fff; border: none;")
            button.setFixedSize(QSize(150, 50))
            button.clicked.connect(self.handleOptionClick)
            optionsLayout.addWidget(button, i // 3, i % 3)

        middleLayout.addWidget(leftWidget)

        rightWidget = QWidget()
        rightLayout = QFormLayout(rightWidget)
        rightLayout.setContentsMargins(0, 0, 0, 0)
        rightLayout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        rightLayout.setFormAlignment(Qt.AlignCenter)
        rightLayout.setLabelAlignment(Qt.AlignRight)

        informationLabel = QLabel("Employee Information", rightWidget)
        informationLabel.setStyleSheet(
            "font-size: 18px; font-weight: bold; color: #333;")
        rightLayout.addWidget(informationLabel)

        self.informationLabel = QLabel("No employee selected", rightWidget)
        self.informationLabel.setStyleSheet("font-size: 14px; color: #666;")
        rightLayout.addWidget(self.informationLabel)

        self.employeeSchedule = EmployeeSchedule(self, self.currentEmployee)
        rightLayout.addWidget(self.employeeSchedule)

        middleLayout.addWidget(rightWidget)
        mainLayout.addWidget(middleWidget)

        returnButton = QPushButton("Return to Main Menu", self)
        returnButton.clicked.connect(self.returnToMainView)
        returnButton.setStyleSheet(
            "font-size: 14px; background-color: #6c757d; color: #fff; border: none;")
        returnButton.setFixedSize(QSize(200, 50))
        mainLayout.addWidget(returnButton, alignment=Qt.AlignCenter)

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
                infoText = f"Name: {self.currentEmployee.name}\nHourly Rate: {self.currentEmployee.hourlyRate}"
                self.employeeSchedule.setEmployee(self.currentEmployee)
            else:
                infoText = "No employee selected"
        else:
            infoText = "No employee selected"

        self.informationLabel.setText(infoText)

    def fetchEmployees(self):
        success, self.employees = EmployeeService().getEmployees()
        if not success:
            QMessageBox.warning(self, "Error", self.employees)
            return
        self.employeeDropdown.clear()
        if not self.employees:
            self.employeeDropdown.setAccessibleName("No employees found")
            self.employeeDropdown.setDisabled(True)
            return
        self.employeeDropdown.setDisabled(False)
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
                success, message = EmployeeService().deleteEmployee(self.currentEmployee.id)
                if success:
                    QMessageBox.information(
                        self, "Success", "Employee deleted successfully.")
                    self.fetchEmployees()
                else:
                    QMessageBox.warning(self, "Error", message)
            else:
                print("Deletion canceled by user")
        else:
            print("No employee selected")
