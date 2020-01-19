from rdflib import Graph
from rdflib import URIRef


def retrieve_tropes(series_name):
    g = Graph()
    series_data_name = 'series_data_'+str(series_name).lower()+'.nt'
    g.parse(series_data_name, format="nt")

    series_full_name = URIRef("http://dbtropes.org/resource/Series/" + series_name)
    if (series_full_name, None, None) in g:
        print("This graph contains triples about " + series_name)

    has_feature = URIRef("http://skipforward.net/skipforward/resource/seeder/skipinions/hasFeature")
    tropes_list = []
    for o in g.objects(series_full_name, has_feature):

        print(series_name + " have the trope: %s" % o)
        tropes = o.split('/')
        print(series_name + " have the trope: %s" % tropes[5])

        tropes_list.append((o, tropes[5]))

    return tropes_list


if __name__ == "__main__":
    retrieve_tropes("Friends")