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


def get_wikidata_actor_uris(series_uri: str) -> Dict[str, Actor]:
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    query = """
        SELECT ?show ?actor ?actorLabel ?dateofbirth ?RottenTomatoes ?Instagram ?Twitter ?Facebook
        WHERE {
            BIND(wd:""" + series_uri + """ as ?show) .
            ?show wdt:P161 ?actor .
             OPTIONAL {
                    ?actor wdt:P569 ?dateofbirth .
                    ?actor wdt:P1258 ?RottenTomatoes . 
                    ?actor wdt:P2003 ?Instagram .
                    ?actor wdt:P2002 ?Twitter .
                    ?actor wdt:P2013 ?Facebook .
                }
            SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en" }
        } 
    """
    sparql.setQuery(query)
    # print(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    handles_names = {"RottenTomatoes": "https://www.rottentomatoes.com/",
                     "Instagram": "https://www.instagram.com/",
                     "Twitter": "https://twitter.com/",
                     "Facebook": "https://www.facebook.com/"}
    # print(results["results"]["bindings"])
    actors = {}
    for result in results["results"]["bindings"]:
        uri = strip_wikidata_entity(result["actor"]["value"])
        name = result["actorLabel"]["value"]
        date_of_birth = result['dateofbirth']['value'] if "dateofbirth" in result.keys() else None

        handles = {handle: handles_names[handle] + result[handle]["value"] for handle in handles_names.keys()
                   if handle in result.keys() and result[handle]['value'] is not None}
        actors[name] = Actor(uri=uri, name=name, date_of_birth=date_of_birth, handles=handles)

    return actors


def get_series_actors(series_name: str, names_to_put_first: List[str], show_all=True) -> List[Actor]:
    uri = get_wikidata_uri(series_name)
    if uri is None:
        return []
    all_actors = get_wikidata_actor_uris(uri)
    sorted_actors = []

    for name in names_to_put_first:
        if name in all_actors.keys():
            sorted_actors.append(all_actors[name])

    if show_all:
        for name in all_actors.keys():
            if name not in names_to_put_first:
                sorted_actors.append(all_actors[name])

    return sorted_actors


if __name__ == "__main__":
    # nn = get_network_name("Gossip Girl")
    get_series_actors("Stranger Things", [])
