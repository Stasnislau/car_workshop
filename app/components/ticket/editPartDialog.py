from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from ...services.partService import PartService

class EditPartDialog(QDialog):
    def __init__(self, parent, ticket):
        super().__init__(parent)
        self.ticket = ticket
        self.part = None
        self.parts = []
        self.setWindowTitle("Edit Part")
        self.setFixedSize(300, 350)

        layout = QVBoxLayout()

        self.partDropdown = QComboBox(self)
        self.partDropdown.currentIndexChanged.connect(self.on_part_changed)
        self.partDropdown.setStyleSheet("padding: 5px; font-size: 14px;")
        layout.addWidget(QLabel("Part:", self))
        layout.addWidget(self.partDropdown)

        self.nameInput = QLineEdit(self)
        self.nameInput.setEnabled(False)
        self.nameInput.setStyleSheet("border: 1px solid #ccc; padding: 5px; font-size: 14px;")
        self.nameInput.setFixedWidth(280)
        layout.addWidget(QLabel("Name:", self))
        layout.addWidget(self.nameInput)

        self.amountInput = QLineEdit(self)
        self.amountInput.setEnabled(False)
        self.amountInput.setStyleSheet("border: 1px solid #ccc; padding: 5px; font-size: 14px;")
        self.amountInput.setFixedWidth(280)
        layout.addWidget(QLabel("Amount:", self))
        layout.addWidget(self.amountInput)

        self.unitPriceInput = QLineEdit(self)
        self.unitPriceInput.setEnabled(False)
        self.unitPriceInput.setStyleSheet("border: 1px solid #ccc; padding: 5px; font-size: 14px;")
        self.unitPriceInput.setFixedWidth(280)
        layout.addWidget(QLabel("Unit Price:", self))
        layout.addWidget(self.unitPriceInput)

        saveButton = QPushButton("Save", self)
        saveButton.setEnabled(False)
        saveButton.clicked.connect(self.savePart)
        saveButton.setStyleSheet("background-color: #007bff; color: #fff; border: none; padding: 5px 10px; font-size: 14px;")
        saveButton.setFixedWidth(100)
        layout.addWidget(saveButton)

        self.setLayout(layout)

        self.fetchParts()

    def fetchParts(self):
        success, parts = PartService().getPartsForTicket(self.ticket.id)
        if not success:
            QMessageBox.warning(self, "Error", "Failed to fetch parts")
            self.close()
            return

        if not parts:
            QMessageBox.warning(self, "Error", "No parts found for this ticket")
            self.close()
            return

        self.parts = parts
        self.populatePartDropdown()

    def populatePartDropdown(self):
        self.partDropdown.clear()
        for part in self.parts:
            self.partDropdown.addItem(part.name, part.id)
        if self.part:
            index = self.partDropdown.findData(self.part.id)
            if index != -1:
                self.partDropdown.setCurrentIndex(index)

    def on_part_changed(self, index):
        self.part = self.parts[index]
        self.nameInput.setText(self.part.name)
        self.nameInput.setEnabled(True)
        self.amountInput.setText(str(self.part.amount))
        self.amountInput.setEnabled(True)
        self.unitPriceInput.setText(str(self.part.unit_price))
        self.unitPriceInput.setEnabled(True)
        self.saveButton.setEnabled(True)

    def savePart(self):
        part_id = self.partDropdown.currentData()
        name = self.nameInput.text()
        amount = float(self.amountInput.text())
        unit_price = float(self.unitPriceInput.text())

        if not all([name, amount, unit_price]):
            QMessageBox.warning(self, "Error", "All fields are required.")
            return

        success, message = PartService().updatePart(part_id, name, amount, unit_price)
        if success:
            QMessageBox.information(self, "Success", "Part updated successfully.")
            self.accept()
        else:
            QMessageBox.warning(self, "Error", message)
