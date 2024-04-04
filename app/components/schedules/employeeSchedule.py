from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt
from ...services.timeService import TimeService

class EmployeeSchedule(QWidget):
    def __init__(self, parent, employee):
        super().__init__(parent)
        self.employee = employee
        self.setupUI()

    def setupUI(self):
        layout = QVBoxLayout(self)

        title = QLabel("Employee Schedule", self)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.scheduleTable = QTableWidget(self)
        self.scheduleTable.setColumnCount(4)
        self.scheduleTable.setHorizontalHeaderLabels(["Date", "Start Time", "End Time", "Ticket"])
        layout.addWidget(self.scheduleTable)

        self.setLayout(layout)

        self.fetchSchedule()

    def fetchSchedule(self):
        if self.employee:
            success, timeSlots = TimeService().getTimeSlotsForEmployee(self.employee.id)
            if success:
                self.updateSchedule(timeSlots)

    def updateSchedule(self, timeSlots):
        self.scheduleTable.setRowCount(len(timeSlots))
        for row, timeSlot in enumerate(timeSlots):
            date = timeSlot.startTime.strftime("%Y-%m-%d") 
            startTime = timeSlot.startTime.strftime("%H:%M") 
            endTime = timeSlot.endTime.strftime("%H:%M")
            registrationId = timeSlot.registrationId

            self.scheduleTable.setItem(row, 0, QTableWidgetItem(date))
            self.scheduleTable.setItem(row, 1, QTableWidgetItem(startTime))
            self.scheduleTable.setItem(row, 2, QTableWidgetItem(endTime))
            self.scheduleTable.setItem(row, 3, QTableWidgetItem(registrationId))

        self.scheduleTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
    def setEmployee(self, employee):
        self.employee = employee
        if self.employee:
            self.fetchSchedule()
        else:
            self.scheduleTable.setRowCount(0)