from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
from ...services.timeService import timeService

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
        self.scheduleTable.setColumnCount(2)
        self.scheduleTable.setHorizontalHeaderLabels(["Time Slot", "Ticket"])
        layout.addWidget(self.scheduleTable)

        self.setLayout(layout)

        self.fetchSchedule()

    def fetchSchedule(self):
        if self.employee:
            success, schedule = ScheduleService().getEmployeeSchedule(self.employee.id)
            if success:
                self.updateSchedule(schedule)

    def updateSchedule(self, schedule):
        self.scheduleTable.setRowCount(len(schedule))
        for row, (time_slot, ticket) in enumerate(schedule):
            self.scheduleTable.setItem(row, 0, QTableWidgetItem(str(time_slot)))
            self.scheduleTable.setItem(row, 1, QTableWidgetItem(ticket))