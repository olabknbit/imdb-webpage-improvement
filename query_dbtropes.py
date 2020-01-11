from rdflib import Graph
from rdflib import URIRef


def retrieve_tropes(seriesName):

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