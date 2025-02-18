import datetime
class Note:
    def __init__(self, code: int = 0, text: str = "")-> None:
        """
        initializes attributes of Note instance
        """
        self.text = text
        self.code = code
        self.timestamp = datetime.datetime.now()

    def __eq__(self, other: 'Note')-> bool:
        """
        returns True if self Note has the same text and note_num as other Note,
        otherwise returns False
        """
        return(self.text == other.get_text()
                and self.code == other.get_note_num())
    
    def __str__(self) -> str:
        """
        returns a readable string with note_num and text of self Note
        """
        return f'Note {self.code}: {self.text}'

    def get_text(self)-> str:
        """
        returns text of self Note instance
        """
        return self.text

    def set_text(self, new: str)-> None:
        """
        sets current text of self Note to given string
        """
        self.text = new
    
    def get_note_num(self)-> int:
        """
        returns note_num of self Note instance
        """
        return self.code

    def set_note_num(self, num: int)-> None:
        """
        sets current note_num of self Note to given value
        """
        self.code = num

    def get_time(self)-> datetime:
        """
        returns time of self Note instance
        """
        return self.timestamp

    def set_time(self)-> None:
        """
        sets original time of self Note to current time
        """
        self.timestamp = datetime.datetime.now()

    def update(self, new_text: str)-> None:
        """
        sets the original time of self Note to current time,
        sets the original text to given string
        """
        self.timestamp = datetime.datetime.now()
        self.text = new_text
        
        