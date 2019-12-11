import extruct
import requests
import pprint
from w3lib.html import get_base_url

pp = pprint.PrettyPrinter(indent=2)
url = 'https://www.imdb.com/title/tt4574334/?ref_=fn_al_tt_1'
r = requests.get(url)
base_url = get_base_url(r.text, r.url)
data = extruct.extract(r.text, base_url=base_url)

pp.pprint(data)