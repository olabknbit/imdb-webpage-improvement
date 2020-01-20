import os

DBTROPES_DIR = "dbtropes"
SERIES_DATA_FILENAME = os.path.join(DBTROPES_DIR, 'series_data.nt')


def get_series_dbtropes_filename(series_name: str) -> str:
    """
    Returns a filename of a local dbtropes series database for a series with series name 'series_name'
    :param series_name (str): Name of the series
    :return str: filename of the local dbtropes series database

    >>> get_series_dbtropes_filename("Friends")
    'dbtropes/series_data_friends.nt'
    >>> get_series_dbtropes_filename("Stranger Things")
    'dbtropes/series_data_stranger_things.nt'
    """

    return os.path.join(DBTROPES_DIR, 'series_data_' + str('_'.join(series_name.split(' '))).lower() + '.nt')
