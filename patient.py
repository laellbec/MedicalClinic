from .patient_record import PatientRecord
from .note import Note
class Patient:
    def __init__(self, phn: int = 0, name: str= "", bday: str = "", phone: str = "", email: str = "", address: str = "", autosave: bool = True)-> None:
        """
        initializes attributes of Patient instance
        """
        self.phn = phn
        self.name = name
        self.birth_date = bday
        self.phone = phone
        self.email = email
        self.address = address
        self.patient_record = PatientRecord(autosave, phn)

    def __eq__(self, other: 'Patient')->bool:
        """
        returns True if all attributes except for patient_record of self Patient 
        are the same as other Patient, otherwise returns False
        """
        return (self.phn == other.phn 
                and self.name == other.get_name()
                and self.birth_date == other.get_bday()
                and self.phone == other.get_phone()
                and self.email == other.get_email()
                and self.address == other.get_address())
    
    def __str__(self) -> str:
        """
        returns a readable string with self Patients name and phn
        """
        return f'Patient {self.name}\'s phn is {self.phn}'
    
    def get_phn(self)-> int:
        """
        returns phn of self Patient instance
        """
        return self.phn

    def set_phn(self, new_phn: int)-> None:
        """
        sets current phn of self Patient to given value
        """
        self.phn = new_phn

    def get_name(self)-> str:
        """
        returns name of self Patient instance
        """
        return self.name

    def set_name(self, new_name: str)-> None:
        """
        sets current name of self Patient to given string
        """
        self.name = new_name

    def get_bday(self)-> str:
        """
        returns bday of self Patient instance
        """
        return self.birth_date

    def set_bday(self, new_bday: str)-> None:
        """
        sets current bday of self Patient to given string
        """
        self.birth_date = new_bday

    def get_phone(self)-> str:
        """
        returns phone of self Patient instance
        """
        return self.phone

    def set_phone(self, new_phone: str)-> None:
        """
        sets current phone of self Patient to given string
        """
        self.phone = new_phone

    def get_email(self)-> str:
        """
        returns email of self Patient instance
        """
        return self.email

    def set_email(self, new_email: str)-> None:
        """
        sets current email of self Patient to given string
        """
        self.email = new_email

    def get_address(self)-> str:
        """
        returns address of self Patient instance
        """
        return self.address

    def set_address(self, new_add: str)-> None:
        """
        sets current address of self Patient to given string
        """
        self.address = new_add

    def get_patient_rec(self)-> PatientRecord:
        """
        returns patient_record of self Patient instance
        """
        return self.patient_record

    def set_patient_rec(self, new_rec: PatientRecord)-> None:
        """
        sets current patient_record of self Patient to given PatientRecord
        """
        self.patient_record = new_rec
    
    def create_note(self, text: str)-> Note:
        """
        calls and returns create_note function in PatientRecord class
        """
        return self.patient_record.create_note(text)
    
    def search_note(self, code: int)-> Note:
        """
        calls and returns search_note function in PatientRecord class
        """
        return self.patient_record.search_note(code)

    def retrieve_notes(self, keyword: str)-> list[Note]:
        """
        calls and returns retrieve_note function in PatientRecord class
        """
        return self.patient_record.retrieve_notes(keyword)
    
    def update_note(self, code: int, text: str)-> bool:
        """
        calls and returns update_note function in PatientRecord class
        """
        return self.patient_record.update_note(code, text)

    def delete_note(self, code: int)-> bool:
        """
        calls and returns delete_note function in PatientRecord class
        """
        return self.patient_record.delete_note(code)

    def list_notes(self)-> list[Note]:
        """
        calls and returns list_note function in PatientRecord class
        """
        return self.patient_record.list_notes()
