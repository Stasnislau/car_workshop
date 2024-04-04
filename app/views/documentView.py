from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication, QPushButton, QVBoxLayout, QWidget, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon, QPainter, QTextDocument, QFont
from PyQt5.QtCore import Qt, QRectF, QDate
from PyQt5.QtPrintSupport import QPrinter
from ..components.documents.chooseTicketDialog import ChooseTicketDialog
from ..components.documents.chooseEmployeeDialog import ChooseEmployeeDialog
from ..services.ticketService import TicketService
from ..services.employeeService import EmployeeService
from ..services.ticketService import TicketService


class DocumentView(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.chosenEmployee = None
        self.chosenTicket = None
        layout = QVBoxLayout(self)

        label = QLabel("Welcome to the Document Management System", self)
        layout.addWidget(label)

        ticketButton = QPushButton("Download Ticket Document", self)
        ticketButton.clicked.connect(self.openChooseTicketDialog)
        layout.addWidget(ticketButton)

        employeeButton = QPushButton("Download Employee Document", self)
        employeeButton.clicked.connect(self.openChooseEmployeeDialog)
        layout.addWidget(employeeButton)

        returnButton = QPushButton("Return to Main Menu", self)
        returnButton.clicked.connect(self.returnToMainView)
        layout.addWidget(returnButton)

    def downloadTicketDocument(self, ticket):
        success, content = TicketService().getTicketDocument(ticket.id)
        if not success:
            QMessageBox.warning(self, "Error", content)
            return
        documentContent = f"Ticket ID: {ticket.id}\nBrand: {ticket.brand}\nModel: {ticket.model}\nRegistration ID: {ticket.registrationId}\nProblem Description: {ticket.problemDescription}\nEmployee ID: {ticket.employeeId}\nEstimate Cost: {ticket.estimateCost}\nEstimate Accepted: {ticket.estimateAccepted}\nPrice Paid: {ticket.pricePaid}\nParts:\n"
        for part in content.parts:
            documentContent += f"Part ID: {part.id}\nPart Name: {part.name}\nPart Price: {part.price}\n\n"
        documentContent += "Time Slots:\n"
        for slot in content.timeSlots:
            documentContent += f"Time Slot ID: {slot.id}\nStart Time: {slot.startTime}\nEnd Time: {slot.endTime}\n\n"
        self.downloadDocument(
            documentContent, f"Ticket_Document_{ticket.id}")

    def downloadEmployeeDocument(self, employee):
        success, content = EmployeeService().fetchEmployeeDocument(employee.id)
        if not success:
            QMessageBox.warning(self, "Error", content)
            return
        documentContent = f"Employee Name: {employee.name}\nHourly Rate: {employee.hourlyRate}\n\nTickets:\n"
        for ticket in content.tickets:
            documentContent += f"Ticket ID: {ticket.id}\n"
            for slot in content.timeSlots:
                if slot.ticketId == ticket.id:
                    documentContent += f"Time Slot: {slot.startTime} - {slot.endTime}\n"
            documentContent += "\n"
            
        self.downloadDocument(
            documentContent, f"Employee_Document_{employee.id}")


    def downloadDocument(self, content, filename):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save Document", filename + ".pdf", "PDF Files (*.pdf)", options=options)
        if file_name:
            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(file_name)
            doc = QTextDocument()
            doc.setPlainText(content)
            doc.setDefaultFont(QFont("Arial", 50))            
            painter = QPainter(printer)
            doc.drawContents(painter)
            painter.end()
            QMessageBox.information(
                self, "Success", "Document downloaded successfully.")
        
    def openChooseTicketDialog(self):
        success, tickets = TicketService().getTickets()
        if not success:
            QMessageBox.warning(self, "Error", tickets)
            return
        
        dialog = ChooseTicketDialog(tickets, self)
        dialog.exec_()

    def openChooseEmployeeDialog(self):
        success, employees = EmployeeService().getEmployees()
        if not success:
            QMessageBox.warning(self, "Error", employees)
            return

        dialog = ChooseEmployeeDialog(employees, self)
        dialog.exec_()

    def returnToMainView(self):
        parentWidget = self.parent
        if isinstance(parentWidget, QMainWindow):
            parentWidget.changeView("main")
            
    def chooseEmployee(self, employee):
        self.chosenEmployee = employee
        
    def chooseTicket(self, ticket):
        self.chosenTicket = ticket
