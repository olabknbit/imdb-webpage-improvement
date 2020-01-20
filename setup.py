import re
from typing import List
from zipfile import ZipFile

import wget

from filenames import *


def get_all_filenames(directory: str) -> List[str]:
    """
    Returns names of all files (not directories) in a directory.
    :param directory (str): directory name
    :return List[str]: List of names of files in that directory
    """
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [f for f in listdir(directory) if isfile(join(directory, f))]
    return onlyfiles


def parse_dbtropes(verbose: bool) -> None:
    """
    Downloads the dbtropes database and parses only the series data into separate file for faster access.
    :param verbose (bool): verbose indicates whether to print progress messages
    :return: None
    """
    dbtropes_zip_filename = 'dbtropes.zip'
    dbtropes_filename = os.path.join(DBTROPES_DIR, "dbtropes.nt")

    step_name = "Downloading dbtropes database"
    if not os.path.isfile(dbtropes_zip_filename):
        # Download DbTropes resource
        if verbose:
            print(step_name)
        url = "http://dbtropes.org/static/dbtropes.zip"
        wget.download(url, dbtropes_zip_filename)
    elif verbose:
        print("Skipping step: \"%s\"" % step_name)

    step_name = "Unzipping dbtropes database"
    if not os.path.isfile(dbtropes_filename):
        # Unzip DbTropes resource

        if verbose:
            print(step_name)
        with ZipFile(dbtropes_zip_filename, "r") as f:
            f.extractall(DBTROPES_DIR)

        # Drop the date part from the filename
        for filename in get_all_filenames(DBTROPES_DIR):
            old_path = os.path.join(DBTROPES_DIR, filename)
            new_path = os.path.join(DBTROPES_DIR, filename.split('-')[0] + '.nt')
            os.rename(old_path, new_path)
    elif verbose:
        print("Skipping step: \"%s\"" % step_name)

    step_name = "Parsing dbtropes database to keep only series related info"
    if not os.path.isfile(SERIES_DATA_FILENAME):
        if verbose:
            print(step_name)
        # Grab only Series relevant information from DbTropes file and save it in a separate file for faster parsing
        with open(dbtropes_filename) as raw_file, open(SERIES_DATA_FILENAME, 'w') as series_data_file:
            for line in raw_file:
                if re.match("<http://dbtropes.org/resource/Series/", line):
                    series_data_file.write(line)
    elif verbose:
        print("Skipping step: \"%s\"" % step_name)


def prepare_data_for_given_series(series_name: str, verbose: bool) -> None:
    """
    Parses dbtropes series database to grab info related to series with series_name.
    This is an optimization process, as the dbtropes databse is quite big and querying the whole database is very slow.
    :param series_name (str): Name of the series
    :param verbose (bool): whether to print progress messages
    :return: None
    """
    new_series_data_filename = get_series_dbtropes_filename(series_name)
    step_name = "Parsing dbtropes series database to grab '%s' related info" % series_name
    if not os.path.isfile(new_series_data_filename):
        if verbose:
            print(step_name)
        with open(SERIES_DATA_FILENAME, 'r') as raw_file, open(new_series_data_filename, 'w') as series_data_file:
            for line in raw_file:
                if re.match("<http://dbtropes.org/resource/Series/" + str(series_name), line):
                    series_data_file.write(line)
    elif verbose:
        print("Skipping step: \"%s\"" % step_name)


def run_setup(series_names: List[str], verbose: bool = False) -> None:
    """
    Run dbtropes setup
    :param series_names (List[str]): Names of tv series
    :param verbose (bool): whether to print progress messages
    :return: None
    """
    parse_dbtropes(verbose)
    for series in series_names:
        prepare_data_for_given_series(series, verbose)


if __name__ == "__main__":
    series_names = ['Friends', 'Stranger Things']
    run_setup(series_names, verbose=True)
