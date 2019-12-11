from SPARQLWrapper import SPARQLWrapper, JSON


def get_network_name():
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        prefix dbpedia-owl: <http://dbpedia.org/ontology/>

        select ?net where  {
        { ?film a dbpedia-owl:TelevisionShow }
        ?film rdfs:label ?label .
        ?film dbo:network ?net
        filter regex( str(?label), "^stranger things", "i") .
        FILTER langMatches(lang(?label), "en")
        }

        limit 1
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    for result in results["results"]["bindings"]:
        return result['net']['value']
        # print('%s: %s' % (result["label"]["xml:lang"], result["label"]["value"]))


if __name__ == "__main__":
    get_network_name()
