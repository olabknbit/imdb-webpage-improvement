from SPARQLWrapper import SPARQLWrapper, JSON


def get_network_name(series_name: str):
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
    print(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    for result in results["results"]["bindings"]:
        return result['net']['value']
        # print('%s: %s' % (result["label"]["xml:lang"], result["label"]["value"]))


def get_wikidata_uri(series_name: str):
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
    print(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    for result in results["results"]["bindings"]:
        return result['sameas']['value']


def get_wikidata_actors(series_uri: str):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    query = """
        SELECT ?show ?actor
        WHERE {
            BIND(wd:Q22906308 as ?show) .
            ?show wdt:P161 ?actor .
            SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en" }
        } 
    """
    sparql.setQuery(query)
    print(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    for result in results["results"]["bindings"]:
        return result['actor']['value']

if __name__ == "__main__":
    # nn = get_network_name("Gossip Girl")
    # uri = get_wikidata_uri("Stranger Things")
    # print(uri)
    actors = get_wikidata_actors("")
    print(actors)
