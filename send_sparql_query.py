from typing import List, Dict, Optional

from SPARQLWrapper import SPARQLWrapper, JSON

from actor import Actor
from series import Series


def get_info_from_dbpedia(series_name: str) -> Optional[Series]:
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    query = """
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>

        SELECT ?film ?net ?sameas ?actor ?actorName ?actorWikidata where  {
            { ?film a dbpedia-owl:TelevisionShow }
            ?film rdfs:label ?label .
            ?film owl:sameAs ?sameas .
            OPTIONAL { 
                ?film owl:sameAs ?sameas .
            }
            OPTIONAL {
                ?film dbo:network ?net .
            }
            OPTIONAL {
                ?film dbo:starring ?actor .
                ?actor rdfs:label ?actorName .
                FILTER langMatches(lang(?actorName), "en") .
                ?actor owl:sameAs ?actorWikidata .
                FILTER regex( str(?actorWikidata), "http://www.wikidata.org/entity/", "i") .
            }
            FILTER regex( str(?label), "^""" + series_name + """$|^""" + series_name + """ \\\\(TV Series\\\\)", "i") .
            FILTER regex( str(?sameas), "http://www.wikidata.org/entity/", "i") .
            FILTER langMatches(lang(?label), "en")
        }
        LIMIT 20
    """
    print(query)
    sparql.setQuery(query)
    # print(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()["results"]["bindings"]

    if len(results) > 0:
        result = results[0]
        network = result['net']['value'].replace("_(TV_channel)", "").replace("_",
                                                                              " ") if 'net' in result.keys() else None
        dbpedia_uri = result['film']['value'] if 'film' in result.keys() else None
        wikidata_uri = result['sameas']['value'] if 'sameas' in result.keys() else None
        series = Series(dbpedia_uri=dbpedia_uri, network=network,
                        wikidata_uri=strip_wikidata_entity(wikidata_uri), actors=[])

        for result in results:
            actor_dbpedia_uri = result['actor']['value'] if 'actor' in result.keys() else None
            actor_wikidata_uri = result['actorWikidata']['value'] if 'actorWikidata' in result.keys() else None
            actor_name = result['actorName']['value'] if 'actorName' in result.keys() else None
            if actor_dbpedia_uri is not None:
                actor = Actor(dbpedia_uri=actor_dbpedia_uri, wikidata_uri=strip_wikidata_entity(actor_wikidata_uri),
                              name=actor_name)
                series.actors.append(actor)
    else:
        series = Series(dbpedia_uri=None, network=None, wikidata_uri=None, actors=[])

    return series


def strip_wikidata_entity(uri: str) -> str:
    return uri[len("http://www.wikidata.org/entity/"):]


def get_wikidata_actors(series_uri: str) -> Dict[str, Actor]:
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    query = """
        SELECT ?show ?actor ?actorLabel ?dateofbirth ?RottenTomatoes ?Instagram ?Twitter ?Facebook
        WHERE {
            BIND(wd:""" + series_uri + """ as ?show) .
            ?show wdt:P161 ?actor .
            OPTIONAL {
                ?actor wdt:P569 ?dateofbirth .
            }        
            OPTIONAL {
                ?actor wdt:P1258 ?RottenTomatoes . 
            }
            OPTIONAL {
                ?actor wdt:P2003 ?Instagram .
            }
            OPTIONAL {
                ?actor wdt:P2002 ?Twitter .
            }
            OPTIONAL {
                ?actor wdt:P2013 ?Facebook .        
            }
            SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en" }
        } 
    """
    import urllib.error
    # TODO add try except clauses in all requests
    print(query)
    try:
        sparql.setQuery(query)
        # print(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
    except urllib.error.HTTPError as e:
        print("Error occurred: %s. Waiting 1 sec and retrying" % str(e))
        import time
        time.sleep(1)
        print("Retying")
        return get_wikidata_actors(series_uri)

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
        actors[name] = Actor(wikidata_uri=uri, name=name, date_of_birth=date_of_birth, handles=handles)

    return actors


def query_wikidata_for_actor_info(actor_uri: str) -> Optional[Actor]:
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    query = """
        SELECT ?actor ?actorLabel ?dateofbirth ?RottenTomatoes ?Instagram ?Twitter ?Facebook
        WHERE {
            BIND(wd:""" + actor_uri + """ as ?actor) .
            OPTIONAL {
                ?actor wdt:P569 ?dateofbirth .
            }        
            OPTIONAL {
                ?actor wdt:P1258 ?RottenTomatoes . 
            }
            OPTIONAL {
                ?actor wdt:P2003 ?Instagram .
            }
            OPTIONAL {
                ?actor wdt:P2002 ?Twitter .
            }
            OPTIONAL {
                ?actor wdt:P2013 ?Facebook .        
            }
            SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en" }
        } 
    """
    print(query)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    handles_names = {"RottenTomatoes": "https://www.rottentomatoes.com/",
                     "Instagram": "https://www.instagram.com/",
                     "Twitter": "https://twitter.com/",
                     "Facebook": "https://www.facebook.com/"}

    for result in results["results"]["bindings"]:
        uri = strip_wikidata_entity(result["actor"]["value"])
        name = result["actorLabel"]["value"]
        date_of_birth = result['dateofbirth']['value'] if "dateofbirth" in result.keys() else None

        handles = {handle: handles_names[handle] + result[handle]["value"] for handle in handles_names.keys()
                   if handle in result.keys() and result[handle]['value'] is not None}
        return Actor(wikidata_uri=uri, name=name, date_of_birth=date_of_birth, handles=handles)


def get_series_actors(series: Series, names_to_put_first: List[str], show_all=True) -> List[Actor]:
    limit = 20
    uri = series.wikidata_uri
    if uri is None:
        wikidata_actors = {}
    else:
        wikidata_actors = get_wikidata_actors(uri)
    sorted_actors = []

    for name in names_to_put_first:
        actor = None
        if name in wikidata_actors.keys():
            actor = wikidata_actors[name]
        elif wikidata_uri := series.get_actor_wikidata_uri(actor_name=name):
            actor = query_wikidata_for_actor_info(wikidata_uri)
        if actor is None:
            actor = Actor(name=name)

        sorted_actors.append(actor)

    if show_all:
        for name in wikidata_actors.keys():
            if len(sorted_actors) > limit:
                break
            if name not in names_to_put_first:
                sorted_actors.append(wikidata_actors[name])

    return sorted_actors


if __name__ == "__main__":
    # nn = get_network_name("Gossip Girl")
    # print(get_info_from_dbpedia("You Me Her"))
    # get_series_actors("Stranger Things", [])
    print(query_wikidata_for_actor_info("Q391359").to_string())
