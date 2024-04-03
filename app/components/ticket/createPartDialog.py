from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from ...services.partService import PartService
from PyQt5.QtGui import QFont, QColor


class CreatePartDialog(QDialog):
    def __init__(self, parent, ticket):
        super().__init__(parent)
        self.setWindowTitle("Create Part")
        self.setFixedSize(300, 350)
        self.parent = parent
        self.ticket = ticket

        layout = QVBoxLayout()

        label_font = QFont("Arial", 12)
        name_label = QLabel("Name:", self)
        name_label.setFont(label_font)
        amount_label = QLabel("Amount:", self)
        amount_label.setFont(label_font)
        unit_price_label = QLabel("Unit Price:", self)
        unit_price_label.setFont(label_font)

        input_font = QFont("Arial", 12)
        input_bg_color = QColor("#f2f2f2")
        self.nameInput = QLineEdit(self)
        self.nameInput.setFont(input_font)
        self.nameInput.setStyleSheet(f"background-color: {input_bg_color};")
        self.amountInput = QLineEdit(self)
        self.amountInput.setFont(input_font)
        self.amountInput.setStyleSheet(f"background-color: {input_bg_color};")
        self.unitPriceInput = QLineEdit(self)
        self.unitPriceInput.setFont(input_font)
        self.unitPriceInput.setStyleSheet(
            f"background-color: {input_bg_color};")

        save_button_font = QFont("Arial", 12)
        save_button_bg_color = QColor("#4caf50")
        save_button_text_color = QColor("#ffffff")
        saveButton = QPushButton("Save", self)
        saveButton.setFont(save_button_font)
        saveButton.setStyleSheet(
            f"background-color: {save_button_bg_color}; color: {save_button_text_color};")
        saveButton.clicked.connect(self.savePart)

        layout.addWidget(name_label)
        layout.addWidget(self.nameInput)
        layout.addWidget(amount_label)
        layout.addWidget(self.amountInput)
        layout.addWidget(unit_price_label)
        layout.addWidget(self.unitPriceInput)
        layout.addWidget(saveButton)

        self.setLayout(layout)

    def savePart(self):
        try:
            if not self.nameInput.text() or not self.amountInput.text() or not self.unitPriceInput.text():
                QMessageBox.warning(self, "Error", "All fields are required.")
                return
            name = self.nameInput.text()
            amount = float(self.amountInput.text())
            unitPrice = float(self.unitPriceInput.text())

            if not all([name, amount, unitPrice]):
                QMessageBox.warning(self, "Error", "All fields are required.")
                return

            success, message = PartService().createPart(
                self.ticket.id, name, amount, unitPrice)
            if success:
                QMessageBox.information(
                    self, "Success", "Part created successfully.")
                self.accept()
            else:
                QMessageBox.warning(self, "Error", message)
        except ValueError:
            QMessageBox.warning(
                self, "Error", "Amount and unit price must be numbers.")
            return
