# imdb-webpage-improvement

Add more information to imdb webpages of TV series.
`web_scrapper.py` adds additional information (like Network name) to the webpage. The result can be seen in the `web_pages' dir.

## Requirements
You need Python 3.8 or later to run imdb-webpage-improvement. You can have multiple Python versions (2.x and 3.x) installed on the same system without problems.

In Ubuntu, Mint and Debian you can install Python 3 like this:

```bash
$ sudo apt-get install python3.8 python3.8-pip python3.8-venv
```

For other Linux flavors, macOS and Windows, packages are available at

http://www.python.org/getit/


You need to install the required packages. You can do that by running
```bash
$ pip3.8 install -r requirements.txt
```

In this project we're using WikiData. On some OSes (tested on MacOS) you need to install required certificates.
Please do that by running:
```bash
$ python install_certificates.py
``` 

## Quick start
imdb-webpage-improvement can be run with:
```bash
$ python3.8 web_scrapper.py
```

### Working with DBTropes

Please download DBTropes here http://dbtropes.org/static/dbtropes.zip.
Then please unpack the files to the main directory and rename the 'nt' file to 'dbtropes.nt'.
Run setup.py script to create missing series_data.nt file 
```bash
python setup.py
```


## TODO
1. Add doctests
2. Use other information sources than dbpedia (mentioned in documentation)
3. Info about all actors - what other movies they starred in etc.