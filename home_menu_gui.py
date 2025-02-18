
from PyQt6.QtCore import Qt, QSize, QAbstractTableModel, QRegularExpression, QDate
from PyQt6.QtGui import QFont, QIntValidator, QRegularExpressionValidator
from PyQt6.QtWidgets import QDialog, QGridLayout, QPushButton, QSizePolicy, QLabel, QLineEdit, QMessageBox, QTableView, QDateEdit
from clinic.controller import Controller
from .appointment_gui import AppointmentGUI
from clinic.exception.illegal_operation_exception import IllegalOperationException

class Home_Menu(QDialog):
    def __init__(self, controller, main_window):
        """
        creates the home menu window which contains button widgets that allow the user to manipulate and view patients in the database
        """
        super().__init__()
        self.controller = controller
        self.main = main_window
        layout = QGridLayout()
        self.setStyleSheet('''
            QWidget{
                background-color: white;
                color: black;
            }
            QLabel {
                background-color: transparent;
            }
            QDialog{
                background-color: #ffe6f2; 
            }
        ''')

        title = QLabel("Clinic Home Menu")
        font = QFont("Helvetica", 22)
        title.setFont(font)
        layout.addWidget(title, 0, 1, alignment=Qt.AlignmentFlag.AlignCenter)

        """
        creating all the home menu buttons
        """
        self.button_create_patient = QPushButton("Add new patient")
        self.button_search_patient = QPushButton("Search for a patient by PHN")
        self.button_retrieve_patient = QPushButton("Retrieve patients by name")
        self.button_change_patient = QPushButton("Update patient data")
        self.button_remove_patient = QPushButton("Remove a patient")
        self.button_list_patient = QPushButton("List all patients")
        self.button_appt = QPushButton("Start appointment")
        self.button_logout = QPushButton("Logout")
        
        """
        setting up button size and alignment in window
        """
        buttons = [self.button_create_patient, self.button_search_patient, self.button_retrieve_patient, self.button_change_patient, self.button_remove_patient, self.button_list_patient, self.button_appt, self.button_logout]
        
        for button, i in zip(buttons, range(1, 9)):
            button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            button.setFixedSize(200, 30)
            layout.addWidget(button, i, 1,  alignment=Qt.AlignmentFlag.AlignCenter)
        
        for i in range(0, 9):
            layout.setRowStretch(i, 1)

        self.setLayout(layout)

        self.button_create_patient.clicked.connect(lambda: self.create_dialog(1))
        self.button_search_patient.clicked.connect(lambda: self.create_dialog(2))
        self.button_retrieve_patient.clicked.connect(lambda: self.create_dialog(3))
        self.button_change_patient.clicked.connect(lambda: self.create_dialog(4))
        self.button_remove_patient.clicked.connect(lambda: self.create_dialog(5))
        self.button_list_patient.clicked.connect(lambda: self.create_dialog(6))
        self.button_appt.clicked.connect(lambda: self.create_dialog(7))
        self.button_logout.clicked.connect(self.logout)

    def create_dialog(self, number):
        """
        creates correct window based off of which button was pushed using a numeric code associated with a certain user story
        """
        if number == 1:
            self.create_patient_window = CreatePatient(self.controller)
            self.create_patient_window.show()
        elif number == 2:
            self.create_search_window = SearchPatient(self.controller)
            self.create_search_window.show()
        elif number == 3:
            self.create_retrieve_window = RetrievePatient(self.controller)
            self.create_retrieve_window.show()
        elif number == 4:
            self.create_update_window = UpdatePatient(self.controller)
            self.create_update_window.show()
        elif number == 5:
            self.create_list_window = RemovePatient(self.controller)
            self.create_list_window.show()
        elif number == 6:
            self.create_list_window = ListPatient(self.controller)
            self.create_list_window.show()
        elif number == 7:
            self.create_app_window = Appointment(self.controller, self)
            self.create_app_window.show()
    
    def logout(self):
        """
        confirms user wants to logout of clinic and if yes, exits the home menu and returns to login window
        """
        reply = QMessageBox.question(None, "Confirmation", "Logout of clinic?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,  QMessageBox.StandardButton.Yes)
        if reply == QMessageBox.StandardButton.Yes:
            self.controller.logout()
            self.main.check_logged_on()

class CreatePatient(QDialog):
        """
        a window that allows the user to new patients for the database
        """
        def __init__(self, controller):
            """
            sets up the pop up window to allow the user to fill in the fields to create a new patient
            """
            super().__init__()
            self.controller = controller
            self.setModal(True)
            layout = QGridLayout()
            self.setStyleSheet('''
                QWidget{
                    background-color: #ffe6f2;
                    color: black;
                }
                QLabel {
                    background-color: transparent;
                }
                QLineEdit{
                    background-color: white; 
                }
                QPushButton{
                    background-color: white; 
                }
                QDateEdit{
                    background-color: white;
                }
            ''')

            self.setWindowTitle("Create New Patient")
            self.setMinimumSize(QSize(500, 300))

            self.title_label = QLabel("Enter new patient's data")
            layout.addWidget(self.title_label, 0, 0, alignment=Qt.AlignmentFlag.AlignLeft)

            self.phn_label = QLabel("Personal Health Number (PHN):")
            self.phn_input = QLineEdit()
            self.phn_input.setPlaceholderText("PHN")
            self.phn_input.setValidator(QIntValidator())
            layout.addWidget(self.phn_label, 1, 0, alignment=Qt.AlignmentFlag.AlignLeft)
            layout.addWidget(self.phn_input, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)

            self.name_label = QLabel("Full Name: ")
            self.name_input = QLineEdit()
            self.name_input.setPlaceholderText("First Last")
            layout.addWidget(self.name_label, 2, 0, alignment=Qt.AlignmentFlag.AlignLeft)
            layout.addWidget(self.name_input, 2, 1, alignment=Qt.AlignmentFlag.AlignCenter)

            self.bday_label = QLabel("Birthdate (YYYY-MM-DD): ")
            self.bday_input = QDateEdit()
            self.bday_input.setFixedSize(140, 25)
            self.bday_input.setDate(QDate.currentDate())
            self.bday_input.setDisplayFormat("yyyy-MM-dd")
            layout.addWidget(self.bday_label, 3, 0, alignment=Qt.AlignmentFlag.AlignLeft)
            layout.addWidget(self.bday_input, 3, 1, alignment=Qt.AlignmentFlag.AlignCenter)

            self.phone_label = QLabel("Phone: ")
            self.phone_input = QLineEdit()
            self.phone_input.setValidator(QIntValidator())
            self.phone_input.setPlaceholderText("Phone Number ")
            layout.addWidget(self.phone_label, 4, 0, alignment=Qt.AlignmentFlag.AlignLeft)
            layout.addWidget(self.phone_input, 4, 1, alignment=Qt.AlignmentFlag.AlignCenter)

            self.email_label = QLabel("Email: ")
            self.email_input = QLineEdit()
            self.email_input.setPlaceholderText("Email Address")
            layout.addWidget(self.email_label, 5, 0, alignment=Qt.AlignmentFlag.AlignLeft)
            layout.addWidget(self.email_input, 5, 1, alignment=Qt.AlignmentFlag.AlignCenter)

            self.address_label = QLabel("Address")
            self.address_input = QLineEdit()
            self.address_input.setPlaceholderText("Street Address")
            layout.addWidget(self.address_label, 6, 0, alignment=Qt.AlignmentFlag.AlignLeft)
            layout.addWidget(self.address_input, 6, 1, alignment=Qt.AlignmentFlag.AlignCenter)

            self.create_button = QPushButton("Create New Patient", self)
            self.create_button.setEnabled(False)
            self.phn_input.textChanged.connect(self.check_text)
            layout.addWidget(self.create_button, 7, 1, alignment=Qt.AlignmentFlag.AlignCenter)

            self.setLayout(layout)

            self.create_button.clicked.connect(self.clicked_create)
        
        def check_text(self):
            """
            checks whether anything was entered in the phn box, if yes, enables the create button
            """
            if self.phn_input.text():
                self.create_button.setEnabled(True)
                self.create_button.setDefault(False)

            else:
                self.create_button.setEnabled(False)

        def clicked_create(self):
            """
            attempts to create the new patient, if successful the window will close
            """
            phn = int(self.phn_input.text())
            name = self.name_input.text()
            bday = self.bday_input.date().toString("yyyy-MM-dd")
            phone = self.phone_input.text()
            email = self.email_input.text()
            address = self.address_input.text()
            try:
                self.controller.create_patient(phn, name, bday, phone, email, address)
                QMessageBox.information(self, "Patient Successfully Created", "Successfully created and added patient to database")
                self.close()
            except IllegalOperationException:
                QMessageBox.warning(self, "Failed to create patient",f" A patient with PHN {phn} already exists")
            
class SearchPatient(QDialog):
        """
        a window that allows the user to search through all patients for a patient with a corresponding phn to a given phn
        """
        def __init__(self, controller):
            """
            sets up the pop up window to allow the user to type a phn and search for a patient with corresponding phn
            """
            super().__init__()
            self.setModal(True)
            self.controller = controller
            self.layout = QGridLayout()
            self.setStyleSheet('''
                QWidget{
                    background-color: #ffe6f2;
                    color: black;
                }
                QLabel {
                    background-color: transparent;
                }
                QLineEdit{
                    background-color: white; 
                }
                QPushButton{
                    background-color: white; 
                }
            ''')
            self.setWindowTitle("Search Patient")
            self.setMinimumSize(QSize(500, 300))

            self.header = QLabel("Enter patient's PHN: ")
            self.layout.addWidget(self.header, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter)
            self.search_phn = QLineEdit()
            self.search_phn.setValidator(QIntValidator())
            self.search_phn.setPlaceholderText("PHN")
            self.layout.addWidget(self.search_phn, 0, 1, alignment=Qt.AlignmentFlag.AlignCenter)
            
            self.search_button = QPushButton("Search", self)
            self.search_button.setEnabled(False)
            self.search_phn.textChanged.connect(self.check_text)
            self.layout.addWidget(self.search_button, 0, 2, alignment=Qt.AlignmentFlag.AlignCenter)

            self.done_button = QPushButton("Done")
            self.layout.addWidget(self.done_button, 8, 1, alignment=Qt.AlignmentFlag.AlignCenter)

            self.setLayout(self.layout)
            self.search_button.clicked.connect(self.clicked_search)
            self.done_button.clicked.connect(self.clicked_done)

            self.search_widgets = []

        def check_text(self):
            """
            checks whether a number was entered in the phn box, if yes, enables the search button
            """
            if self.search_phn.text():
                self.search_button.setEnabled(True)
            else:
                self.search_button.setEnabled(False)

        def clicked_search(self):
            """
            behaviour to occur once the search button is pressed - if the patient is found, its details are displayed
            """
            for widget in self.search_widgets:
                widget.deleteLater()

            self.search_widgets.clear()

            phn = int(self.search_phn.text())
            patient = self.controller.search_patient(phn)
            if patient:
                self.found_header = QLabel(f"Patient {patient.phn} found:")
                self.layout.addWidget(self.found_header, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)
                self.search_widgets.append(self.found_header)

                self.phn = QLabel(f"PHN: {patient.phn}")
                self.layout.addWidget(self.phn, 2, 1, alignment=Qt.AlignmentFlag.AlignLeft)
                self.search_widgets.append(self.phn)

                self.name = QLabel(f"Name: {patient.name}")
                self.layout.addWidget(self.name, 3, 1, alignment=Qt.AlignmentFlag.AlignLeft)
                self.search_widgets.append(self.name)

                self.bday = QLabel(f"Birth date:  {patient.birth_date}")
                self.layout.addWidget(self.bday, 4, 1, alignment=Qt.AlignmentFlag.AlignLeft)
                self.search_widgets.append(self.bday)

                self.phone = QLabel(f"Phone: {patient.phone}")
                self.layout.addWidget(self.phone, 5, 1, alignment=Qt.AlignmentFlag.AlignLeft)
                self.search_widgets.append(self.phone)

                self.email = QLabel(f"Email: {patient.email}")
                self.layout.addWidget(self.email, 6, 1, alignment=Qt.AlignmentFlag.AlignLeft)
                self.search_widgets.append(self.email)

                self.address = QLabel(f"Address: {patient.address}")
                self.layout.addWidget(self.address, 7, 1, alignment=Qt.AlignmentFlag.AlignLeft)
                self.search_widgets.append(self.address)
                self.search_phn.clear()


            else:
                self.found_header = QLabel("No patient found")
                self.layout.addWidget(self.found_header, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
                self.search_widgets.append(self.found_header)
                self.search_phn.clear()
   
        def clicked_done(self):
            """
            allows the user to exit the window
            """
            self.close()
             
class UpdatePatient(QDialog):
    """
    a window that allows the user to update a certain patient
    """
    def __init__(self, controller):
            """
            sets up the pop up window to allow the user to search for a patient to update
            """
            super().__init__()
            self.controller = controller
            self.setModal(True)
            self.layout = QGridLayout()
            self.setStyleSheet('''
                QWidget{
                    background-color: #ffe6f2;
                    color: black;
                }
                QLabel{
                    background-color: transparent;
                }
                QLineEdit{
                    background-color: white; 
                }
                QPushButton{
                    background-color: white; 
                }
                QDateEdit{
                    background-color: white;
                }
            ''')
            self.setWindowTitle("Update Patient")
            self.setMinimumSize(QSize(500, 300))

            self.header = QLabel("Enter patient's PHN: ")
            self.layout.addWidget(self.header, 0, 0, alignment=Qt.AlignmentFlag.AlignLeft)
            self.search_phn = QLineEdit()
            self.search_phn.setValidator(QIntValidator())
            self.search_phn.setPlaceholderText("PHN")
            self.layout.addWidget(self.search_phn, 0, 1, alignment=Qt.AlignmentFlag.AlignLeft)
            
            self.search_button = QPushButton("Search", self)
            self.search_button.setEnabled(False)
            self.search_phn.textChanged.connect(self.check_text)
            self.layout.addWidget(self.search_button, 0, 2, alignment=Qt.AlignmentFlag.AlignLeft)

            self.setLayout(self.layout)
            self.search_button.clicked.connect(self.clicked_search)
            self.search_widgets = []

    def check_text(self):
            """
            checks whether a number was entered in the phn box, if yes, enables the search button
            """
            if self.search_phn.text():
                self.search_button.setEnabled(True)
            else:
                self.search_button.setEnabled(False)

    def clicked_search(self):
        """
        behaviour to occur once the search button is pressed - if the phn is valid, an editable version of the patient and an update button are shown
        """
        for widget in self.search_widgets:
            widget.deleteLater()

        self.search_widgets.clear()

        self.phn1 = int(self.search_phn.text())
        self.patient = self.controller.search_patient(self.phn1)

        if self.patient:
            self.found_header = QLabel(f"Edit patient {self.patient.phn}'s data")
            self.layout.addWidget(self.found_header, 1, 0, alignment=Qt.AlignmentFlag.AlignLeft)
            self.search_widgets.append(self.found_header)

            self.phn2_label = QLabel("Personal Health Number (PHN):")
            self.phn2_input = QLineEdit(str(self.patient.phn))
            self.phn2_input.setPlaceholderText("PHN")
            self.phn2_input.setValidator(QIntValidator())
            self.layout.addWidget(self.phn2_label, 2, 0, alignment=Qt.AlignmentFlag.AlignLeft)
            self.layout.addWidget(self.phn2_input, 2, 1, alignment=Qt.AlignmentFlag.AlignLeft)
            self.search_widgets.append(self.phn2_label)
            self.search_widgets.append(self.phn2_input)

            self.name_label = QLabel("Full Name:")
            self.name_input = QLineEdit(self.patient.name)
            self.name_input.setPlaceholderText("First Last")
            self.layout.addWidget(self.name_label, 3, 0, alignment=Qt.AlignmentFlag.AlignLeft)
            self.layout.addWidget(self.name_input, 3, 1, alignment=Qt.AlignmentFlag.AlignLeft)
            self.search_widgets.append(self.name_label)
            self.search_widgets.append(self.name_input)

            self.bday_label = QLabel("Birthdate (YYYY-MM-DD):")
            self.bday_input = QDateEdit()
            self.bday_input.setFixedSize(140, 25)
            self.bday_input.setDate(QDate.currentDate())
            self.bday_input.setDisplayFormat("yyyy-MM-dd")
            self.layout.addWidget(self.bday_label, 4, 0, alignment=Qt.AlignmentFlag.AlignLeft)
            self.layout.addWidget(self.bday_input, 4, 1, alignment=Qt.AlignmentFlag.AlignLeft)
            self.search_widgets.append(self.bday_label)
            self.search_widgets.append(self.bday_input)

            self.phone_label = QLabel("Phone:")
            self.phone_input = QLineEdit(self.patient.phone)
            self.phone_input.setPlaceholderText("Phone Number")
            self.phone_input.setValidator(QIntValidator())
            self.layout.addWidget(self.phone_label, 5, 0, alignment=Qt.AlignmentFlag.AlignLeft)
            self.layout.addWidget(self.phone_input, 5, 1, alignment=Qt.AlignmentFlag.AlignLeft)
            self.search_widgets.append(self.phone_label)
            self.search_widgets.append(self.phone_input)

            self.email_label = QLabel("Email:")
            self.email_input = QLineEdit(self.patient.email)
            self.email_input.setPlaceholderText("Email Address")
            self.layout.addWidget(self.email_label, 6, 0, alignment=Qt.AlignmentFlag.AlignLeft)
            self.layout.addWidget(self.email_input, 6, 1, alignment=Qt.AlignmentFlag.AlignLeft)
            self.search_widgets.append(self.email_label)
            self.search_widgets.append(self.email_input)

            self.address_label = QLabel("Address:")
            self.address_input = QLineEdit(self.patient.address)
            self.address_input.setPlaceholderText("Street Address")
            self.layout.addWidget(self.address_label, 7, 0, alignment=Qt.AlignmentFlag.AlignLeft)
            self.layout.addWidget(self.address_input, 7, 1, alignment=Qt.AlignmentFlag.AlignLeft)
            self.search_widgets.append(self.address_label)
            self.search_widgets.append(self.address_input)

            self.update_button = QPushButton("Update", self)
            self.update_button.setEnabled(True)
            self.phn2_input.textChanged.connect(self.check_text_update)
            self.layout.addWidget(self.update_button, 8, 2, alignment=Qt.AlignmentFlag.AlignLeft)
            self.search_widgets.append(self.update_button)
            self.update_button.clicked.connect(self.clicked_update)
            self.search_phn.clear()

        else:
            self.found_header = QLabel("No patient found")
            self.layout.addWidget(self.found_header, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
            self.search_widgets.append(self.found_header)
            self.search_phn.clear()

    def check_text_update(self):
        """
        checks if the phn input holds text, if yes, enables the update button
        """
        if self.phn2_input.text():
            self.update_button.setEnabled(True)
        else:
            self.update_button.setEnabled(False)

    def clicked_update(self):
        """
        attempts to update the patient with the edited fields, closes window if successful
        """
        try:
            reply = QMessageBox.question(None, "Confirmation", f"Are you sure you want to update patient {self.patient.phn}?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,  QMessageBox.StandardButton.Yes)
            if reply == QMessageBox.StandardButton.Yes:
                self.controller.update_patient(self.phn1, int(self.phn2_input.text()), self.name_input.text(), self.bday_input.date().toString("yyyy-MM-dd"), self.phone_input.text(), self.email_input.text(), self.address_input.text())
                QMessageBox.information(self, "Patient Updated", "Patient's data has been successfully updated")
                self.close()
        except IllegalOperationException:
            QMessageBox.warning(self, "Pre-existing PHN", f"The PHN {self.phn2_input.text()} already belongs to an existing patient")
            self.phn2_input.clear()
             
class RetrievePatient(QDialog):
        """
        a window that allows the user to search through all patients for any that contain a certain keyword in their name
        """
        def __init__(self, controller):
            """
            sets up the pop up window to allow the user to type a keyword and search for patients name containing it
            """
            super().__init__()
            self.controller = controller
            self.setModal(True)
            self.layout = QGridLayout()
            self.setStyleSheet('''
                QWidget{
                    background-color: #ffe6f2;
                    color: black;
                }
                QLabel {
                    background-color: transparent;
                }
                QLineEdit{
                    background-color: white; 
                }
                QPushButton{
                    background-color: white; 
                }
                QTableView{
                    background-color: white;  
                }
            ''')
            self.setWindowTitle("Retrieve Patient")
            self.setMinimumSize(QSize(800, 500))

            self.header = QLabel("Enter name to search: ")
            self.layout.addWidget(self.header, 0, 0, alignment=Qt.AlignmentFlag.AlignRight)
            self.layout.setRowStretch(1, 5)
            self.search_name = QLineEdit()
            self.search_name.setValidator(QRegularExpressionValidator(QRegularExpression("[A-Za-z.:\"/!@#$%^&*(),?<>]+"), self.search_name))
            self.layout.addWidget(self.search_name, 0, 1, alignment=Qt.AlignmentFlag.AlignCenter)
            self.search_button = QPushButton("Search")
            self.layout.addWidget(self.search_button, 0, 2, alignment=Qt.AlignmentFlag.AlignLeft)

            self.done_button = QPushButton("Done")
            self.layout.addWidget(self.done_button, 2, 1, alignment=Qt.AlignmentFlag.AlignCenter)
            self.layout.setColumnStretch(0, 2)
            self.layout.setColumnStretch(2, 2)

            self.setLayout(self.layout)
            self.search_button.clicked.connect(self.clicked_search)
            self.done_button.clicked.connect(self.clicked_done)
            self.table_widgets = []
            
        def clicked_search(self):
            """
            behaviour to occur once the search button is pressed - any patients with names containing the keyword are displayed
            """
            for widget in self.table_widgets:
                widget.deleteLater()

            self.table_widgets.clear()

            patients_list = self.controller.retrieve_patients(self.search_name.text())
            self.patient_table = QTableView(self)
            self.patient_table.resizeColumnsToContents()
            header = self.patient_table.horizontalHeader()
            header.setMinimumSectionSize(100)
            
            self.patient_table.setMinimumSize(650, 350)
            
            if patients_list:
                self.model = self.create_patients_model(patients_list)
                self.patient_table.setModel(self.model)
                self.layout.addWidget(self.patient_table, 1, 0, 1, 3, alignment=Qt.AlignmentFlag.AlignCenter) 
                self.patient_table.resizeColumnsToContents()
                self.table_widgets.append(self.patient_table)      

            else:
                self.found_header = QLabel("No patient found")
                self.patient_table.clearSpans()
                self.layout.addWidget(self.found_header, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
                self.table_widgets.append(self.found_header)

            self.search_name.clear()

        def create_patients_model(self, pat_list):
            """
            creates and return a ProductTableModel object to display the retrieved patients
            """
            model = ProductTableModel(self.controller, pat_list)
            return model

        def clicked_done(self):
            """
            allows user to exit the window
            """
            self.close()

class ProductTableModel(QAbstractTableModel):
    """
    A table model class for displaying patients
    """
    def __init__(self, controller, patient_list):
        """
        initializes the model
        """
        super().__init__()
        self.controller = controller
        self.patient_list = patient_list
        self._data = []
        self.refresh_data()

    def refresh_data(self):
        """
        refreshes the data from patient list
        """
        self._data = []
        
        for patient in self.patient_list:
            fields = list(patient.__dict__.values())
            fields = fields[:6]
            self._data.append(fields)  
        
        self.layoutChanged.emit()

    def reset(self):
        """
        resets the data
        """
        self._data = []
        self.layoutChanged.emit()

    def data(self, index, role):
        """
        returns the data for the given index and role
        """
        value = self._data[index.row()][index.column()]

        if role == Qt.ItemDataRole.DisplayRole:
            if isinstance(value, float):
                return "%.2f" % value
            if isinstance(value, str):
                return '%s' % value
            return value

        if role == Qt.ItemDataRole.TextAlignmentRole:
            if isinstance(value, int) or isinstance(value, float):
                return Qt.AlignmentFlag.AlignVCenter + Qt.AlignmentFlag.AlignRight

    def rowCount(self, index):
        """
        returns the number of rows in the model
        """
        return len(self._data)

    def columnCount(self, index):
        """
        returns the number of columns in the model
        """
        if self._data:
            return len(self._data[0])
        else:
            return 0

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        """
        returns the header data for the given section and orientation
        """
        headers = ['PHN', 'Patient Name', 'Birth Date', 'Phone Number', 'Email', 'Address']
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return '%s' % headers[section]
        return super().headerData(section, orientation, role)
                 
class RemovePatient(QDialog):
        """
        a window that allows the user to remove a certain paitent from the database
        """
        def __init__(self, controller):
            """
            sets up the pop up window to allow the user to search for a patient to remove
            """
            super().__init__()
            self.controller = controller
            self.setModal(True)
            self.layout = QGridLayout()
            self.setStyleSheet('''
                QWidget{
                    background-color: #ffe6f2;
                    color: black;
                }
                QLabel {
                    background-color: transparent;
                }
                QLineEdit, QPushButtone{
                    background-color: white; 
                }
                QPushButton{
                    background-color: white; 
                }
            ''')
            self.setWindowTitle("Remove Patient")
            self.setMinimumSize(QSize(500, 300))

            self.header = QLabel("Enter patient's PHN:")
            self.layout.addWidget(self.header, 0, 0, alignment=Qt.AlignmentFlag.AlignRight)
            self.search_phn = QLineEdit()
            self.search_phn.setValidator(QIntValidator())
            self.search_phn.setPlaceholderText("PHN")
            self.layout.addWidget(self.search_phn, 0, 1, alignment=Qt.AlignmentFlag.AlignCenter)
            self.search_button = QPushButton("Search", self)
            self.search_button.setEnabled(False)
            self.search_phn.textChanged.connect(self.check_text)
            self.layout.addWidget(self.search_button, 0, 2, alignment=Qt.AlignmentFlag.AlignLeft)

            self.setLayout(self.layout)
            self.search_button.clicked.connect(self.clicked_search)

            self.search_widgets = []

        def check_text(self):
            """
            checks if a phn number is inputed, if yes, enables the search button
            """
            if self.search_phn.text():
                self.search_button.setEnabled(True)
            else:
                self.search_button.setEnabled(False)

        def clicked_search(self):
            """
            if the phn is valid, the patient displayed on the screen and the user is given access to a delete button 
            """
            for widget in self.search_widgets:
                widget.deleteLater()

            self.search_widgets.clear()

            phn = int(self.search_phn.text())
            self.patient = self.controller.search_patient(phn)
            if self.patient:
                self.found_header = QLabel(f"Patient {self.patient.phn} found:")
                self.layout.addWidget(self.found_header, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)
                self.search_widgets.append(self.found_header)

                self.phn = QLabel(f"PHN: {self.patient.phn}")
                self.layout.addWidget(self.phn, 2, 1, alignment=Qt.AlignmentFlag.AlignLeft)
                self.search_widgets.append(self.phn)

                self.name = QLabel(f"Name: {self.patient.name}")
                self.layout.addWidget(self.name, 3, 1, alignment=Qt.AlignmentFlag.AlignLeft)
                self.search_widgets.append(self.name)

                self.bday = QLabel(f"Birth date:  {self.patient.birth_date}")
                self.layout.addWidget(self.bday, 4, 1, alignment=Qt.AlignmentFlag.AlignLeft)
                self.search_widgets.append(self.bday)

                self.phone = QLabel(f"Phone: {self.patient.phone}")
                self.layout.addWidget(self.phone, 5, 1, alignment=Qt.AlignmentFlag.AlignLeft)
                self.search_widgets.append(self.phone)

                self.email = QLabel(f"Email: {self.patient.email}")
                self.layout.addWidget(self.email, 6, 1, alignment=Qt.AlignmentFlag.AlignLeft)
                self.search_widgets.append(self.email)

                self.address = QLabel(f"Address: {self.patient.address}")
                self.layout.addWidget(self.address, 7, 1, alignment=Qt.AlignmentFlag.AlignLeft)
                self.search_widgets.append(self.address)

                self.delete_button = QPushButton("Delete", self)
                self.layout.addWidget(self.delete_button, 8, 1, alignment=Qt.AlignmentFlag.AlignCenter)
                self.search_widgets.append(self.delete_button)
                self.delete_button.clicked.connect(self.clicked_delete)

            else:
                QMessageBox.information(self, "Invalid PHN", f"Patient with PHN {phn} does not exist")
                
            self.search_phn.clear()

        def clicked_delete(self):
            """
            confirms that the user wants to delete the given patient and, if yes, removes the patient
            """
            reply = QMessageBox.question(None, "Confirmation", f"Are you sure you want to delete patient {self.patient.phn}?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,  QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                self.controller.delete_patient(self.patient.phn)
                QMessageBox.information(self, "Deletion Successful", f"Successfully removed patient {self.patient.phn}")
                self.close()

class ListPatient(QDialog):
        """
        a window that allows the user to list all patients that exist
        """
        def __init__(self, controller):
            """
            sets up the pop up window and displays all patients in a QTableView widget
            """
            super().__init__()
            self.controller = controller
            self.setModal(True)
            self.layout = QGridLayout()
            self.setStyleSheet('''
                QWidget{
                    background-color: #ffe6f2;
                    color: black;
                }
                QTableView{
                    background-color: white; 
                }
                QPushButton{
                    background-color: white;
                }
            ''')
            self.setWindowTitle("List Patients")
            self.setMinimumSize(QSize(800, 500))

            
            self.done_button = QPushButton("Done")
            self.layout.addWidget(self.done_button, 4, 2, alignment=Qt.AlignmentFlag.AlignCenter)
            self.layout.setRowStretch(3, 3)

            self.setLayout(self.layout)
            self.done_button.clicked.connect(self.clicked_done)
            
            patients_list = self.controller.list_patients()
            self.patient_table = QTableView(self)
            
            self.patient_table.setMinimumSize(650, 350)
            
            if patients_list:
                self.title = QLabel("All Patients")
                font = QFont("Helvetica", 15)
                self.title.setFont(font)
                self.layout.addWidget(self.title, 0, 2, alignment=Qt.AlignmentFlag.AlignCenter)

                self.model = self.create_patients_model(patients_list)
                self.patient_table.setModel(self.model)
                self.layout.addWidget(self.patient_table, 1, 1, 1, 3, alignment=Qt.AlignmentFlag.AlignCenter) 
                self.patient_table.resizeColumnsToContents()
                header = self.patient_table.horizontalHeader()
                header.setMinimumSectionSize(100)

            else:
                self.patient_table.hide()
                self.found_header = QLabel("  No patients to list")
                self.layout.addWidget(self.found_header, 3, 2, alignment=Qt.AlignmentFlag.AlignCenter)
     

        def create_patients_model(self, pat_list):
            """
            creates and return a ProductTableModel object to display the retrieved patients
            """
            model = ProductTableModel(self.controller, pat_list)
            return model
        
        def clicked_done(self):
            """
            allows users to close the window
            """
            self.close()

class Appointment(QDialog):
        """
        a window that allows the user to start an appointment with a certain patient
        """
        def __init__(self, controller, main_window):
            """
            sets up the pop up window to allow the user to search for a patient to start an appointment with
            """
            super().__init__()
            self.controller = controller
            self.setModal(True)
            self.main = main_window
            self.layout = QGridLayout()
            self.setStyleSheet('''
                QWidget{
                    background-color: #ffe6f2;
                    color: black;
                }
                QLabel {
                    background-color: transparent;
                }
                QLineEdit, QPushButtone{
                    background-color: white; 
                }
                QPushButton{
                    background-color: white; 
                }
            ''')
            self.setWindowTitle("Start appointment")
            self.setMinimumSize(QSize(500, 300))

            self.header = QLabel("Enter patient's PHN:")
            self.layout.addWidget(self.header, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter)
            self.search_phn = QLineEdit()
            self.search_phn.setValidator(QIntValidator())
            self.search_phn.setPlaceholderText("PHN")
            self.layout.addWidget(self.search_phn, 0, 1, alignment=Qt.AlignmentFlag.AlignCenter)
            
            self.search_button = QPushButton("Start appointment", self)
            self.search_button.setEnabled(False)
            self.search_phn.textChanged.connect(self.check_text)
            self.layout.addWidget(self.search_button, 0, 2, alignment=Qt.AlignmentFlag.AlignCenter)

            self.setLayout(self.layout)
            self.search_button.clicked.connect(self.clicked_search)

            self.search_widgets = []

        def check_text(self):
            """
            checks whether a number was entered in the phn box, if yes, enables the search button
            """
            if self.search_phn.text():
                self.search_button.setEnabled(True)
            else:
                self.search_button.setEnabled(False)

        def clicked_search(self):
            """
            behaviour to occur once the search button is pressed - if the phn is valid, opens the appointment window and closes this window
            """
            for widget in self.search_widgets:
                widget.deleteLater()

            self.search_widgets.clear()

            phn = self.search_phn.text()
  
            try:
                self.controller.set_current_patient(int(phn))
                self.appointment_window = AppointmentGUI(self.controller, self.main)
                self.appointment_window.show()
                self.close()

            except IllegalOperationException:
                QMessageBox.information(self, "Invalid PHN", f"Patient with PHN {phn} does not exist")
                self.search_phn.clear()