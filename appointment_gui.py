from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIntValidator
from PyQt6.QtWidgets import QDialog, QMainWindow, QGridLayout, QPushButton, QWidget, QSizePolicy, QLabel, QLineEdit, QMessageBox, QPlainTextEdit
from clinic.controller import Controller

class AppointmentGUI(QMainWindow):
    def __init__(self, controller, main_window):
        """ 
        creates an appointment window which contains button widgets that allow the user to manipulate the current patient's patient record and notes
        """
        super().__init__()
        self.controller = controller
        self.main = main_window
        self.current_patient = self.controller.get_current_patient()

        self.main.setDisabled(True)

        central_widget = QWidget()
        layout = QGridLayout()
        self.setStyleSheet('''
            QWidget{
                background-color: #ffe6f2; 
                color: black;
            }
            QLabel{
                background-color: transparent;
            }
            QPushButton{
                background-color: white;   
            }
            
        ''')
        self.setWindowTitle("Appointment")
        title = QLabel(f"Appointment with patient {self.current_patient.get_phn()}")
        font = QFont("Helvetica", 22)
        title.setFont(font)
        layout.addWidget(title, 0, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setMinimumSize(QSize(800, 500))
        
        """
        creating all of the appointment home window buttons
        """
        self.button_create_note = QPushButton("Add note to patient record")
        self.button_retrieve_notes = QPushButton("Retrieve notes from patient record by text")
        self.button_update_note = QPushButton("Update note from patient record")
        self.button_remove_note = QPushButton("Remove note from patient record")
        self.button_list_notes = QPushButton("List full patient record")
        self.button_finish_app = QPushButton("Finish appointment")

        buttons = [self.button_create_note, self.button_retrieve_notes, self.button_update_note, self.button_remove_note, self.button_list_notes, self.button_finish_app]

        """
        setting up button size and alignment in window
        """
        for button, i in zip(buttons, range(1, 7)):
            button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            button.setFixedSize(300, 30)
            layout.addWidget(button, i, 1,  alignment=Qt.AlignmentFlag.AlignCenter)
        
        for i in range(0, 7):
            layout.setRowStretch(i, 1)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
        self.button_create_note.clicked.connect(lambda: self.create_dialog(1))
        self.button_retrieve_notes.clicked.connect(lambda: self.create_dialog(2))
        self.button_update_note.clicked.connect(lambda: self.create_dialog(3))
        self.button_remove_note.clicked.connect(lambda: self.create_dialog(4))
        self.button_list_notes.clicked.connect(lambda: self.create_dialog(5))
        self.button_finish_app.clicked.connect(self.finish_app)

    def closeEvent(self, event):
        """
        enables the clinic home window after the appointment menu window is closed
        """
        self.main.setDisabled(False)
        event.accept()

    def create_dialog(self, number):
        """
        creates correct window based off of which button was pushed using a numeric code associated with a certain user story
        """
        if number == 1:
            self.create_note_window = CreateNote(self.controller, self.current_patient)
            self.create_note_window.show()
        elif number == 2:
            self.retrieve_note_window = RetrieveNote(self.controller, self.current_patient)
            self.retrieve_note_window.show()
        elif number == 3:
            self.update_note_window = UpdateNote(self.controller)
            self.update_note_window.show()
        elif number == 4:
            self.remove_note_window = RemoveNote(self.controller)
            self.remove_note_window.show()
        elif number == 5:
            self.list_notes_window = ListNotes(self.controller)
            self.list_notes_window.show()

    def finish_app(self):
        """
        confirms user wants to close window and if yes, exits the appointment and returns to the clinic's home menu
        """
        reply = QMessageBox.question(None, "Confirmation", "Are you sure you want to finish this appointment?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,  QMessageBox.StandardButton.Yes)
        if reply == QMessageBox.StandardButton.Yes:
            self.controller.unset_current_patient()
            self.close()
            self.main.show()

class CreateNote(QDialog):
    """
    a window that allows the user to new create notes for the current patient
    """
    def __init__(self, controller, current_patient):
        """
        sets up the pop up window to allow the user to type a new note in a note box
        """
        super().__init__()
        self.setModal(True)
        self.controller = controller
        self.current_patient = current_patient
        self.setStyleSheet('''
            QDialog{
                background-color: #ffe6f2;                   
            }
            QWidget{
                color: black;
            }
            QLabel{
                background-color: transparent;
            }
            QPushButton{
                background-color: white;   
            }
            QPlainTextEdit{
                background-color: white;               
            }
        ''')

        self.layout = QGridLayout()
        self.setWindowTitle("Create New Note")
        self.setMinimumSize(QSize(650, 400))
        self.header = QLabel(f"Enter appointment note:")
        self.layout.addWidget(self.header, 0, 0, alignment=Qt.AlignmentFlag.AlignLeft)

        self.note_box = QPlainTextEdit()
        self.note_box.setMinimumSize(600, 350)
        self.layout.addWidget(self.note_box, 1, 0, 1, 3, alignment=Qt.AlignmentFlag.AlignCenter)

        self.add_button = QPushButton("Add", self)
        self.add_button.setEnabled(False)
        self.note_box.textChanged.connect(self.check_text)
        self.layout.addWidget(self.add_button, 3, 1, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(self.layout)

        self.add_button.clicked.connect(self.clicked_add)

    def check_text(self):
        """
        checks whether anything was entered in the note box, if yes, enables the add button
        """
        if self.note_box.toPlainText().strip():
            self.add_button.setEnabled(True)
        else:
            self.add_button.setEnabled(False)

    def clicked_add(self):
        """
        adds a new note to the current patient's patient record and closes the window
        """
        note = self.note_box.toPlainText()
        self.controller.create_note(note)
        QMessageBox.information(self, "Note added", "New patient note has been successfully created")
        self.note_box.clear()
        self.close()

class RetrieveNote(QDialog):
    """
    a window that allows the user to search through the current patient's notes for any that contain a certain keyword
    """
    
    def __init__(self, controller, current_patient):
        """
        sets up the pop up window to allow the user to type a keyword and search for notes containing it
        """
        super().__init__()
        self.controller = controller
        self.setModal(True)
        self.current_patient = current_patient
        self.setStyleSheet('''
            QDialog{
                background-color: #ffe6f2; 
            }
            QWidget{
                color: black;           
            }
            QLabel{
                background-color: transparent;
            }
            QPushButton{
                background-color: white;   
            }
            QLineEdit{
                background-color: white;   
            }
            QPlainTextEdit{
                background-color: white;
            }
        ''')

        self.layout = QGridLayout()
        self.setWindowTitle("Retrieve notes")
        self.setMinimumSize(QSize(650, 400))
        self.header = QLabel("Search keyword:")
        self.layout.addWidget(self.header, 0, 0, alignment=Qt.AlignmentFlag.AlignRight)

        self.keyword_input = QLineEdit()
        self.layout.addWidget(self.keyword_input, 0, 1, alignment=Qt.AlignmentFlag.AlignCenter)

        self.search_button = QPushButton("Search")
        self.layout.addWidget(self.search_button, 0, 2, alignment=Qt.AlignmentFlag.AlignLeft)

        self.done_button = QPushButton("Done")
        self.layout.addWidget(self.done_button, 2, 1, alignment=Qt.AlignmentFlag.AlignBottom)
        self.setLayout(self.layout)

        self.search_button.clicked.connect(self.clicked_search)
        self.done_button.clicked.connect(self.clicked_done)
        self.search_widgets = []

    def clicked_search(self):
        """
        behaviour to occur once the search button is pressed - any notes containing the keyword are displayed
        """
        for widget in self.search_widgets:
            widget.deleteLater()

        self.search_widgets.clear()
        keyword = self.keyword_input.text()
        
        self.note_box = QPlainTextEdit()
        self.note_box.setMinimumSize(600, 275)
        self.layout.addWidget(self.note_box, 1, 0, 1, 3, alignment=Qt.AlignmentFlag.AlignCenter)
        self.search_widgets.append(self.note_box)
        notes = self.controller.retrieve_notes(keyword)
        if len(notes) != 0:
            for note in notes:
                self.note_box.insertPlainText(note.__str__() + "\n")
        else:
            self.note_box.insertPlainText(f"No note(s) with keyword \"{keyword}\" found")

        self.note_box.setReadOnly(True)
        self.keyword_input.clear()
    
    def clicked_done(self):
        """
        allows user to exit the window
        """
        self.close()

class UpdateNote(QDialog):
    """
    a window that allows the user to update a certain note in the current patient's record
    """
    def __init__(self, controller):
        """
        sets up the pop up window to allow the user to search for a note to update
        """
        super().__init__()
        self.setModal(True)
        self.controller = controller
        self.setStyleSheet('''
            QDialog{
                background-color: #ffe6f2; 
            }
            QWidget{
                color: black;
            }
            QLabel{
                background-color: transparent;
            }
            QPushButton{
                background-color: white;   
            }
            QLineEdit{
                background-color: white;
            }
            QPlainTextEdit{
                background-color: white;
            }
        ''')
        self.layout = QGridLayout()
        self.setWindowTitle("Update Note")
        self.setMinimumSize(QSize(650, 400))

        self.header = QLabel(f"Note to change:")
        self.layout.addWidget(self.header, 0, 0, alignment=Qt.AlignmentFlag.AlignRight)

        self.keyword_input = QLineEdit()
        self.keyword_input.setPlaceholderText("Note Number")
        self.keyword_input.setValidator(QIntValidator())
        self.layout.addWidget(self.keyword_input, 0, 1, alignment=Qt.AlignmentFlag.AlignCenter)

        self.find_button = QPushButton("Find", self)
        self.find_button.setEnabled(False)
        self.keyword_input.textChanged.connect(self.check_text)
        self.layout.addWidget(self.find_button, 0, 2, alignment=Qt.AlignmentFlag.AlignLeft)
          
        self.setLayout(self.layout)
        
        self.find_button.clicked.connect(self.clicked_find)

        self.find_widgets = []
    
    def check_text(self):
        """
        checks whether a number was entered in the note box, if yes, enables the find button
        """
        if self.keyword_input.text():
            self.find_button.setEnabled(True)
        else:
            self.find_button.setEnabled(False)

    def clicked_find(self):
        """
        behaviour to occur once the find button is pressed - if the note is valid, an editable version of the note and an update button are shown
        """
        note_num = self.keyword_input.text()

        for widget in self.find_widgets:
                widget.deleteLater()

        self.find_widgets.clear()

        if not self.controller.search_note(int(note_num)):
            QMessageBox.information(self, "Invalid Note", f"Note {note_num} does not exist")
            self.keyword_input.clear()
        else:
            note_num = int(note_num)
            note_to_edit = self.controller.search_note(note_num)

            self.update_button = QPushButton("Update", self)
            self.layout.addWidget(self.update_button, 3, 1, alignment=Qt.AlignmentFlag.AlignCenter)
            self.update_button.setEnabled(False)

            self.note_title = QLabel(f"Note {note_num}:")
            self.layout.addWidget(self.note_title, 1, 0, alignment=Qt.AlignmentFlag.AlignLeft)
            self.find_widgets.append(self.note_title)

            self.note_box = QPlainTextEdit()
            self.note_box.textChanged.connect(self.text_change)
            self.note_box.setMinimumSize(600, 275)
            self.layout.setRowStretch(2, 2)
            self.layout.addWidget(self.note_box, 2, 0, 1, 3, alignment=Qt.AlignmentFlag.AlignTop)
            self.find_widgets.append(self.note_box)
            
            self.note_box.textChanged.disconnect(self.text_change)
            self.note_box.insertPlainText(note_to_edit.__str__()[7+len(str(note_num)):])
            self.note_box.textChanged.connect(self.text_change)
            
            self.update_button.clicked.connect(lambda: self.clicked_update(note_num))

            self.keyword_input.clear()

    def text_change(self):
        """
        checks if the note is changed, if yes, enables the update button
        """
        if self.note_box.toPlainText().strip():
            self.update_button.setEnabled(True)
        else:
            self.update_button.setEnabled(False)

    def clicked_update(self, note_num):
        """
        updates the current patient's patient record with the edited note
        """
        updated_text = self.note_box.toPlainText()
        self.controller.update_note(note_num, updated_text)
        QMessageBox.information(self, "Update Complete", f"Note {note_num} has been updated")
        self.close()

class RemoveNote(QDialog):
    """
    a window that allows the user to remove a certain note in the current patient's record
    """
    def __init__(self, controller):
        """
        sets up the pop up window to allow the user to search for a note to remove
        """
        super().__init__()
        self.controller = controller
        self.setModal(True)
        self.setStyleSheet('''
            QDialog{
                background-color: #ffe6f2; 
            }
            QWidget{
                color: black;           
            }
            QLabel{
                background-color: transparent;
            }
            QPushButton{
                background-color: white;   
            }
            QLineEdit{
                background-color: white;   
            }
            QPlainTextEdit{
                background-color: white;
            }
        ''')
        self.layout = QGridLayout()
        self.setWindowTitle("Remove Note")
        self.setMinimumSize(QSize(650, 400))
        self.header = QLabel(f"Note to delete:")
        self.layout.addWidget(self.header, 0, 0, alignment=Qt.AlignmentFlag.AlignRight)

        self.keyword_input = QLineEdit()
        self.keyword_input.setValidator(QIntValidator())
        self.keyword_input.setPlaceholderText("Note Number")
        self.layout.addWidget(self.keyword_input, 0, 1, alignment=Qt.AlignmentFlag.AlignCenter)

        self.find_button = QPushButton("Find", self)
        self.find_button.setEnabled(False)
        self.keyword_input.textChanged.connect(self.check_text)
        self.layout.addWidget(self.find_button, 0, 2, alignment=Qt.AlignmentFlag.AlignLeft)

        self.setLayout(self.layout)
        
        self.find_button.clicked.connect(self.clicked_find)

        self.find_widgets = []

    def check_text(self):
        """
        checks if a note number is inputed, if yes, enables the find button
        """
        if self.keyword_input.text():
            self.find_button.setEnabled(True)
        else:
            self.find_button.setEnabled(False)

    def clicked_find(self):
        """
        if the note is valid, it is displayed on the screen and the user is given access to a delete button 
        """
        note_num = self.keyword_input.text()
        self.keyword_input.clear()

        for widget in self.find_widgets:
                widget.deleteLater()

        self.find_widgets.clear()

        if not self.controller.search_note(int(note_num)):
            QMessageBox.information(self, "Invalid Note", f"Note {note_num} does not exist")
            
        else:
            self.delete_button = QPushButton("Delete")
            self.layout.addWidget(self.delete_button, 3, 1, alignment=Qt.AlignmentFlag.AlignCenter)
            self.delete_button.setEnabled(False)
            self.find_widgets.append(self.delete_button)
            
            note_num = int(note_num)
            note_to_edit = self.controller.search_note(note_num)

            self.note_title = QLabel(f"Note {note_num}:")
            self.layout.addWidget(self.note_title, 1, 0, alignment=Qt.AlignmentFlag.AlignLeft)
            self.find_widgets.append(self.note_title)
            
            self.note_box = QPlainTextEdit()
            self.note_box.setMinimumSize(600, 275)
            self.layout.setRowStretch(2, 2)
            self.layout.addWidget(self.note_box, 2, 0, 1, 3, alignment=Qt.AlignmentFlag.AlignTop)
            self.find_widgets.append(self.note_box)
            self.note_box.insertPlainText(note_to_edit.__str__()[6+len(str(note_num)):])
            self.note_box.setReadOnly(True)
            
            self.delete_button.setEnabled(True)
            self.delete_button.clicked.connect(lambda: self.clicked_delete(note_num))

    def clicked_delete(self, note_num):
        """
        confirms that the user wants to delete the given note and, if yes, removes the note from the current patient's patient record
        """
        self.keyword_input.clear()
        reply = QMessageBox.question(None, "Confirmation", f"Are you sure you want to delete note {note_num}?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,  QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.controller.delete_note(note_num)
            QMessageBox.information(self, "Deletion Completed", f"Note {note_num} has been deleted")
            self.close()

class ListNotes(QDialog):
    """
    a window that allows the user to list all notes that exist in the current patient's patient record
    """
    def __init__(self, controller):
        """
        sets up the pop up window and fills a note box with all of the current patient's notes
        """
        super().__init__()
        self.controller = controller
        self.setModal(True)
        self.setStyleSheet('''
            QDialog{
                background-color: #ffe6f2; 
            }
            QWidget{
                color: black;           
            }
            QLabel{
                background-color: transparent;
            }
            QPushButton{
                background-color: white;   
            }
            QPlainTextEdit{
                background-color: white;
            }
        ''')
        self.layout = QGridLayout()
        self.setWindowTitle("List notes")
        self.setMinimumSize(QSize(650, 400))

        self.done_button = QPushButton("Done")
        self.layout.addWidget(self.done_button, 2, 1, alignment=Qt.AlignmentFlag.AlignBottom)
        self.setLayout(self.layout)
  
        self.note_box = QPlainTextEdit()
        self.note_box.setMinimumSize(600, 300)
        self.layout.addWidget(self.note_box, 0, 0, 3, 3, alignment=Qt.AlignmentFlag.AlignTop)

        notes = self.controller.list_notes()
        notes.reverse()
        if len(notes) != 0:
            for note in notes:
                self.note_box.insertPlainText(note.__str__() + "\n")
        else:
            self.note_box.insertPlainText(f"Patient {self.controller.current_patient.get_phn()} has no notes")


        self.note_box.setReadOnly(True)

        self.done_button.clicked.connect(self.clicked_done)
    
    def clicked_done(self):
        """
        closes the pop up window and returns to the appointment home screen
        """
        self.close()

    



       

