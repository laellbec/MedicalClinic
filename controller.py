from .patient import Patient
from .patient_record import PatientRecord
from .note import Note
from .dao.patient_dao_json import PatientDAOJSON
from .exception.invalid_logout_exception import InvalidLogoutException
from .exception.invalid_login_exception import InvalidLoginException
from .exception.duplicate_login_exception import DuplicateLoginException
from .exception.illegal_access_exception import IllegalAccessException
from .exception.illegal_operation_exception import IllegalOperationException
from .exception.no_current_patient_exception import NoCurrentPatientException
import hashlib

class Controller:
        def __init__(self, autosave: bool) -> None:
            """
            initializes attributions of Controller instance
            """
            if autosave == False:
                self.users = {
                    "user": "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92", 
                    "ali": "6394ffec21517605c1b426d43e6fa7eb0cff606ded9c2956821c2c36bfee2810",
                    "kala": "e5268ad137eec951a48a5e5da52558c7727aaa537c8b308b5e403e6b434e036e"
                    }
            else:
                self.users = {}
                try:
                    with open('clinic/users.txt', 'r') as file:
                        for line in file:
                                key, value = line.strip().split(",", 1)
                                self.users[key] = value
                except FileNotFoundError:
                    print("file not found")
            self.logged_on = False
            self.patients_dao = PatientDAOJSON(autosave)
            self.current_patient = None
            self.autosave = autosave

        def get_password_hash(self, password: str) -> str:
            """
            hashes a password and returns the resulting string
            """
            encoded_password = password.encode('utf-8')    
            hash_object = hashlib.sha256(encoded_password)    
            hex_dig = hash_object.hexdigest()      
            return hex_dig

        def login(self, username: str, password: str) -> bool:
            """
            if not self.logged_on and both correct username and password are given, sets self.logged to True and returns True, 
            otherwise exception is raised
            """
            if self.logged_on:
                raise DuplicateLoginException("duplicate login exception")
            else:
                if username in self.users and self.users.get(username) == self.get_password_hash(password):
                    self.logged_on = True
                    return True
                else:
                    raise InvalidLoginException("invalid login exception raised")

        def logout(self) -> bool:
            """
            if self.logged_on, sets self.logged_on to False and returns True
            otherwise exception is raised
            """
            if not self.logged_on:
                raise InvalidLogoutException("invalid logout exception")
            else:
                self.logged_on = False
                return True

        def create_patient(self, phn: int, name: str, bday: str, phone: str, email: str, address: str)-> Patient:
            """
            if self.logged_on and phn DNE, calls and returns PatientDAOJSON create_patient method
            otherwise, exception is raised
            """
            if not self.logged_on:
                raise IllegalAccessException("illegal access exception")
            if self.patients_dao.search_patient(phn) is not None:
                raise IllegalOperationException("illegal operation exception")
            new = Patient(phn, name, bday, phone, email, address, self.autosave)
            self.patients_dao.create_patient(new)
            return new
            
        def search_patient(self, phn: int)-> Patient:
            """
            if found, calls and returns PatientDAOJSON search_patient method
            otherwise, exception is raised
            """
            if not self.logged_on:
                raise IllegalAccessException("illegal access exception")
            return self.patients_dao.search_patient(phn)
        
        def retrieve_patients(self, name: str)-> list[Patient]:
            """
            if logged on, calls and returns PatientDAOJSON retrieve_patients method
            otherwise, exception is raised
            """
            if not self.logged_on:
                raise IllegalAccessException("illegal access exception")
            return self.patients_dao.retrieve_patients(name)
            
        def update_patient(self, phn1: int, phn2: int, name: str, bday: str, phone: str, email: str, address: str)-> bool:
            """
            if self.logged_on, the patient exists, and the new phn doesn't already exist, calls and returns PatientDAOJSON update_patient method
            otherwise, exception is raised
            """
            if not self.logged_on:
                raise IllegalAccessException("illegal access exception")
            if self.patients_dao.search_patient(phn1) is None:
                raise IllegalOperationException("illegal operation exception")
            if phn1 != phn2 and self.patients_dao.search_patient(phn2) is not None:
                raise IllegalOperationException("illegal operation exception")
            elif self.current_patient is not None and phn1 == self.current_patient.get_phn():
                raise IllegalOperationException("illegal operation exception")
            cur = self.patients_dao.search_patient(phn1)
            cur.set_phn(phn2)
            cur.set_name(name)
            cur.set_bday(bday)
            cur.set_phone(phone)
            cur.set_email(email)
            cur.set_address(address)
            return self.patients_dao.update_patient(phn1, cur)
            
        def list_patients(self)-> list[Patient]:
            """
            if self.logged_on, calls and returns PatientDAOJSON list_patient method.
            otherwise, exception is raised
            """
            if not self.logged_on:
                raise IllegalAccessException("illegal access exception")
            return self.patients_dao.list_patients()

        def delete_patient(self, phn: int)-> bool:
            """
            if self.logged_on, and given phn is a valid phn but not the self.current_patient phn, calls and returns PatientDAOJSON delete_patient method
            otherwise, exception is raised
            """
            if not self.logged_on:
                raise IllegalAccessException("illegal access exception")
            if self.current_patient is not None and self.current_patient.get_phn() == phn or self.patients_dao.search_patient(phn) is None:
                raise IllegalOperationException("illegal operation exception")
            return self.patients_dao.delete_patient(phn)

        def set_current_patient(self, phn: int)-> None:
            """
            if self.logged_on and given phn is a valid patient, sets the corresponding patient to self.current_patient
            otherwise, exception is raised
            """
            if not self.logged_on:
                raise IllegalAccessException("illegal access exception")
            pat = self.patients_dao.search_patient(phn)
            if pat is None:
                raise IllegalOperationException("illegal operation exception")
            self.current_patient = pat

        def get_current_patient(self)-> Patient:
            """
            if self.logged_on with a valid current patient, returns self.current_patient,
            otherwise, an exception is raised or, if there is no current patient, returns None
            """
            if not self.logged_on:
                raise IllegalAccessException("illegal access exception")
            if self.current_patient is None:
                return None
            return self.current_patient

        def unset_current_patient(self)-> None:
            """
            if logged on, sets self.current_patient to None.
            otherwise, exception is raised.
            """
            if not self.logged_on:
                raise IllegalAccessException("illegal access exception")
            self.current_patient = None

        def create_note(self, text: str)-> Note:
            """
            if self.logged_on and valid self.current_patient, calls and returns create_note function from Patient class
            otherwise, exception is raised
            """
            if not self.logged_on:
                raise IllegalAccessException("illegal access exception")
            if self.current_patient is None:
                raise NoCurrentPatientException("no current patient exception")
            return self.current_patient.create_note(text)

        def search_note(self, code: int)-> Note:
            """
            if self.logged_on and valid self.current_patient, calls and returns search_note function from Patient class
            otherwise, exception is raised
            """
            if not self.logged_on:
                raise IllegalAccessException("illegal access exception")
            if self.current_patient is None:
                raise NoCurrentPatientException("no current patient exception")
            return self.current_patient.search_note(code)

        def retrieve_notes(self, keyword: str)-> list[Note]:
            """
            if self.logged_on and valid self.current_patient, calls and returns retrieve_notes function from Patient class
            otherwise, exception is raised
            """
            if not self.logged_on:
                raise IllegalAccessException("illegal access exception")
            if self.current_patient is None:
                raise NoCurrentPatientException("no current patient exception")
            return self.current_patient.retrieve_notes(keyword)      

        def update_note(self, code: int, text: str)-> bool:
            """
            if self.logged_on and valid self.current_patient, calls and returns update_note function from Patient class
            otherwise, exception is raised
            """
            if not self.logged_on:
                raise IllegalAccessException("illegal access exception")
            if self.current_patient is None:
                raise NoCurrentPatientException("no current patient exception")
            return self.current_patient.update_note(code, text)

        def delete_note(self, code: int)-> bool:
            """
            if self.logged_on and valid self.current_patient, calls and returns delete_note function from Patient class
            otherwise, exception is raised
            """
            if not self.logged_on:
                raise IllegalAccessException("illegal access exception")
            if self.current_patient is None:
                raise NoCurrentPatientException("no current patient exception")
            return self.current_patient.delete_note(code)

        def list_notes(self)-> list[Note]:
            """
            if self.logged_on and valid self.current_patient, calls and returns list_notes function from Patient class
            otherwise, exception is raised
            """
            if not self.logged_on:
                raise IllegalAccessException("illegal access exception")
            if self.current_patient is None:
                raise NoCurrentPatientException("no current patient exception")
            return self.current_patient.list_notes()
                
            

            


            


                