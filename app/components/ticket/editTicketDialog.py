from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
from ...services.ticketService import TicketService

class EditTicketDialog(QDialog):
    def __init__(self, parent, ticket, employee):
        super().__init__(parent)
        self.setWindowTitle("Edit Ticket")
        self.setFixedSize(300, 200)
        self.employee = employee

        layout = QVBoxLayout()

        self.titleInput = QLineEdit(self)
        self.titleInput.setText(ticket.title)
        layout.addWidget(self.titleInput)

        self.descriptionInput = QLineEdit(self)
        self.descriptionInput.setText(ticket.description)
        layout.addWidget(self.descriptionInput)

        saveButton = QPushButton("Save", self)
        saveButton.clicked.connect(self.saveTicket)
        layout.addWidget(saveButton)

        self.setLayout(layout)
        self.ticket = ticket

    def saveTicket(self):
        title = self.titleInput.text()
        description = self.descriptionInput.text()
        if not title or not description:
            QMessageBox.warning(self, "Error", "Title and description are required.")
            return
        success, message = TicketService().updateTicket(self.ticket.id, title, description)
        if success:
            QMessageBox.information(self, "Success", "Ticket updated successfully.")
            self.accept()
        else:
            QMessageBox.warning(self, "Error", message)
