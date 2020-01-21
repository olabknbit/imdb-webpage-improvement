import requests
from bs4 import BeautifulSoup as bs

from actor import Actor
from query_dbtropes import retrieve_tropes
from send_sparql_query import get_info_from_dbpedia, get_series_actors
from series import Series

directory = 'web_pages/'


class WebPage():
    def __init__(self, url: str):
        self.url: str = url
        self.soup: bs = self.__init_soup__()

    def __init_soup__(self):
        response = requests.get(self.url)
        return bs(response.text, 'html.parser')

    def serialize(self, full_title):
        with open(directory + full_title + ".htm", 'w') as f:
            f.write(self.soup.prettify())

    def grab_original_title(self):
        if (original_title := self.soup.find("div", attrs={"class": "originalTitle"})) is not None:
            original_title = original_title.text
            index = original_title.find(" (original title)")
            series_name = original_title[:index]
            return series_name
        return None

    def add_new_element_to_plot_summary_tag(self, name, tags):
        plot_summary_tag = self.soup.find(class_="plot_summary")
        credit_summary_item = self.soup.new_tag("div")
        credit_summary_item['class'] = "credit_summary_item"

        tropes_tag = self.soup.new_tag("h4")
        tropes_tag['class'] = "inline"
        tropes_tag.string = name + ":"
        credit_summary_item.append(tropes_tag)

        n_tags = len(tags)
        for i, tag in enumerate(tags):
            credit_summary_item.append(tag)
            if i < n_tags - 1:
                comma = self.soup.new_string(", ")
                credit_summary_item.append(comma)

        plot_summary_tag.append(credit_summary_item)
        print(plot_summary_tag)

    def add_tropes_info(self, series_name):
        tropes = retrieve_tropes(series_name)
        if tropes:
            tags = []
            for i in range(6):
                t = tropes[i]
                tropes_name_tag = self.soup.new_tag("a", href=t[0])
                tropes_name_tag.string = t[1]
                tags.append(tropes_name_tag)
            self.add_new_element_to_plot_summary_tag("Tropes", tags)

    def get_most_important_actors(self):
        el = self.soup.find("div", attrs={"class": "article", "id": "titleCast"})
        table = el.find("table", attrs={"class": "cast_list"})
        actor_names = []
        for row in table.findAll('tr')[1:]:
            if first_column := row.find('td', attrs={"class": "primary_photo"}):
                actor_name = first_column.find("a").find("img")["title"]
                actor_names.append(actor_name)
        return actor_names

    def add_network_name_info(self, series: Series):
        net_name = series.network
        print("network name:", net_name)
        if net_name:
            network_name_tag = self.soup.new_tag("a", href=net_name)
            network_name_tag.string = net_name.split('/')[-1]
            self.add_new_element_to_plot_summary_tag("Network", [network_name_tag])

    def create_actor_row(self, actor: Actor, i: int):
        row = self.soup.new_tag("tr")
        row['class'] = 'odd' if i % 2 == 1 else "even"

        # Add actor name cell
        actor_tag = self.soup.new_tag("td")
        actor_a_tag = self.soup.new_tag("a", href=actor.get_uri())
        actor_a_tag.string = actor.name
        actor_tag.append(actor_a_tag)

        # Add actor date of birth cell
        dob_actor_tag = self.soup.new_tag("td")
        dob_actor_tag.string = actor.date_of_birth[:len("1971-04-12")] if actor.date_of_birth else ""

        # Add actor handles cell
        handles_tag = self.soup.new_tag("td")
        for website, handle in actor.handles.items():
            print(handle)
            handle_a_tag = self.soup.new_tag("a", href=handle)
            handle_a_tag.string = website
            handles_tag.append(handle_a_tag)
        # handles_tag.string = ', '

        row.append(actor_tag)
        row.append(dob_actor_tag)
        row.append(handles_tag)
        return row

    def create_table_header(self):
        header_tag = self.soup.new_tag("tr")

        # Add actor name header cell
        header_actor_tag = self.soup.new_tag("th")
        header_actor_tag.string = "Actor"

        # Add actor date of birth  header cell
        dob_actor_tag = self.soup.new_tag("th")
        dob_actor_tag.string = "Date of birth"

        # Add actor handles header cell
        handles_tag = self.soup.new_tag("th")
        handles_tag.string = "Handles"

        header_tag.append(header_actor_tag)
        header_tag.append(dob_actor_tag)
        header_tag.append(handles_tag)

        return header_tag

    def add_actors_info(self, series: Series):
        actor_names = self.get_most_important_actors()
        actors = get_series_actors(series, actor_names)
        print("actors:", [a.to_string() for a in actors])
        if len(actors) > 0:
            plot_summary_tag = self.soup.find(class_="plot_summary")
            credit_summary_item = self.soup.new_tag("div")
            credit_summary_item['class'] = "credit_summary_item"

            actors_tag = self.soup.new_tag("h4")
            actors_tag['class'] = "inline"
            actors_tag.string = ""
            credit_summary_item.append(actors_tag)

            table_tag = self.soup.new_tag("table")
            table_tag['class'] = "cast_list"

            header_tag = self.create_table_header()
            table_tag.append(header_tag)

            for i, actor in enumerate(actors):
                row = self.create_actor_row(actor=actor, i=i)
                table_tag.append(row)
            credit_summary_item.append(table_tag)
            plot_summary_tag.append(credit_summary_item)

    def improve(self):
        full_title = self.soup.find("title").text
        if not (series_name := self.grab_original_title()):
            index = full_title.find(" (TV Series")
            series_name = full_title[:index]
        print(series_name)
        from setup import prepare_data_for_given_series
        prepare_data_for_given_series(series_name, False)

        print(full_title, "XXX", series_name)
        series = get_info_from_dbpedia(series_name)
        self.add_network_name_info(series)
        self.add_tropes_info(series_name)
        self.add_actors_info(series)
        self.serialize(full_title)


def main():
    urls = [
        'https://www.imdb.com/title/tt1606375/?ref_=adv_li_tt',
        'https://www.imdb.com/title/tt1520211/?ref_=adv_li_tt',
        'https://www.imdb.com/title/tt2261227/?ref_=fn_al_tt_1',  # Altered Carbon
        'https://www.imdb.com/title/tt2575988/?ref_=nv_sr_srsg_0',  # Silicon Valley
        'https://www.imdb.com/title/tt0397442/?ref_=fn_al_tt_1',  # Plotkara
        'https://www.imdb.com/title/tt4574334/?ref_=fn_al_tt_1',  # Stranger Things
        'https://www.imdb.com/title/tt5179408/?ref_=fn_al_tt_1',  # You Me Her
        'https://www.imdb.com/title/tt0108778/?ref_=fn_al_tt_1',  # Friends
        'https://www.imdb.com/title/tt1578873/?ref_=nv_sr_srsg_0'  # Pretty Little Liars
    ]
    import os
    if not os.path.exists(directory):
        os.makedirs(directory)

    for url in urls:
        wp = WebPage(url)
        wp.improve()


if __name__ == "__main__":
    from setup import parse_dbtropes

    parse_dbtropes(verbose=False)
    main()
