from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QVBoxLayout, QPushButton, QMessageBox
from PyQt5.QtGui import QDoubleValidator
from ...services.employeeService import EmployeeService


class EditEmployeeDialog(QDialog):
    def __init__(self, parent=None, employee=None):
        super(EditEmployeeDialog, self).__init__(parent)

        self.employee = employee

        self.setWindowTitle("Edit Employee")
        self.setStyleSheet("background-color: #f0f0f0;")
        self.setFixedSize(400, 200)

        self.nameLabel = QLabel("Name:")
        self.nameLabel.setStyleSheet("font-weight: bold;")
        self.nameInput = QLineEdit()
        self.nameInput.setPlaceholderText("Employee Name")
        self.nameInput.setStyleSheet("font-size: 14px")
        self.nameInput.setFixedHeight(30)

        self.priceLabel = QLabel("Price per Hour:")
        self.priceLabel.setStyleSheet("font-weight: bold;")
        self.priceInput = QLineEdit()
        self.priceInput.setPlaceholderText("0.00")
        self.priceInput.setStyleSheet("font-size: 14px")
        self.priceInput.setValidator(QDoubleValidator())
        self.priceInput.setFixedHeight(30)

        self.submitButton = QPushButton("Update")
        self.submitButton.setStyleSheet(
            "background-color: #007bff; color: #fff;")
        self.submitButton.setFixedHeight(35)

        layout = QVBoxLayout()
        layout.addWidget(self.nameLabel)
        layout.addWidget(self.nameInput)
        layout.addWidget(self.priceLabel)
        layout.addWidget(self.priceInput)
        layout.addWidget(self.submitButton)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        self.setLayout(layout)

        self.submitButton.clicked.connect(self.updateEmployee)

        # Populate employee data
        self.populateEmployeeData()

    def populateEmployeeData(self):
        if self.employee:
            self.nameInput.setText(self.employee.name)
            self.priceInput.setText(str(self.employee.hourlyRate))

    def updateEmployee(self):
        name = self.nameInput.text()
        pricePerHour = self.priceInput.text()

        if not name or not pricePerHour:
            QMessageBox.warning(
                self, "Warning", "Please provide both name and price per hour.")
            return

        try:
            pricePerHour = float(pricePerHour)
            if pricePerHour <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(
                self, "Warning", "Price per hour must be a positive number.")
            return

        print(
            f"Updating employee: {self.employee.id}, {name}, {pricePerHour}")
        success, message = EmployeeService().updateEmployee(
            self.employee.id, name, pricePerHour)
        if not success:
            QMessageBox.warning(self, "Warning", message)
            return

        self.accept()
        self.parent().fetchEmployees()
