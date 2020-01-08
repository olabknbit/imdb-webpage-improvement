from typing import List

from SPARQLWrapper import SPARQLWrapper, JSON


def get_network_name(series_name: str) -> str:
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    query = """
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>

        SELECT ?net where  {
            { ?film a dbpedia-owl:TelevisionShow }
            ?film rdfs:label ?label .
            ?film dbo:network ?net
            FILTER regex( str(?label), "^""" + series_name + """", "i") .
            FILTER langMatches(lang(?label), "en")
        }

        LIMIT 1
    """
    sparql.setQuery(query)
    # print(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    for result in results["results"]["bindings"]:
        return result['net']['value']
        # print('%s: %s' % (result["label"]["xml:lang"], result["label"]["value"]))


def strip_wikidata_entity(uri: str) -> str:
    return uri[len("http://www.wikidata.org/entity/"):]


def get_wikidata_uri(series_name: str) -> str:
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    query = """
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>

        select DISTINCT ?sameas where  {
            { ?film a dbpedia-owl:TelevisionShow }
            ?film rdfs:label ?label .
            ?film dbo:network ?net .
            ?film owl:sameAs ?sameas .
            FILTER regex( str(?label), "^""" + series_name + """", "i") .
            FILTER regex( str(?sameas), "http://www.wikidata.org/entity/", "i") .
        
            FILTER langMatches(lang(?label), "en")
        }
        LIMIT 1
    """
    sparql.setQuery(query)
    # print(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    for result in results["results"]["bindings"]:
        return strip_wikidata_entity(result['sameas']['value'])


def get_wikidata_actor_uris(series_uri: str) -> List[str]:
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    query = """
        SELECT ?show ?actor
        WHERE {
            BIND(wd:""" + series_uri + """ as ?show) .
            ?show wdt:P161 ?actor .
            SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en" }
        } 
        LIMIT 3
    """
    sparql.setQuery(query)
    # print(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    actors = [strip_wikidata_entity(result['actor']['value']) for result in results["results"]["bindings"]]
    return actors


class Actor:
    def __init__(self, uri: str, name: str, date_of_birth: str):
        self.uri = uri
        self.name = name
        self.date_of_birth = date_of_birth

    def to_string(self):
        return self.name + " was born " + self.date_of_birth


def get_actor_info_from_wikidata(actor_uri: str) -> Actor:
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    query = """
        SELECT ?actor ?actorLabel ?dateofbirth
        WHERE {
            BIND(wd:""" + actor_uri + """ as ?actor) .
            ?actor wdt:P569 ?dateofbirth .
            SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en" }
            
        }
        """
    sparql.setQuery(query)
    # print(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    for result in results["results"]["bindings"]:
        uri = result['actor']['value']
        name = result['actorLabel']['value']
        bod = result['dateofbirth']['value']
        return Actor(uri=uri, name=name, date_of_birth=bod)


def get_series_actors(series_name: str) -> List[Actor]:
    uri = get_wikidata_uri(series_name)
    if uri is None:
        return []
    actor_uris = get_wikidata_actor_uris(uri)
    actors = [get_actor_info_from_wikidata(actor_uri) for actor_uri in actor_uris]
    actors = [a for a in actors if a is not None]
    return actors


if __name__ == "__main__":
    # nn = get_network_name("Gossip Girl")
    get_series_actors("Stranger Things")
