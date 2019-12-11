from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setQuery("""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>

    SELECT distinct ?film ?label where  {
    { ?film a dbpedia-owl:TelevisionShow }
    ?film rdfs:label ?label .
    FILTER regex( str(?label), "^stranger things"@en, "i") .
    FILTER langMatches(lang(?label), "en")
}

limit 1000
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for result in results["results"]["bindings"]:
    print('%s: %s' % (result["label"]["xml:lang"], result["label"]["value"]))