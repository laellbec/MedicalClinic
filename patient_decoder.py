from clinic.patient import Patient
import json

class PatientDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs) -> None:
        """
        initializes the PatientDecoder
        """
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, dct: dict):
        """
        converts and returns a dictionary to a Patient object if the dictionary has the key "__type__" with the value "Patient",
        otherwise recturns dct
        """
        if "__type__" in dct and dct["__type__"] == "Patient":
            return Patient(dct["phn"], dct["name"], dct["birth_date"], dct["phone"], dct["email"], dct["address"])
        return dct