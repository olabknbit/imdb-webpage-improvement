import requests
from bs4 import BeautifulSoup as bs

from send_sparql_query import get_network_name


def grab_original_title(soup: bs):
    if (original_title := soup.find("div", attrs={"class": "originalTitle"})) is not None:
        original_title = original_title.text
        index = original_title.find(" (original title)")
        series_name = original_title[:index]
        return series_name
    return None


def improve_webpage(url: str):
    response = requests.get(url)

    soup = bs(response.text, 'html.parser')
    # print(response.text)

    full_title = soup.find("title").text
    if not (series_name:= grab_original_title(soup)):

        index = full_title.find(" (TV Series")
        series_name = full_title[:index]

    print(full_title, "XXX", series_name)
    net_name = get_network_name(series_name)
    print("network name:", net_name)
    if net_name:
        el = soup.find(text="Creators:")
        plot_summary_tag = el.parent.parent.parent
        network_tag = soup.new_tag("h4")
        network_tag['class'] = "inline"
        network_tag.string = "Network:"
        plot_summary_tag.append(network_tag)

        network_name_tag = soup.new_tag("a", href=net_name)
        network_name_tag.string = net_name.split('/')[-1]
        network_tag.append(network_name_tag)
        print(plot_summary_tag)

    with open('web_pages/' + full_title + ".htm", 'w') as f:
        f.write(soup.prettify())


def main():
    urls = [
        'https://www.imdb.com/title/tt0397442/?ref_=fn_al_tt_1',
        'https://www.imdb.com/title/tt4574334/?ref_=fn_al_tt_1',
        'https://www.imdb.com/title/tt5179408/?ref_=fn_al_tt_1',
        'https://www.imdb.com/title/tt0108778/?ref_=fn_al_tt_1'
    ]
    for url in urls:
        improve_webpage(url)


if __name__ == "__main__":
    main()
