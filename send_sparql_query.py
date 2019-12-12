from SPARQLWrapper import SPARQLWrapper, JSON


def get_network_name(series_name: str):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    query = """
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        prefix dbpedia-owl: <http://dbpedia.org/ontology/>

        select ?net where  {
        { ?film a dbpedia-owl:TelevisionShow }
        ?film rdfs:label ?label .
        ?film dbo:network ?net
        filter regex( str(?label), "^""" + series_name + """", "i") .
        FILTER langMatches(lang(?label), "en")
        }

        limit 1
    """
    sparql.setQuery(query)
    print(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    for result in results["results"]["bindings"]:
        return result['net']['value']
        # print('%s: %s' % (result["label"]["xml:lang"], result["label"]["value"]))


if __name__ == "__main__":
    nn = get_network_name("Gossip Girl")
    print(nn)
