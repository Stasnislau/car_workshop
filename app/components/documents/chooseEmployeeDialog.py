from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QComboBox, QPushButton, QHBoxLayout
from PyQt5 import QtCore

class ChooseEmployeeDialog(QDialog):
    def __init__(self, employees, parent):
        super().__init__(parent)
        self.setWindowTitle("Choose Employee")
        self.parent = parent
        self.employees = employees

        layout = QVBoxLayout(self)

        label = QLabel("Select an Employee:", self)
        layout.addWidget(label)

        self.employeeDropdown = QComboBox(self)
        for employee in employees:
            self.employeeDropdown.addItem(employee.name)
        self.employeeDropdown.currentIndexChanged.connect(self.handleEmployeeChange)
        layout.addWidget(self.employeeDropdown)

        buttonLayout = QHBoxLayout()

        fetchButton = QPushButton("Download", self)
        fetchButton.clicked.connect(self.handleDownload)
        buttonLayout.addWidget(fetchButton)

        cancelButton = QPushButton("Cancel", self)
        cancelButton.clicked.connect(self.reject)
        buttonLayout.addWidget(cancelButton)

        layout.addLayout(buttonLayout)

    def handleEmployeeChange(self): 
        index = self.employeeDropdown.currentIndex()
        print(f"Selected employee: {self.employees[index].name}")
        
    def handleDownload(self):
        index = self.employeeDropdown.currentIndex()
        if index != -1:
            selected_employee = self.employees[index]
            self.parent.downloadEmployeeDocument(selected_employee)
            self.accept()
