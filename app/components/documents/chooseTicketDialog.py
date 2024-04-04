from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QComboBox, QPushButton, QHBoxLayout

class ChooseTicketDialog(QDialog):
    def __init__(self, tickets, parent):
        super().__init__(parent)
        self.setWindowTitle("Choose Ticket")
        self.parent = parent
        self.tickets = tickets

        layout = QVBoxLayout(self)

        label = QLabel("Select a Ticket:", self)
        layout.addWidget(label)

        self.ticketDropdown = QComboBox(self)
        for ticket in tickets:
            self.ticketDropdown.addItem(str(ticket.id)) 
        self.ticketDropdown.currentIndexChanged.connect(self.handleTicketChange)
        layout.addWidget(self.ticketDropdown)

        buttonLayout = QHBoxLayout()

        chooseButton = QPushButton("Choose", self)
        chooseButton.clicked.connect(self.handleChooseTicket)
        buttonLayout.addWidget(chooseButton)

        cancelButton = QPushButton("Cancel", self)
        cancelButton.clicked.connect(self.reject)
        buttonLayout.addWidget(cancelButton)

        layout.addLayout(buttonLayout)

    def handleTicketChange(self):
        index = self.ticketDropdown.currentIndex()
        if index != -1:
            print(f"Selected ticket ID: {self.tickets[index].id}")

    def handleChooseTicket(self):
        index = self.ticketDropdown.currentIndex()
        if index != -1:
            selected_ticket = self.tickets[index]
            self.parent.downloadTicketDocument(selected_ticket)
            self.accept()
