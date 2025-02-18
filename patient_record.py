from .dao.note_dao_pickle import NoteDAOPickle
from .note import Note
class PatientRecord:
    def __init__(self, autosave: bool, phn: int)-> None:
        """
        initializes attributes of PatientRecord instance
        """
        self.note_dao = NoteDAOPickle(autosave, phn)

    def __eq__(self, other: 'PatientRecord')-> bool:
        """
        returns True if self PatientRecord has the same autocounter and notes
        as other PatientRecord, otherwise returns False
        """
        return (self.note_dao.autocounter == other.get_autocounter()
                and self.note_dao.notes == other.get_notes())
    
    def __str__(self) -> str:
        """
        returns a readable string with autocounter of self PatientRecord
        """
        return f'This patient record has {self.note_dao.autocounter} note(s)'
    
    def get_autocounter(self)-> int:
        """
        calls and returns get_autocounter method in NoteDAOPickle
        """
        return self.note_dao.get_autocounter()

    def set_autocounter(self, val: int)-> None:
        """
        calls set_autocounter method in NoteDAOPickle
        """
        self.note_dao.set_autocounter(val)

    def get_notes(self)-> dict[int, Note]:
        """
        calls and returns NoteDAOPickle get_notes method
        """
        return self.note_dao.get_notes()

    def set_notes(self, new_notes: dict[int, str])-> None:
        """
        calls set_notes method in NoteDAOPickle
        """
        self.note_dao.set_notes(new_notes)

    def create_note(self, text: str)-> Note:
        """
        calls and returns create_note method in NoteDAOPickle
        """
        return self.note_dao.create_note(text)

    def search_note(self, code: int)-> Note:
        """
        calls and returns search_note method in NoteDAOPickle
        """
        return self.note_dao.search_note(code)


    def retrieve_notes(self, keyword: str)-> list[Note]:
        """
        calls and returns retrieve_note method in PNoteDAOPickle
        """
        return self.note_dao.retrieve_notes(keyword)


    def update_note(self, code: int, text: str)-> bool:
        """
        calls and returns update_note method in NoteDAOPickle
        """
        return self.note_dao.update_note(code, text)


    def delete_note(self, code: int)-> bool:
        """
        calls and returns delete_note method in NoteDAOPickle
        """
        return self.note_dao.delete_note(code)


    def list_notes(self)-> list[Note]:
        """
        calls and returns list_notes method in NoteDAOPickle
        """
        return self.note_dao.list_notes()