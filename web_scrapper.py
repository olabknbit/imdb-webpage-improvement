import requests
from bs4 import BeautifulSoup as bs

url = 'https://www.imdb.com/title/tt6257970/?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=332cb927-0342-42b3-815c-f9124e84021d&pf_rd_r=0DRP9V1ZZYC33XPZKM1T&pf_rd_s=center-1&pf_rd_t=15506&pf_rd_i=tvmeter&ref_=chttvm_tt_7'
response = requests.get(url)

soup = bs(response.text, 'html.parser')

tags = ['style', 'script', 'head', 'title', '[document]']
for t in tags:
    [s.extract() for s in soup(t)]

for el in soup.find_all()[2:]:
    text_el = el.text.strip()
    print(el.name, '\t', el.attrs, '\t', text_el)
# print(response.text)
