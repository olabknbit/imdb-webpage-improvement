import requests
from bs4 import BeautifulSoup as bs

url = 'https://www.imdb.com/title/tt4574334/?ref_=fn_al_tt_1'
response = requests.get(url)
soup = bs(response.text, 'html.parser')

el = soup.find(text="Creators:")
creator_tags = el.parent.parent.find_all('a')
print(creator_tags)
for creator_tag in creator_tags:
    creator_tag.string = 'F'

with open("file.html", 'w') as f:
    f.write(soup.prettify())
