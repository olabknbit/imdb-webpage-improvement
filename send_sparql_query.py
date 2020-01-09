from typing import List, Dict

from SPARQLWrapper import SPARQLWrapper, JSON

from actor import Actor


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


def get_wikidata_actor_uris(series_uri: str) -> List[Actor]:
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    query = """
        SELECT ?show ?actor ?actorLabel
        WHERE {
            BIND(wd:""" + series_uri + """ as ?show) .
            ?show wdt:P161 ?actor .
            SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en" }
        } 
    """
    sparql.setQuery(query)
    # print(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    actors = []
    for result in results["results"]["bindings"]:
        uri = strip_wikidata_entity(result['actor']['value'])
        actors.append(Actor(uri=uri, name=result['actorLabel']['value'], handles={}))

    return actors


def get_actor_info_from_wikidata(actor_uri: str) -> Actor:
    try:
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
        query = """
            SELECT ?actor ?actorLabel ?dateofbirth ?rottenTomatoesHandle ?instaHandle ?twitterHandle ?fbHandle
            WHERE {
                BIND(wd:""" + actor_uri + """ as ?actor) .
                OPTIONAL {
                    ?actor wdt:P569 ?dateofbirth .
                    ?actor wdt:P1258 ?rottenTomatoesHandle . 
                    ?actor wdt:P2003 ?instaHandle .
                    ?actor wdt:P2002 ?twitterHandle .
                    ?actor wdt:P2013 ?fbHandle .
                }
                SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en" }
                
            }
            """
        sparql.setQuery(query)
        # print(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        handles_names = ["rottenTomatoesHandle", "instaHandle", "twitterHandle", "fbHandle"]

        for result in results["results"]["bindings"]:
            uri = result['actor']['value']
            name = result['actorLabel']['value']
            bod = result['dateofbirth']['value']

            handles = {handle: result[handle]['value'] for handle in handles_names if
                       result[handle]['value'] is not None}
            print(handles)
            return Actor(uri=uri, name=name, date_of_birth=bod, handles=handles)
    except Exception as e:
        print(e.args)


def get_series_actors(series_name: str, names_to_filter=None) -> Dict[str, Actor]:
    uri = get_wikidata_uri(series_name)
    if uri is None:
        return {}
    actor_uris = get_wikidata_actor_uris(uri)
    actors = {}
    if names_to_filter:
        for actor in actor_uris:
            if actor.name in names_to_filter:
                if actor := get_actor_info_from_wikidata(actor.uri):
                    actors[actor.name] = actor

    return actors


if __name__ == "__main__":
    # nn = get_network_name("Gossip Girl")
    # get_series_actors("Stranger Things")
    get_actor_info_from_wikidata("Q162959")
