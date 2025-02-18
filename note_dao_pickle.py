from clinic.note import Note
from .note_dao import NoteDAO
from pickle import dump, load

class NoteDAOPickle(NoteDAO):
    def __init__(self, autosave: bool, phn: int) -> None:
        """
        initializes attributes of NoteDaoPickle based on whether autosave is true or false. if true, record containing notes is loaded from a binary file field. otherwise, record is initialized as an empty dictionary 
        """
        self.autosave = autosave
        if self.autosave:
            self.record_file = "clinic/records/%s.dat" % str(phn)
            try: 
                with open(self.record_file, 'rb') as file:
                    self.notes = load(file)
                    keys = list(self.notes.keys())
                    if len(keys) == 0:
                        self.autocounter = 0
                    else:
                        self.autocounter = max(keys)
            except FileNotFoundError:
                self.notes = {}
                self.autocounter = 0 
        else:
            self.notes = {}
            self.autocounter = 0 


    def get_autocounter(self)-> int:
        """
        returns autocounter of self PatientRecord instance
        """
        return self.autocounter

    def set_autocounter(self, val: int)-> None:
        """
        sets current autocounter of self PatientRecord to given value
        """
        self.autocounter = val

    def get_notes(self)-> dict[int, Note]:
        """
        returns notes of self PatientRecord instance
        """
        return self.notes

    def set_notes(self, new_notes: dict[int, str])-> None:
        """
        sets current notes of self PatientRecord to given notes
        """
        self.notes = new_notes
        self.autocounter = len(new_notes)  

    def create_note(self, text: str)-> Note:
        """
        increases the autocounter by 1, creates and returns a new Note instance,
        and adds the new Note to notes. 
        notes is updated in patient record file
        """
        self.autocounter += 1
        new_note = Note(self.autocounter, text)
        self.notes[self.autocounter] = new_note
        if self.autosave:
            with open(self.record_file, 'wb') as file:
                dump(self.notes, file)
        return new_note

    def search_note(self, key: int)-> Note:
        """
        if given code is in notes, returns corresponding note,
        otherwise returns None
        """
        if key not in self.get_notes():
            return None
        else:
            return self.notes.get(key)

    def retrieve_notes(self, search_string: str)-> list[Note]:
        """
        returns a list of notes that contain given keyword
        """
        note_list = []
        for key in self.notes:
                if search_string.upper() in self.notes.get(key).get_text().upper():
                    note_list.append(self.notes.get(key))
        return note_list

    def update_note(self, key: int, text: str)-> bool:
        """
        if the note is valid, updates the desired note and returns True.
        notes is updated in patient record file
        """
        if len(self.notes) == 0 or key not in self.notes:
            return False
        else:
            self.notes.get(key).update(text)
            if self.autosave:
                with open(self.record_file, 'wb') as file: 
                    dump(self.notes, file)
            return True

    def delete_note(self, key: int)-> bool:
        """
        if the note exists, deletes from dictionary and returns True,
        notes is updated in patient record file
        """
        if len(self.notes) == 0 or key not in self.notes:
            return False
        else:
            del self.notes[key]
            keys = list(self.notes.keys())
            if len(self.notes) != 0:
                self.autocounter = max(keys)
            else:
                self.autocounter = 0
            if self.autosave:
                with open(self.record_file, 'wb') as file:
                    dump(self.notes, file)
            return True

    def list_notes(self)-> list[Note]:
        """
        returns a list of the notes in reverse order of when they were created
        """
        note_list = []
        if(len(self.notes) == 0):
            return note_list
        else:
            note_list = list(self.notes.values())
            note_list.reverse()
            return note_list

    
