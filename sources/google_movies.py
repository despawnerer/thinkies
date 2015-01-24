from urllib.parse import urljoin, urlencode, urlsplit, parse_qs
from funcy import cached_property, collecting, first
from collections import namedtuple
from operator import methodcaller

from lxml import html
from requests import Session


class GoogleMovies:
    def __init__(self, location, day_offset=0):
        self.location = location
        self.day_offset = day_offset
        self.session = Session()

    def get_movies(self):
        divs = self.xpath('//div[@class="theater"]//div[@class="movie"]')
        return set(map(self._build_movie_from_div, divs))

    def get_theaters(self):
        divs = self.xpath('//div[@class="theater"]')
        return set(map(self._build_theater_from_div, divs))

    def get_theaters_for_movie(self, movie):
        divs = self.xpath('//div[@class="theater"]'
                          '[.//a[contains(@href,"mid=%s")]]'
                          % movie.mid)
        return set(map(self._build_theater_from_div, divs))

    def xpath(self, *args):
        return sum(map(methodcaller('xpath', *args), self.trees), [])

    @cached_property
    @collecting
    def trees(self):
        params = {'near': self.location, 'date': self.day_offset}
        base_url = 'http://google.com/movies?%s' % urlencode(params)

        response = self.session.get(base_url)
        tree = html.fromstring(response.text)
        yield tree

        other_page_urls = self._get_pagination_urls(tree)
        for url in other_page_urls:
            response = self.session.get(urljoin(base_url, url))
            yield html.fromstring(response.text)

    def _get_pagination_urls(self, tree):
        return tree.xpath('//div[@id="navbar"]//table//td/a/@href')

    def _build_movie_from_div(self, div):
        title_link = first(div.xpath('div[@class="name"]/a'))
        imdb_link = first(div.xpath('span[@class="info"]/a[.="IMDb"]'))

        title = title_link.text
        mid = mid_from_google_movies_url(title_link.attrib['href'])
        imdb_id = (
            imdb_id_from_google_movies_url(imdb_link.attrib['href'])
            if imdb_link is not None else None)
        return Movie(title, mid, imdb_id)

    def _build_theater_from_div(self, div):
        h2 = first(div.xpath('div[@class="desc"]/h2[@class="name"]'))
        if h2 is not None:
            title_link = first(h2.xpath('a'))
            if title_link is not None:
                return title_link.text
            else:
                return h2.text

        raise ValueError(
            "Movies can't exist without theaters. Something's wrong.")


# data classes

_Movie = namedtuple('_Movie', ('title', 'mid', 'imdb_id'))


class Movie(_Movie):
    def __str__(self):
        return self.title

    def __eq__(self, other):
        return isinstance(other, Movie) and hash(other) == hash(self)

    def __hash__(self):
        return hash(self.mid)


# helpers

def mid_from_google_movies_url(url):
    return get_param_from_url(url, 'mid')


def imdb_id_from_google_movies_url(url):
    imdb_url = get_param_from_url(url, 'q')
    imdb_path = urlsplit(imdb_url).path
    return imdb_path.strip('/')[len('title/'):]


def get_param_from_url(url, param):
    query_string = urlsplit(url).query
    params = parse_qs(query_string)
    return params.get(param)[0]
