from typing import Dict


class Actor:
    def __init__(self, dbpedia_uri: str = None, wikidata_uri: str = None, name: str = None, url: str = None,
                 handles: Dict[str, str] = {}, date_of_birth: str = None):
        self.name = name
        self.wikidata_uri = wikidata_uri
        self.dbpedia_uri = dbpedia_uri
        self.url = url
        self.date_of_birth = date_of_birth
        self.handles: Dict[str, str] = handles

    def to_string(self):
        return str(self.name) + " was born " + self.date_of_birth if self.date_of_birth else self.name

    def get_uri(self):
        uri = ("http://www.wikidata.org/entity/" + self.wikidata_uri) if self.wikidata_uri is not None else ""
        return uri

    def improve(self, actor: 'Actor'):
        if not self.name:
            self.name = actor.name
        if not self.wikidata_uri:
            self.wikidata_uri = actor.wikidata_uri
        if not self.dbpedia_uri:
            self.dbpedia_uri = actor.dbpedia_uri
        if not self.url:
            self.url = actor.url
        if not self.date_of_birth:
            self.date_of_birth = actor.date_of_birth
        if not self.handles:
            self.handles = actor.handles
