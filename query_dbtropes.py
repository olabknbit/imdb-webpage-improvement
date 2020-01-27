from typing import List, Tuple, Any

from rdflib import Graph
from rdflib import URIRef

from filenames import *


def retrieve_tropes(series_name: str) -> List[Tuple[Any, str]]:
    """
    Retrieve series related tropes from local dbtropes series datastore.
    :param series_name (str): Name of a series
    :return List[Tuple[Any, str]]: List of tropes occurring in that series in a form of a list of tuples
    (url, trope name)
    """
    g = Graph()
    series_data_name = get_series_dbtropes_filename(series_name)
    g.parse(series_data_name, format="nt")
    series_full_name = URIRef("http://dbtropes.org/resource/Series/" + series_name.replace(' ', ''))

    has_feature = URIRef("http://skipforward.net/skipforward/resource/seeder/skipinions/hasFeature")
    tropes_list = []
    for url in g.objects(series_full_name, has_feature):
        tropes = url.split('/')
        if tropes[4] == 'Main':
            trope = ''.join(' ' + x if x.isupper() else x for x in tropes[5]).strip(' ')
            tropes_list.append((url, trope))
    return tropes_list
