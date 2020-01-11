from typing import Dict


class Actor:
    def __init__(self, uri: str, name: str, handles: Dict[str, str], date_of_birth: str = None):
        self.uri = uri
        self.name = name
        self.date_of_birth = date_of_birth
        self.handles: Dict[str, str] = handles

    def to_string(self):
        return self.name + " was born " + self.date_of_birth if self.date_of_birth else self.name
