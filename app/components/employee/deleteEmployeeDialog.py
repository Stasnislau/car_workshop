from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QHBoxLayout, QPushButton


class DeleteEmployeeDialog(QDialog):
    def __init__(self, employee_name, parent=None):
        super(DeleteEmployeeDialog, self).__init__(parent)

        self.setWindowTitle("Delete Employee")

        self.messageLabel = QLabel(
            f"Are you sure you want to delete {employee_name}?")
        self.messageLabel.setStyleSheet("font-size: 14px;")

        self.yesButton = QPushButton("Yes")
        self.noButton = QPushButton("No")

        self.yesButton.clicked.connect(self.accept)
        self.noButton.clicked.connect(self.reject)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.yesButton)
        buttonLayout.addWidget(self.noButton)

        layout = QVBoxLayout()
        layout.addWidget(self.messageLabel)
        layout.addLayout(buttonLayout)

        self.setLayout(layout)
