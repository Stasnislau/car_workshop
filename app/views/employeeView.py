from PyQt5.QtWidgets import QPushButton, QLabel, QVBoxLayout, QWidget, QMainWindow, QComboBox, QHBoxLayout
from PyQt5.QtCore import Qt
from ..components.employee.createEmployeeDialog import CreateEmployeeDialog

class EmployeeView(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        mainLayout = QVBoxLayout(self)

        titleLabel = QLabel("Employee Management", self)
        titleLabel.setStyleSheet("font-size: 24px; font-weight: bold;")
        titleLabel.setFixedSize(300, 50)
        mainLayout.addWidget(titleLabel, alignment=Qt.AlignCenter)

        # Middle part with left and right layouts
        middleWidget = QWidget()
        middleLayout = QHBoxLayout(middleWidget)  # Change to QHBoxLayout

        # Left part with buttons and dropdown
        leftWidget = QWidget()
        leftLayout = QVBoxLayout(leftWidget)

        optionsLayout = QVBoxLayout()
        leftLayout.addLayout(optionsLayout)

        options = ["Add Employee", "Edit Employee", "Delete Employee"]
        for option in options:
            button = QPushButton(option, leftWidget)
            button.clicked.connect(self.handleOptionClick)
            button.setFixedSize(200, 50)  # Set size for each button
            optionsLayout.addWidget(button, alignment=Qt.AlignCenter)

        self.employeeDropdown = QComboBox(leftWidget)
        self.employeeDropdown.setFixedSize(200, 50)
        leftLayout.addWidget(self.employeeDropdown, alignment=Qt.AlignCenter)

        middleLayout.addWidget(leftWidget)  # Add leftWidget to middleLayout

        # Right part with rectangles
        rightWidget = QWidget()
        rightLayout = QVBoxLayout(rightWidget)

        # Add widgets to rightLayout here
        
        informationLabel = QLabel("Employee Information", rightWidget)
        informationLabel.setStyleSheet("font-size: 18px; font-weight: bold;")
        informationLabel.setFixedSize(200, 50)
        rightLayout.addWidget(informationLabel, alignment=Qt.AlignCenter)
        
        # TODO: include name, price per hour, 
        
        informationLabel = QLabel("Employee Schedule", rightWidget)
        informationLabel.setStyleSheet("font-size: 18px; font-weight: bold;")
        informationLabel.setFixedSize(200, 50)
        
        rightLayout.addWidget(informationLabel, alignment=Qt.AlignCenter)
        
        scheduleContainer = QWidget(rightWidget)
        scheduleLayout = QVBoxLayout(scheduleContainer)
        scheduleContainer.setStyleSheet("border: 1px solid black;")
        scheduleContainer.setFixedSize(500, 400)
        rightLayout.addWidget(scheduleContainer, alignment=Qt.AlignCenter)        

        middleLayout.addWidget(rightWidget)  # Add rightWidget to middleLayout

        mainLayout.addWidget(middleWidget)  # Add middleWidget to mainLayout

        returnButton = QPushButton("Return to Main Menu", self)
        returnButton.clicked.connect(self.returnToMainView)
        returnButton.setFixedSize(200, 50)  # Set size for returnButton
        mainLayout.addWidget(returnButton, alignment=Qt.AlignCenter)

    def handleOptionClick(self):
        senderButton = self.sender()
        if senderButton:
            optionText = senderButton.text()
            if optionText == "Add Employee":
                self.addEmployee()
            elif optionText == "Edit Employee":
                self.editEmployee()
            elif optionText == "Delete Employee":
                self.deleteEmployee()

    def returnToMainView(self):
        parentWidget = self.parent
        if isinstance(parentWidget, QMainWindow):
            parentWidget.changeView("main")

    def addEmployee(self):
        CreateEmployeeDialog(self).show()

    def editEmployee(self):
        # Functionality to edit an employee
        pass

    def deleteEmployee(self):
        # Functionality to delete an employee
        pass