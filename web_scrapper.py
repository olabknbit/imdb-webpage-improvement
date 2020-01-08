import requests
from bs4 import BeautifulSoup as bs

from query_dbtropes import retrieve_tropes
from send_sparql_query import get_network_name, get_series_actors

directory = 'web_pages/'


def grab_original_title(soup: bs):
    if (original_title := soup.find("div", attrs={"class": "originalTitle"})) is not None:
        original_title = original_title.text
        index = original_title.find(" (original title)")
        series_name = original_title[:index]
        return series_name
    return None


def add_tropes_info(soup, series_name):
    tropes = retrieve_tropes(series_name)
    if tropes:
        plot_summary_tag = soup.find(class_="plot_summary")
        credit_summary_item = soup.new_tag("div")
        credit_summary_item['class'] = "credit_summary_item"

        tropes_tag = soup.new_tag("h4")
        tropes_tag['class'] = "inline"
        tropes_tag.string = "Tropes:"
        credit_summary_item.append(tropes_tag)

        t = tropes[0]
        tropes_name_tag = soup.new_tag("a", href=t[0])
        tropes_name_tag.string = t[1]
        credit_summary_item.append(tropes_name_tag)
        plot_summary_tag.append(credit_summary_item)
        print(plot_summary_tag)


def improve_webpage(url: str):
    response = requests.get(url)

    soup = bs(response.text, 'html.parser')
    # print(response.text)

    full_title = soup.find("title").text
    if not (series_name := grab_original_title(soup)):
        index = full_title.find(" (TV Series")
        series_name = full_title[:index]

    print(full_title, "XXX", series_name)
    net_name = get_network_name(series_name)
    print("network name:", net_name)
    if net_name:
        plot_summary_tag = soup.find(class_="plot_summary")
        credit_summary_item = soup.new_tag("div")
        credit_summary_item['class'] = "credit_summary_item"

        network_tag = soup.new_tag("h4")
        network_tag['class'] = "inline"
        network_tag.string = "Network:"
        credit_summary_item.append(network_tag)

        network_name_tag = soup.new_tag("a", href=net_name)
        network_name_tag.string = net_name.split('/')[-1]
        credit_summary_item.append(network_name_tag)

        plot_summary_tag.append(credit_summary_item)

        # print(plot_summary_tag)

    actors = get_series_actors(series_name)
    print("actors:", [a.to_string() for a in actors])
    if len(actors) > 0:
        plot_summary_tag = soup.find(class_="plot_summary")
        credit_summary_item = soup.new_tag("div")
        credit_summary_item['class'] = "credit_summary_item"

        actors_tag = soup.new_tag("h4")
        actors_tag['class'] = "inline"
        actors_tag.string = "Actors:"
        credit_summary_item.append(actors_tag)

        for actor in actors:
            actor_name_tag = soup.new_tag("a", href=actor.uri)
            actor_name_tag.string = actor.name
            credit_summary_item.append(actor_name_tag)

        plot_summary_tag.append(credit_summary_item)

    add_tropes_info(soup, series_name)

    with open(directory + full_title + ".htm", 'w') as f:
        f.write(soup.prettify())


def main():
    urls = [
        'https://www.imdb.com/title/tt2261227/?ref_=fn_al_tt_1',
        'https://www.imdb.com/title/tt2575988/?ref_=nv_sr_srsg_0',
        'https://www.imdb.com/title/tt11194508/?ref_=nv_sr_srsg_0',
        'https://www.imdb.com/title/tt0397442/?ref_=fn_al_tt_1',
        'https://www.imdb.com/title/tt4574334/?ref_=fn_al_tt_1',
        'https://www.imdb.com/title/tt5179408/?ref_=fn_al_tt_1',
        'https://www.imdb.com/title/tt0108778/?ref_=fn_al_tt_1'
    ]
    import os
    if not os.path.exists(directory):
        os.makedirs(directory)

    for url in urls:
        improve_webpage(url)


if __name__ == "__main__":
    main()
