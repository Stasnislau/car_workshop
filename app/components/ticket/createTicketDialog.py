from datetime import datetime
from ...services.ticketService import TicketService
from PyQt5.QtWidgets import (
    QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QDateEdit, QTimeEdit
)
from PyQt5.QtCore import Qt, QDateTime, QTime


class CreateTicketDialog(QDialog):
    def __init__(self, parent, employee):
        super().__init__(parent)
        self.employee = employee
        self.parent = parent
        self.setWindowTitle("Create Ticket")
        self.setFixedSize(350, 500)

        layout = QVBoxLayout()

        # Labels
        brandLabel = QLabel("Brand:", self)
        modelLabel = QLabel("Model:", self)
        registrationIdLabel = QLabel("Registration ID:", self)
        problemDescriptionLabel = QLabel("Problem Description:", self)
        startDateLabel = QLabel("Start Date:", self)
        endTimeLabel = QLabel("End time:", self)

        # Line Edits
        self.brandInput = QLineEdit(self)
        self.modelInput = QLineEdit(self)
        self.registrationIdInput = QLineEdit(self)
        self.problemDescriptionInput = QLineEdit(self)

        # Date Edit
        self.dateEdit = QDateEdit(self)
        
        # only the date part 
        self.dateEdit.setDisplayFormat("yyyy-MM-dd")
        self.dateEdit.setCalendarPopup(True)
        # Set minimum to current date and time
        self.dateEdit.setMinimumDateTime(QDateTime.currentDateTime())
        self.dateEdit.setStyleSheet("padding: 8px; border: 1px solid #ccc;")

        self.startTimeEdit = QTimeEdit(self)
        self.startTimeEdit.setDisplayFormat("HH:00") 
        self.startTimeEdit.setMinimumTime(QTime(0, 0)) 
        self.startTimeEdit.setMaximumTime(QTime(23, 0))
        self.startTimeEdit.setStyleSheet("padding: 8px; border: 1px solid #ccc;")

        self.endTimeEdit = QTimeEdit(self)
        self.endTimeEdit.setDisplayFormat("HH:00")
        self.endTimeEdit.setMinimumTime(QTime(0, 0)) 
        self.endTimeEdit.setMaximumTime(QTime(23, 0)) 
        self.endTimeEdit.setStyleSheet("padding: 8px; border: 1px solid #ccc;")

        placeholders = ["Enter brand", "Enter model", "Enter registration ID",
                        "Enter problem description"]
        line_edits = [self.brandInput, self.modelInput, self.registrationIdInput,
                      self.problemDescriptionInput]

        for line_edit, placeholder in zip(line_edits, placeholders):
            line_edit.setPlaceholderText(placeholder)
            line_edit.setStyleSheet("padding: 8px; border: 1px solid #ccc;")

        # Save Button
        saveButton = QPushButton("Save", self)
        saveButton.clicked.connect(self.saveTicket)
        saveButton.setStyleSheet(
            "background-color: #007bff; color: white; padding: 8px; border: none;")

        # Add Widgets to Layout
        layout.addWidget(brandLabel)
        layout.addWidget(self.brandInput)
        layout.addWidget(modelLabel)
        layout.addWidget(self.modelInput)
        layout.addWidget(registrationIdLabel)
        layout.addWidget(self.registrationIdInput)
        layout.addWidget(problemDescriptionLabel)
        layout.addWidget(self.problemDescriptionInput)
        layout.addWidget(startDateLabel)
        layout.addWidget(self.dateEdit)
        layout.addWidget(self.startTimeEdit)
        layout.addWidget(endTimeLabel)
        layout.addWidget(self.endTimeEdit)
        layout.addWidget(saveButton, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def saveTicket(self):
        brand = self.brandInput.text()
        model = self.modelInput.text()
        registrationId = self.registrationIdInput.text()
        problemDescription = self.problemDescriptionInput.text()
        startDate = self.dateEdit.dateTime().toString("yyyy-MM-dd")
        startTime = self.startTimeEdit.time().toString("HH:00")
        endTime = self.endTimeEdit.time().toString("HH:00")
        
        startDateTime = datetime.strptime(startDate + " " + startTime, "%Y-%m-%d %H:%M")
        endDateTime = datetime.strptime(startDate + " " + endTime, "%Y-%m-%d %H:%M")   
        
        
        if not all([brand, model, registrationId, problemDescription, startDate, startTime]):
            QMessageBox.warning(self, "Error", "All fields are required.")
            return

        success, message = TicketService().createTicket(brand, model, registrationId,
                                                        problemDescription, self.employee.id, startDateTime, endDateTime)
        if success:
            QMessageBox.information(
                self, "Success", "Ticket created successfully.")
            self.parent.fetchTickets()
            self.accept()
        else:
            QMessageBox.warning(self, "Error", message)
