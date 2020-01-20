from typing import List, Tuple, Any

from rdflib import Graph
from rdflib import URIRef

from filenames import *


def retrieve_tropes(series_name: str) -> List[Tuple[Any, str]]:
    """
    Retrieve series related tropes from local dbtropes series datastore.
    :param series_name (str): Name of a series
    :return List[Tuple[Any, str]]: List of tropes occurring in that series
    TODO(bulka): what is in the tuple except for series name? Update docstring pls.
    """
    g = Graph()
    series_data_name = get_series_dbtropes_filename(series_name)
    g.parse(series_data_name, format="nt")
    series_full_name = URIRef("http://dbtropes.org/resource/Series/" + series_name.replace(' ', ''))
    if (series_full_name, None, None) in g:
        print("This graph contains triples about " + series_name)
    else:
        print("This graph does not contain triples about " + series_name)

    has_feature = URIRef("http://skipforward.net/skipforward/resource/seeder/skipinions/hasFeature")
    tropes_list = []
    for o in g.objects(series_full_name, has_feature):
        tropes = o.split('/')
        if tropes[4] == 'Main':
            tropes_list.append((o, tropes[5]))
    return tropes_list

if __name__ == "__main__":
    retrieve_tropes("Friends")
