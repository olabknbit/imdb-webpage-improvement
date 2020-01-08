class Actor:
    def __init__(self, uri: str, name: str, date_of_birth: str = None):
        self.uri = uri
        self.name = name
        self.date_of_birth = date_of_birth

    def to_string(self):
        return self.name + " was born " + self.date_of_birth
