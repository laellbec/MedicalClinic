from clinic.patient import Patient
from .patient_dao import PatientDAO
from .patient_decoder import PatientDecoder
from .patient_encoder import PatientEncoder
import json
import os

class PatientDAOJSON(PatientDAO):
    def __init__(self, autosave: bool) -> None:
        """
        instantiates a patient directory, either as empty or loaded with patients from a json file depending on the value of autosave
        """
        self.autosave = autosave
        if self.autosave:
            self.patients = self.load_patients()
        else:
            self.patients = {}
    
    def load_patients(self) -> dict[int, Patient]:
        """
        returns a patient directory with patient objects that are retrieved from a file and decoded from json strings
        """
        patients = {}
        try:
            with open('clinic/patients.json', 'r') as file:
                decoder = PatientDecoder()
                for line in file:
                    patient = json.loads(line.strip(), object_hook=decoder.object_hook)
                    patients[patient.phn] = patient
            return patients
        except FileNotFoundError:
             return patients
        
    def save_patients(self) -> None:
        """
        updates json file with new changes to patient directory
        """
        with open('clinic/patients.json', 'w') as file:
            for patient in self.patients.values():
                json.dump(patient, file, cls=PatientEncoder)
                file.write('\n')

    def create_patient(self, patient: Patient)-> None:
        """
        creates and returns a new Patient instance and adds to self.patients. updates json file
        """
        self.patients[patient.get_phn()] = patient
        if self.autosave:
            self.save_patients()
            
    def search_patient(self, key: int)-> Patient:
        """
        returns a Patient instance
        """
        return self.patients.get(key)
    
    def retrieve_patients(self, search_string: str)-> list[Patient]:
        """
        returns a list of patients that have the given name in their name
        """
        found_p = []
        for key in self.patients:
            if search_string.upper() in self.patients.get(key).get_name().upper():
                found_p.append(self.patients.get(key))
        return found_p
        
    def update_patient(self, key: int, patient: Patient)-> bool:
        """
        updates the desired patient's fields to given fields and updates patient json file. returns true
        """
        self.patients[patient.get_phn()] = patient
        if key != patient.get_phn():
            del self.patients[key]
        if self.autosave:
            self.save_patients()
        return True
        
    def list_patients(self)-> list[Patient]:
        """
        returns a list of all Patients
        """
        patient_list = []
        for key in self.patients:
            patient_list.append(self.patients.get(key))
        return patient_list

    def delete_patient(self, key: int)-> bool:
        """
        deletes corresponding patient from self.patients and returns True. updates json file
        """
        del self.patients[key]

        file_path = os.path.join("clinic", "records", f"{key}.dat")
        if os.path.exists(file_path):
            os.remove(file_path)

        if self.autosave:
            self.save_patients()
        return True
