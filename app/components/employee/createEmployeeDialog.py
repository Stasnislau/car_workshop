from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QVBoxLayout, QPushButton, QMessageBox
from PyQt5.QtGui import QDoubleValidator
from ...services.employeeService import EmployeeService

class CreateEmployeeDialog(QDialog):
    def __init__(self, parent=None):
        super(CreateEmployeeDialog, self).__init__(parent)

        self.setWindowTitle("Create Employee")
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

        self.submitButton = QPushButton("Create")
        self.submitButton.setStyleSheet("background-color: #007bff; color: #fff;")
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

        self.submitButton.clicked.connect(self.createEmployee)

    def createEmployee(self):
        name = self.nameInput.text()
        price_per_hour = self.priceInput.text()

        if not name or not price_per_hour:
            QMessageBox.warning(
                self, "Warning", "Please provide both name and price per hour.")
            return

        try:
            price_per_hour = float(price_per_hour)
            if price_per_hour <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(
                self, "Warning", "Price per hour must be a positive number.")
            return

        print(f"Creating employee: {name}, {price_per_hour}")
        employeeService = EmployeeService()
        success, employee = employeeService.createEmployee(name, price_per_hour)
        if not success:
            QMessageBox.warning(self, "Warning", employee)
            return

        self.accept()
        self.parent().fetchEmployees()
