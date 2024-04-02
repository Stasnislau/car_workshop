from PyQt5.QtWidgets import QPushButton, QLabel, QVBoxLayout, QWidget, QMainWindow, QComboBox, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
from ..components.ticket.createTicketDialog import CreateTicketDialog
from ..services.ticketService import TicketService
from ..components.ticket.editTicketDialog import EditTicketDialog
from ..components.ticket.deleteTicketDialog import DeleteTicketDialog


class TicketView(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.currentTicket = None

        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(50, 50, 50, 50)  # Add some margin

        titleLabel = QLabel("Ticket Management", self)
        titleLabel.setStyleSheet(
            "font-size: 24px; font-weight: bold; color: #333;")
        titleLabel.setFixedSize(300, 30)
        mainLayout.addWidget(titleLabel, alignment=Qt.AlignCenter)

        # Middle part with left and right layouts
        middleWidget = QWidget()
        middleLayout = QHBoxLayout(middleWidget)

        # Left part with buttons and dropdown
        leftWidget = QWidget()
        leftLayout = QVBoxLayout(leftWidget)
        self.ticketDropdown = QComboBox(leftWidget)
        self.ticketDropdown.setStyleSheet(
            "font-size: 14px; background-color: #fff; border: 1px solid #ccc;")

        self.ticketDropdown.setFixedSize(200, 50)
        leftLayout.addWidget(self.ticketDropdown, alignment=Qt.AlignCenter)
        self.ticketDropdown.currentIndexChanged.connect(
            self.updateCurrentTicket)

        optionsLayout = QVBoxLayout()
        leftLayout.addLayout(optionsLayout)

        options = ["Add Ticket", "Edit Ticket", "Delete Ticket"]
        for option in options:
            button = QPushButton(option, leftWidget)
            button.setStyleSheet(
                "font-size: 14px; background-color: #007bff; color: #fff; border: none;")
            button.clicked.connect(self.handleOptionClick)
            button.setFixedSize(200, 50)
            optionsLayout.addWidget(button, alignment=Qt.AlignCenter)

        middleLayout.addWidget(leftWidget)

        rightWidget = QWidget()
        rightLayout = QVBoxLayout(rightWidget)

        informationLabel = QLabel("Ticket Information", rightWidget)
        informationLabel.setStyleSheet(
            "font-size: 18px; font-weight: bold; color: #333;")
        informationLabel.setFixedSize(210, 50)
        rightLayout.addWidget(informationLabel, alignment=Qt.AlignCenter)

        self.informationLabel = QLabel("No ticket selected", rightWidget)
        self.informationLabel.setStyleSheet("font-size: 14px; color: #666;")
        rightLayout.addWidget(self.informationLabel, alignment=Qt.AlignCenter)

        middleLayout.addWidget(rightWidget)
        mainLayout.addWidget(middleWidget)

        returnButton = QPushButton("Return to Main Menu", self)
        returnButton.clicked.connect(self.returnToMainView)
        returnButton.setStyleSheet(
            "font-size: 14px; background-color: #6c757d; color: #fff; border: none;")
        returnButton.setFixedSize(200, 50)
        mainLayout.addWidget(returnButton, alignment=Qt.AlignCenter)

        self.fetchTickets()

    def handleOptionClick(self):
        senderButton = self.sender()
        if senderButton:
            optionText = senderButton.text()
            if optionText == "Add Ticket":
                self.addTicket()
            elif optionText == "Edit Ticket":
                self.editTicket()
            elif optionText == "Delete Ticket":
                self.deleteTicket()

    def updateCurrentTicket(self):
        index = self.ticketDropdown.currentIndex()
        if index != -1:
            self.currentTicket = self.tickets[index]
            if self.currentTicket:
                infoText = f"Title: {self.currentTicket.title}\nDescription: {self.currentTicket.description}"
            else:
                infoText = "No ticket selected"
        else:
            infoText = "No ticket selected"

        self.informationLabel.setText(infoText)

    def fetchTickets(self):
        success, self.tickets = TicketService().getTickets()
        if not success:
            QMessageBox.warning(self, "Error", self.tickets)
            return
        self.ticketDropdown.clear()
        if not self.tickets:
            self.ticketDropdown.setAccessibleName("No tickets found")
            self.ticketDropdown.setDisabled(True)
            return
        self.ticketDropdown.setDisabled(False)
        for ticket in self.tickets:
            self.ticketDropdown.addItem(ticket.title)

    def returnToMainView(self):
        parentWidget = self.parent
        if isinstance(parentWidget, QMainWindow):
            parentWidget.changeView("main")

    def addTicket(self):
        CreateTicketDialog(self).show()

    def editTicket(self):
        if self.currentTicket:
            edit_dialog = EditTicketDialog(self, self.currentTicket)
            edit_dialog.exec_()
        else:
            print("No ticket selected")

    def deleteTicket(self):
        if self.currentTicket:
            dialog = DeleteTicketDialog(self.currentTicket.title, self)
            if dialog.exec_():
                success, message = TicketService().deleteTicket(self.currentTicket.id)
                if success:
                    QMessageBox.information(
                        self, "Success", "Ticket deleted successfully.")
                    self.fetchTickets() 
                else:
                    QMessageBox.warning(self, "Error", message)
            else:
                print("Deletion canceled by user")
        else:
            print("No ticket selected")