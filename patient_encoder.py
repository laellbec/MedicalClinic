import json
from clinic.patient import Patient

class PatientEncoder(json.JSONEncoder):
    def default(self, obj):
        """
        overrides the default method to convert Patient objects to a serializable dictionary
        """
        if isinstance(obj, Patient):
            return {"__type__":"Patient", "phn":obj.phn, "name":obj.name, "birth_date":obj.birth_date, "phone":obj.phone, "email":obj.email, "address":obj.address}
        return super().default(obj)