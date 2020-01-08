import re
from rdflib import Graph
from rdflib import URIRef
from rdflib.namespace import RDFS


def parse_dbtropes():
    series_data = open('series_data.nt', 'w')
    with open('dbtropes.nt') as rawfile:
        for line in rawfile:
            if re.match("<http://dbtropes.org/resource/Series/", line):
                series_data.write(line)
        series_data.close()


def retrieve_tropes(seriesName):
    # uncomment when running for the first time
    # parse_dbtropes()
    g = Graph()
    g.parse("series_data.nt", format="nt")

    seriesFullName = URIRef("http://dbtropes.org/resource/Series/"+seriesName)
    if (seriesFullName, None, None) in g:
        print("This graph contains triples about "+seriesName)

    hasFeature = URIRef("http://skipforward.net/skipforward/resource/seeder/skipinions/hasFeature")
    tropes_list = []
    for o in g.objects(seriesFullName, hasFeature):

        print(seriesName+" have the trope: %s"%o)
        tropes = o.split('/')
        print(seriesName + " have the trope: %s" %tropes[5])

        tropes_list.append((o, tropes[5]))

    return tropes_list


if __name__ == "__main__":
    retrieve_tropes("Friends")