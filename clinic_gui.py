import sys
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QMainWindow, QGridLayout, QPushButton, QWidget, QSizePolicy, QLabel, QLineEdit, QMessageBox
from clinic.controller import Controller
from .home_menu_gui import Home_Menu
from clinic.exception.invalid_login_exception import InvalidLoginException

class ClinicGUI(QMainWindow):
    """
    the main window of our walk in clinic database program!
    """
    def __init__(self):
        """
        creates the main window and formats it
        """
        super().__init__()
        self.controller = Controller(True)
        self.setWindowTitle("Clinic Database")
        self.setMinimumSize(QSize(800, 500))
        self.check_logged_on()
        self.setStyleSheet('''
            QWidget{
                background-color: #ffe6f2;
            }
        
        ''')
    def check_logged_on(self):
        """
        adds a login menu widget to the main window
        """
        login_widget = LoginMenu(self, self.controller)
        self.setCentralWidget(login_widget)

    def create_home(self):
        """
        sets the clinic's home menu as the main window's central widget once a user has successfully logged in
        """
        home_widget = Home_Menu(self.controller, self)
        self.setCentralWidget(home_widget)
        self.setWindowTitle("Main Menu")
    
class LoginMenu(QWidget):
    """
    an widget that allows the user to enter their username and password to log into the clinic database
    """
    def __init__(self, main_window, controller):
        """
        creates a format which contains editable lines for the user to enter their username and password
        """
        super().__init__()
        self.main = main_window
        self.controller = controller
        layout = QGridLayout()
        self.setStyleSheet('''
            QWidget{
                background-color: white;
                color: black;           
            }
            QLabel {
                background-color: transparent; 
            }
            QMessageBox{
                background-color: white;
                color: black;           
            }
        ''')
        title = QLabel("Clinic Home Menu")
        font = QFont("Helvetica", 22)
        title.setFont(font)
        layout.addWidget(title, 0, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.text_username = QLineEdit()
        self.text_password = QLineEdit()
        self.text_password.setEchoMode(QLineEdit.EchoMode.Password)

        layout.addWidget(self.text_username, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.text_password, 2, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        self.text_username.setPlaceholderText("Username")
        self.text_password.setPlaceholderText("Password")


        self.button_login_window = QPushButton("Login")
        self.button_quit = QPushButton("Quit")

        self.button_login_window.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.button_login_window.setFixedSize(75, 30)

        self.button_quit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.button_quit.setFixedSize(75, 30)

        layout.addWidget(self.button_login_window, 3, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.button_quit, 4, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        
        layout.setRowStretch(0, 2)
        layout.setRowStretch(6, 2)
        layout.setRowStretch(3, 1)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(2, 1)
        
        self.setLayout(layout)

        self.button_login_window.clicked.connect(self.open_login_window)
        self.button_quit.clicked.connect(self.quit_button_clicked)

    def open_login_window(self):
        """
        compares the username and password with ones that are accepted and either calls the create_home method or presents a login failure warning to the user
        """
        username = self.text_username.text()
        password = self.text_password.text()

        try:
            self.controller.login(username, password)
            QMessageBox.information(self, "Login Success", "You have successfully logged in")
            self.main.create_home()
            self.close()
        except InvalidLoginException:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password")

        self.text_username.clear()
        self.text_password.clear()
    
    def quit_button_clicked(self):
        """
        ends the application
        """
        QApplication.quit()

def main():
    """
    creates application, event loop and main window
    """
    app = QApplication(sys.argv)
    window = ClinicGUI()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()
