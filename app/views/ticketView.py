from PyQt5.QtWidgets import (
    QPushButton, QLabel, QVBoxLayout, QWidget, QMainWindow,
    QComboBox, QHBoxLayout, QGridLayout, QFormLayout, QMessageBox, QSizePolicy
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont
from ..services.ticketService import TicketService
from ..services.employeeService import EmployeeService
from ..components.ticket.createTicketDialog import CreateTicketDialog
from ..components.ticket.editTicketDialog import EditTicketDialog
from ..components.ticket.deleteTicketDialog import DeleteTicketDialog
from ..components.ticket.createPartDialog import CreatePartDialog
from ..components.ticket.editPartDialog import EditPartDialog
from ..components.schedules.ticketSchedule import TicketSchedule


class TicketView(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.currentTicket = None
        self.currentEmployee = None
        self.tickets = []

        self.setupUI()

    def setupUI(self):
        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(50, 50, 50, 50)

        titleLabel = QLabel("Ticket Management", self)
        titleLabel.setStyleSheet(
            "font-size: 24px; font-weight: bold; color: #333;")
        titleLabel.setAlignment(Qt.AlignCenter)
        mainLayout.addWidget(titleLabel)

        middleWidget = QWidget()
        middleLayout = QHBoxLayout(middleWidget)
        middleLayout.setContentsMargins(0, 50, 0, 50)

        leftWidget = QWidget()
        leftLayout = QFormLayout(leftWidget)
        leftLayout.setContentsMargins(0, 0, 0, 0)
        leftLayout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        leftLayout.setFormAlignment(Qt.AlignCenter)
        leftLayout.setLabelAlignment(Qt.AlignRight)

        self.employeeDropdown = QComboBox(leftWidget)
        self.employeeDropdown.setStyleSheet(
            "font-size: 14px; background-color: #fff; border: 1px solid #ccc;")
        self.employeeDropdown.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.employeeDropdown.currentIndexChanged.connect(
            self.updateCurrentEmployee)

        leftLayout.addRow("Employee:", self.employeeDropdown)

        rightWidget = QWidget()
        self.ticketDropdown = QComboBox(rightWidget)
        self.ticketDropdown.setStyleSheet(
            "font-size: 14px; background-color: #fff; border: 1px solid #ccc;")
        self.ticketDropdown.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.ticketDropdown.setDisabled(True)
        leftLayout.addRow("Ticket:", self.ticketDropdown)

        self.ticketDropdown.currentIndexChanged.connect(
            self.updateCurrentTicket)

        self.optionsLayout = QGridLayout()
        leftLayout.addRow(self.optionsLayout)

        options = ["Add Ticket", "Edit Ticket", "Delete Ticket",
                   "Add Part", "Edit Parts", "Confirm Estimate"]
        for i, option in enumerate(options):
            button = QPushButton(option, leftWidget)
            button.setStyleSheet(
                "font-size: 14px; background-color: #007bff; color: #fff; border: none;")
            button.setFixedSize(QSize(150, 50))
            button.clicked.connect(self.handleOptionClick)
            self.optionsLayout.addWidget(button, i // 2, i % 2)

        middleLayout.addWidget(leftWidget)
        middleLayout.addWidget(rightWidget)

        middleLayout.setStretchFactor(leftWidget, 1)
        middleLayout.setStretchFactor(rightWidget, 1)

        rightLayout = QFormLayout(rightWidget)
        rightLayout.setContentsMargins(0, 0, 0, 0)
        rightLayout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        rightLayout.setFormAlignment(Qt.AlignCenter)
        rightLayout.setLabelAlignment(Qt.AlignRight)

        self.informationLabel = QLabel("No ticket selected", rightWidget)
        self.informationLabel.setStyleSheet("font-size: 14px; color: #666;")
        self.informationLabel.setAlignment(Qt.AlignCenter)
        rightLayout.addRow(self.informationLabel)

        mainLayout.addWidget(middleWidget)

        returnButton = QPushButton("Return to Main Menu", self)
        returnButton.clicked.connect(self.returnToMainView)
        returnButton.setStyleSheet(
            "font-size: 14px; background-color: #6c757d; color: #fff; border: none;")
        returnButton.setFixedSize(QSize(200, 50))
        mainLayout.addWidget(returnButton, alignment=Qt.AlignCenter)
        self.ticketSchedule = TicketSchedule(self, self.currentTicket)
        rightLayout.addWidget(self.ticketSchedule)
        self.fetchEmployees()
        
           

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
            elif optionText == "Add Part":
                self.addPart()
            elif optionText == "Edit Parts":
                self.editParts()
            elif optionText == "Confirm Estimate":
                self.confirmEstimate()

    def updateTicketDropdown(self):
        index = self.employeeDropdown.currentIndex()
        if index != -1:
            self.currentEmployee = self.employees[index]
            if self.currentEmployee:
                success, tickets = TicketService().getEmployeeTickets(self.currentEmployee.id)
                if success:
                    self.ticketDropdown.clear()
                    for ticket in tickets:
                        self.ticketDropdown.addItem(ticket.registrationId)
                    self.ticketDropdown.setDisabled(False)
                    return
                else:
                    QMessageBox.warning(
                        self, "Error", "Failed to fetch tickets.")
        self.ticketDropdown.clear()
        self.ticketDropdown.setDisabled(True)

    def updateCurrentEmployee(self):
        index = self.employeeDropdown.currentIndex()
        if index != -1:
            self.currentEmployee = self.employees[index]
            self.fetchTickets()

    def updateCurrentTicket(self):
        index = self.ticketDropdown.currentIndex()
        if index != -1:
            self.currentTicket = self.tickets[index]
            if self.currentTicket:
                infoText = f"Registration number: {self.currentTicket.registrationId}\nBrand: {self.currentTicket.brand}\nModel: {self.currentTicket.model}\nProblem Description: {self.currentTicket.problemDescription}\n{self.displayedCost()}"
                self.ticketSchedule.setTicket(self.currentTicket)
            else:
                infoText = "No ticket selected"
        else:
            infoText = "No ticket selected"
            self.currentTicket = None

        self.informationLabel.setText(infoText)

    def fetchEmployees(self):
        success, self.employees = EmployeeService().getEmployees()
        if not success:
            QMessageBox.warning(self, "Error", "Failed to fetch employees.")
            return
        if not self.employees:
            self.employeeDropdown.clear()
            return
        self.employeeDropdown.clear()
        for employee in self.employees:
            self.employeeDropdown.addItem(employee.name)

    def fetchTickets(self):
        if not self.currentEmployee:
            return
        success, self.tickets = TicketService().getEmployeeTickets(self.currentEmployee.id)
        if not success:
            QMessageBox.warning(self, "Error", "Error fetching tickets.")
            return
        if not self.tickets:
            self.ticketDropdown.clear()
            return
        self.ticketDropdown.clear()
        for ticket in self.tickets:
            self.ticketDropdown.addItem(ticket.registrationId)
        if self.tickets:
            self.ticketDropdown.setDisabled(False)

    def returnToMainView(self):
        parentWidget = self.parent
        if isinstance(parentWidget, QMainWindow):
            parentWidget.changeView("main")

    def addTicket(self):
        if self.currentEmployee:
            CreateTicketDialog(self, self.currentEmployee).show()
        else:
            QMessageBox.warning(self, "Error", "Please select an employee.")

    def editTicket(self):
        if self.currentTicket:
            edit_dialog = EditTicketDialog(
                self, self.currentTicket, self.currentEmployee)
            edit_dialog.exec_()
        else:
            QMessageBox.warning(
                self, "Error", "Please select a ticket to edit.")

    def deleteTicket(self):
        if self.currentTicket:
            DeleteTicketDialog(
                self.currentTicket, self, self.currentEmployee).show()
        else:
            QMessageBox.warning(
                self, "Error", "Please select a ticket to delete.")

    def addPart(self):
        if self.currentTicket:
            CreatePartDialog(self, self.currentTicket).show()
        else:
            QMessageBox.warning(self, "Error", "Please select a ticket.")

    def editParts(self):
        if self.currentTicket:
            EditPartDialog(self, self.currentTicket).show()
        else:
            QMessageBox.warning(self, "Error", "Please select a ticket.")

    def confirmEstimate(self):
        if self.currentTicket is None:
            QMessageBox.warning(self, "Error", "Please select a ticket.")
            return
        if self.currentTicket.estimateAccepted is True:
            QMessageBox.warning(self, "Error", "Estimate already accepted.")
            return
        
        success, message = TicketService().confirmEstimate(self.currentTicket.id)
        if success:
            QMessageBox.information(
                self, "Success", "Estimate confirmed successfully.")
            self.currentTicket.estimateAccepted = True
        else:
            QMessageBox.warning(self, "Error", message)

    def displayedCost(self):
        if self.currentTicket.estimateAccepted:
            return f"Price Paid: {self.currentTicket.pricePaid}"
        else:
            return f"Estimate Cost: {self.currentTicket.estimateCost}"


# TODO: Add one more button for the employee to accept the ticket, if the ticket is accepted both the employee and the ticket status goes to "In Progress"
