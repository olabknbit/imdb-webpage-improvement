import requests
from bs4 import BeautifulSoup as bs

from send_sparql_query import get_network_name


def main():
    url = 'https://www.imdb.com/title/tt4574334/?ref_=fn_al_tt_1'
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')

    el = soup.find(text="Creators:")

    plot_summary_tag = el.parent.parent.parent
    network_tag = soup.new_tag("h4")
    network_tag['class'] = "inline"
    network_tag.string = "Network:"
    plot_summary_tag.append(network_tag)

    net_name = get_network_name()
    network_name_tag = soup.new_tag("a", href=net_name)
    network_name_tag.string = net_name.split('/')[-1]
    network_tag.append(network_name_tag)
    print(plot_summary_tag)

    creator_tags = el.parent.parent.find_all('a')
    print(creator_tags)

    with open("file.html", 'w') as f:
        f.write(soup.prettify())


if __name__ == "__main__":
    main()
