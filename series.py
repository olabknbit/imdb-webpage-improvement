from typing import Optional, List

from actor import Actor


class Series:
    def __init__(self, dbpedia_uri: Optional[str], network: Optional[str], wikidata_uri: Optional[str],
                 actors: List[Actor]):
        self.dbpedia_uri = dbpedia_uri
        self.network = network
        self.wikidata_uri = wikidata_uri
        self.actors = actors

    def get_actor_wikidata_uri(self, actor_name):
        for actor in self.actors:
            if actor.name == actor_name:
                return self.wikidata_uri
