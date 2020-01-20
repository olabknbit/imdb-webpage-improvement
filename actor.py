from typing import Dict


class Actor:
    def __init__(self, dbpedia_uri: str = None, wikidata_uri: str = None, name: str = None,
                 handles: Dict[str, str] = {}, date_of_birth: str = None):
        self.wikidata_uri = wikidata_uri
        self.dbpedia_uri = dbpedia_uri
        self.name = name
        self.date_of_birth = date_of_birth
        self.handles: Dict[str, str] = handles

    def to_string(self):
        return str(self.name) + " was born " + self.date_of_birth if self.date_of_birth else self.name

    def get_uri(self):
        uri = ("http://www.wikidata.org/entity/" + self.wikidata_uri) if self.wikidata_uri is not None else ""
        return uri
