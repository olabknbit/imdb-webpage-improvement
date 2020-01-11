import os
import re
from typing import List
from zipfile import ZipFile

import wget


def get_all_filenames(directory: str) -> List[str]:
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [f for f in listdir(directory) if isfile(join(directory, f))]
    return onlyfiles


def parse_dbtropes():
    dbtropes_zip_filename = 'dbtropes.zip'
    dbtropes_dir = "dbtropes"
    dbtropes_filename = os.path.join(dbtropes_dir, "dbtropes.nt")

    # Download DbTropes resource
    url = "http://dbtropes.org/static/dbtropes.zip"
    wget.download(url, dbtropes_zip_filename)

    # Unzip DbTropes resource
    with ZipFile(dbtropes_zip_filename, "r") as f:
        f.extractall(dbtropes_dir)

    # Drop the date part from the filename
    for filename in get_all_filenames(dbtropes_dir):
        old_path = os.path.join(dbtropes_dir, filename)
        new_path = os.path.join(dbtropes_dir, filename.split('-')[0] + '.nt')
        os.rename(old_path, new_path)

    # Grab only Series relevant information from DbTropes file and save it in a separate file for faster parsing
    with open(dbtropes_filename) as raw_file, open('series_data.nt', 'w') as series_data_file:
        for line in raw_file:
            if re.match("<http://dbtropes.org/resource/Series/", line):
                series_data_file.write(line)


if __name__ == "__main__":
    parse_dbtropes()
