from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication, QPushButton
from PyQt5.QtGui import QPixmap, QBrush, QIcon
from PyQt5.QtCore import QRect, Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Car Workshop")
        palette = self.palette()
        self.setPalette(palette)

        employee_navigation_button = QPushButton("Employee Management", self)
        employee_navigation_button.setGeometry(QRect(100, 250, 500, 500))
        employee_navigation_button.setIcon(QIcon("assets/employee_icon.jpg"))
        employee_navigation_button.setIconSize(employee_navigation_button.size())
        

        ticket_navigation_button = QPushButton("Ticket Management", self)
        ticket_navigation_button.setGeometry(QRect(700, 250, 500, 500))
        ticket_navigation_button.setIcon(QIcon("assets/ticket_icon.jpg"))
        ticket_navigation_button.setIconSize(ticket_navigation_button.size())

        document_navigation_button = QPushButton("Document Management", self)
        document_navigation_button.setGeometry(QRect(1300, 250, 500, 500))
        document_navigation_button.setIcon(QIcon("assets/documents_icon.jpg"))
        document_navigation_button.setIconSize(document_navigation_button.size())
        

        # Center the window on the screen
        screen_geometry = QApplication.desktop().screenGeometry()
        window_geometry = self.geometry()
        window_center_point = window_geometry.center()
        screen_center_point = screen_geometry.center()
        window_center_point.setX(
            screen_center_point.x() - round(window_geometry.width() / 2))
        window_center_point.setY(
            screen_center_point.y() - round(window_geometry.height() / 2))
        self.move(window_center_point)

        # Set the central widget to None as we are not using it anymore
        self.setCentralWidget(None)

app = QApplication([])
window = MainWindow()
window.show()
app.exec_()