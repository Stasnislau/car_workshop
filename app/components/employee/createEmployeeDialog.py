from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QVBoxLayout, QPushButton, QMessageBox
from ...services.employeeService import EmployeeService


class CreateEmployeeDialog(QDialog):
    def __init__(self, parent=None):
        super(CreateEmployeeDialog, self).__init__(parent)

        self.setWindowTitle("Create Employee")

        self.nameLabel = QLabel("Name")
        self.nameInput = QLineEdit()

        self.priceLabel = QLabel("Price per Hour")
        self.priceInput = QLineEdit()

        self.submitButton = QPushButton("Create")

        layout = QVBoxLayout()
        layout.addWidget(self.nameLabel)
        layout.addWidget(self.nameInput)
        layout.addWidget(self.priceLabel)
        layout.addWidget(self.priceInput)
        layout.addWidget(self.submitButton)

        self.setLayout(layout)

        self.submitButton.clicked.connect(self.createEmployee)

    def createEmployee(self):
        # Retrieve employee details from input fields
        name = self.nameInput.text()
        price_per_hour = self.priceInput.text()

        # Ensure both name and price per hour are provided
        if not name or not price_per_hour:
            QMessageBox.warning(
                self, "Warning", "Please provide both name and price per hour.")
            return

        # Ensure price per hour is a valid number
        try:
            price_per_hour = float(price_per_hour)
            if price_per_hour <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(
                self, "Warning", "Price per hour must be a positive number.")
            return

        # Here you can add the code to create the employee in your system
        print(f"Creating employee: {name}, {price_per_hour}")
        # put the employee in the database
        employeeService = EmployeeService()
        success, employee = employeeService.createEmployee(name, price_per_hour)
        if not success:
            QMessageBox.warning(self, "Warning", employee)
            return

        # Optionally, you can close the dialog after successful creation
        self.accept()
