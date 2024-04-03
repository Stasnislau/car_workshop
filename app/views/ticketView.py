from PyQt5.QtWidgets import (
    QPushButton, QLabel, QVBoxLayout, QWidget, QMainWindow,
    QComboBox, QHBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt
from ..components.ticket.createTicketDialog import CreateTicketDialog
from ..services.ticketService import TicketService
from ..services.employeeService import EmployeeService
from ..components.ticket.editTicketDialog import EditTicketDialog
from ..components.ticket.deleteTicketDialog import DeleteTicketDialog


class TicketView(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.currentTicket = None
        self.currentEmployee = None

        self.setupUI()

    def setupUI(self):
        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(50, 50, 50, 50)

        titleLabel = QLabel("Ticket Management", self)
        titleLabel.setStyleSheet(
            "font-size: 24px; font-weight: bold; color: #333;")
        titleLabel.setFixedSize(300, 30)
        mainLayout.addWidget(titleLabel, alignment=Qt.AlignCenter)

        middleWidget = QWidget()
        middleLayout = QHBoxLayout(middleWidget)

        leftWidget = QWidget()
        leftLayout = QVBoxLayout(leftWidget)

        self.employeeDropdown = QComboBox(leftWidget)
        self.employeeDropdown.setStyleSheet(
            "font-size: 14px; background-color: #fff; border: 1px solid #ccc;")
        self.employeeDropdown.setFixedSize(200, 50)
        self.employeeDropdown.currentIndexChanged.connect(
            self.updateTicketDropdown)
        leftLayout.addWidget(self.employeeDropdown, alignment=Qt.AlignCenter)

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

        self.ticketDropdown = QComboBox(rightWidget)
        self.ticketDropdown.setStyleSheet(
            "font-size: 14px; background-color: #fff; border: 1px solid #ccc;")
        self.ticketDropdown.setFixedSize(200, 50)
        rightLayout.addWidget(self.ticketDropdown, alignment=Qt.AlignCenter)

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

    def updateTicketDropdown(self):
        index = self.employeeDropdown.currentIndex()
        if index != -1:
            self.currentEmployee = self.employees[index]
            if self.currentEmployee:
                success, tickets = TicketService().getEmployeeTickets(self.currentEmployee.id)
                if success:
                    self.ticketDropdown.clear()
                    for ticket in tickets:
                        self.ticketDropdown.addItem(ticket.title)
                    self.ticketDropdown.setDisabled(False)
                    return
        self.ticketDropdown.clear()
        self.ticketDropdown.setDisabled(True)

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

    def fetchEmployees(self):
        success, self.employees = EmployeeService().getEmployees()
        if not success:
            QMessageBox.warning(self, "Error", self.employees)
            return
        if not self.employees:
            QMessageBox.warning(self, "Error", "No employees found")
            return
        for employee in self.employees:
            self.employeeDropdown.addItem(employee.name)

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
            edit_dialog = EditTicketDialog(self.currentTicket)
            edit_dialog.exec_()
        else:
            QMessageBox.warning(
                self, "Error", "Please select a ticket to edit.")

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
            QMessageBox.warning(
                self, "Error", "Please select a ticket to delete.")


# TODO: добавить вьюху для тикетов, которая позволит создавать, редактировать и удалять тикеты
# TODO: дропдаун сотрудников, от которых зависит второй дропдаун с тикетами. Нижний дропдаун задизейблен, пока не выбран сотрудник
# TODO: оно крашится вот с такой херней пока
#  File "c:\Everything\Programming\WUT\Car_workshop\app\views\ticketView.py", line 102, in updateTicketDropdown
#     success, tickets = TicketService().getEmployeeTickets(self.currentEmployee.id)
# AttributeError: 'TicketService' object has no attribute 'getEmployeeTickets'