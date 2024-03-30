from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLineEdit, QLabel


class EmployeeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Employee Management")

        # Create widgets
        self.name_label = QLabel("Employee Name:")
        self.name_input = QLineEdit()
        self.add_button = QPushButton("Add Employee")
        self.remove_button = QPushButton("Remove Employee")

        # Create layout
        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.add_button)
        layout.addWidget(self.remove_button)

        # Set layout
        self.setLayout(layout)
