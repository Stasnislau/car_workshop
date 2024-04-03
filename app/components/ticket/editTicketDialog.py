from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QComboBox
from ...services.ticketService import TicketService


class EditTicketDialog(QDialog):
    def __init__(self, parent, ticket, employee):
        super().__init__(parent)
        self.employee = employee
        self.parent = parent
        self.setWindowTitle("Edit Ticket")
        self.setFixedSize(300, 400)

        layout = QVBoxLayout()

        brandLabel = QLabel("Brand:", self)
        layout.addWidget(brandLabel)
        self.brandInput = QLineEdit(self)
        self.brandInput.setText(ticket.brand)
        self.brandInput.setPlaceholderText("Enter brand")
        layout.addWidget(self.brandInput)

        modelLabel = QLabel("Model:", self)
        layout.addWidget(modelLabel)
        self.modelInput = QLineEdit(self)
        self.modelInput.setText(ticket.model)
        self.modelInput.setPlaceholderText("Enter model")
        layout.addWidget(self.modelInput)

        regIdLabel = QLabel("Registration ID:", self)
        layout.addWidget(regIdLabel)
        self.registrationIdInput = QLineEdit(self)
        self.registrationIdInput.setText(ticket.registrationId)
        self.registrationIdInput.setPlaceholderText("Enter registration ID")
        layout.addWidget(self.registrationIdInput)

        descLabel = QLabel("Problem Description:", self)
        layout.addWidget(descLabel)
        self.problemDescriptionInput = QLineEdit(self)
        self.problemDescriptionInput.setText(ticket.problemDescription)
        self.problemDescriptionInput.setPlaceholderText("Enter problem description")
        layout.addWidget(self.problemDescriptionInput)

        statusLabel = QLabel("Status:", self)
        layout.addWidget(statusLabel)
        self.statusComboBox = QComboBox(self)
        self.statusComboBox.addItems(["Created", "In Progress", "Done"])
        self.statusComboBox.setCurrentText(ticket.state)
        self.statusComboBox.setStyleSheet("QComboBox { padding: 8px; border: 1px solid #ccc; }")
        layout.addWidget(self.statusComboBox)

        saveButton = QPushButton("Save", self)
        saveButton.clicked.connect(self.saveTicket)
        layout.addWidget(saveButton)

        self.setLayout(layout)
        self.ticket = ticket

    def saveTicket(self):
        brand = self.brandInput.text()
        model = self.modelInput.text()
        registrationId = self.registrationIdInput.text()
        problemDescription = self.problemDescriptionInput.text()
        status = self.statusComboBox.currentText()

        if not all([brand, model, registrationId, problemDescription, status]):
            QMessageBox.warning(self, "Error", "All fields are required.")
            return

        success, message = TicketService().updateTicket(
            self.ticket.id, brand, model, registrationId, problemDescription, status)

        if success:
            QMessageBox.information(
                self, "Success", "Ticket updated successfully.")
            self.accept()
        else:
            QMessageBox.warning(self, "Error", message)
