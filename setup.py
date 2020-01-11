import re


def parse_dbtropes():
    series_data = open('series_data.nt', 'w')
    with open('dbtropes.nt') as rawfile:
        for line in rawfile:
            if re.match("<http://dbtropes.org/resource/Series/", line):
                series_data.write(line)
        series_data.close()


if __name__ == "__main__":
    parse_dbtropes()