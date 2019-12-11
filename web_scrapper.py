import requests
from bs4 import BeautifulSoup as bs
#
# url = 'https://www.imdb.com/title/tt6257970/?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=332cb927-0342-42b3-815c-f9124e84021d&pf_rd_r=0DRP9V1ZZYC33XPZKM1T&pf_rd_s=center-1&pf_rd_t=15506&pf_rd_i=tvmeter&ref_=chttvm_tt_7'
# response = requests.get(url)
#
# soup = bs(response.text, 'html.parser')
#
# # tags = ['style', 'script', 'head', 'title', '[document]']
# # for t in tags:
# #     [s.extract() for s in soup(t)]
# for i, x in enumerate(soup.find_all("meta")[6:]):
#     print(i, x)


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
