from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt
from ...services.timeService import TimeService

class TicketSchedule(QWidget):
    def __init__(self, parent, ticket):
        super().__init__(parent)
        self.ticket = ticket
        self.setupUI()

    def setupUI(self):
        layout = QVBoxLayout(self)

        title = QLabel("Ticket Schedule", self)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.scheduleTable = QTableWidget(self)
        self.scheduleTable.setColumnCount(3)
        self.scheduleTable.setHorizontalHeaderLabels(["Date", "Start Time", "End Time"])
        layout.addWidget(self.scheduleTable)

        self.setLayout(layout)

        self.fetchSchedule()

    def fetchSchedule(self):
        if self.ticket:
            success, timeSlots = TimeService().getTimeSlotsForTicket(self.ticket.id)
            if success:
                self.updateSchedule(timeSlots)

    def updateSchedule(self, timeSlots):
        self.scheduleTable.setRowCount(len(timeSlots))
        for row, timeSlot in enumerate(timeSlots):
            date = timeSlot.startTime.strftime("%Y-%m-%d") 
            start_time = timeSlot.startTime.strftime("%H:%M") 
            end_time = timeSlot.endTime.strftime("%H:%M")

            self.scheduleTable.setItem(row, 0, QTableWidgetItem(date))
            self.scheduleTable.setItem(row, 1, QTableWidgetItem(start_time))
            self.scheduleTable.setItem(row, 2, QTableWidgetItem(end_time))

        self.scheduleTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
    def setTicket(self, ticket):
        self.ticket = ticket
        if self.ticket:
            self.fetchSchedule()
        else :
            self.scheduleTable.setRowCount(0)

