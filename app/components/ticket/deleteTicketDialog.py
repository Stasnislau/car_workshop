from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
from ...services.ticketService import TicketService

class DeleteTicketDialog(QDialog):
    def __init__(self, ticket, parent, employee):
        super().__init__(parent)
        self.setWindowTitle("Delete Ticket")
        self.setFixedSize(300, 100)
        self.employee = employee
        self.ticket = ticket
        self.parent = parent

        layout = QVBoxLayout()

        messageLabel = QLabel(f"Do you want to delete the ticket '{ticket.registrationId}'?", self)
        layout.addWidget(messageLabel)

        yesButton = QPushButton("Yes", self)
        yesButton.clicked.connect(self.deleteTicket)
        layout.addWidget(yesButton)

        noButton = QPushButton("No", self)
        noButton.clicked.connect(self.reject)
        layout.addWidget(noButton)

        self.setLayout(layout)

    def deleteTicket(self):
        success, message = TicketService().deleteTicket(self.ticket.id)
        if success:
            QMessageBox.information(self, "Success", "Ticket deleted successfully.")
            self.parent.fetchTickets()
            self.accept()
        else:
            QMessageBox.warning(self, "Error", message)