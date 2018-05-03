import csv
import re

from bs4 import BeautifulSoup as bs

import bonobo
from bonobo.config.processors import use_context

import requests


class Top250MoviesPageExtractor():

    URL = 'https://www.imdb.com/chart/top?ref_=nv_mv_250_6'

    def __init__(self):
        resp = requests.get(self.URL)
        if resp.status_code != 200:
            raise Exception('Error while fetching IMDB page!')

        self.page = bs(resp.text, 'html.parser')

    def read(self, *args, **kwargs):
        movie_trs = self.find_movie_table_rows()
        for tr in movie_trs:
            rank, title, year = self.extract_basic_info(tr)
            rating = self.extract_rating(tr)
            link = self.extract_movie_link(tr)

            yield {
                'rank':rank,
                'title':title,
                'year': year,
                'rating': rating,
                'link': link
            }

    def find_movie_table_rows(self):
        tbody = self.page.find('tbody', class_='lister-list')
        return tbody.find_all('tr')

    def extract_movie_link(self, movie_row):
        td = movie_row.find('td', class_='titleColumn')
        return td.find('a')['href']

    def extract_basic_info(self, movie_row):
        td = movie_row.find('td', class_='titleColumn')
        return list(td.stripped_strings)

    def extract_rating(self, movie_row):
        td = movie_row.find('td', class_='ratingColumn imdbRating')
        return td.text

    __call__ = read


class MovieTranform():

    def transform(self, movie):
        movie['rank'] = movie['rank'].replace('.', '')
        movie['title'] = movie['title'].upper()
        movie['year'] = movie['year'].replace('(', '').replace(')', '')
        movie['rating'] = movie['rating'].replace('\n', '')
        movie['link'] = self.parse_link(movie['link'])

        yield movie

    def parse_link(self, link):
        relative_link = re.search(r'/title/[a-z0-9]*/', link).group(0)
        return "https://www.imdb.com{}".format(relative_link)

    __call__ = transform


@use_context
class DictCsvWriter(bonobo.FileWriter):

    fields = ('rank', 'title', 'year', 'rating', 'link')

    def writer_factory(self, file):
        return csv.DictWriter(file, fieldnames=self.fields)

    def write(self, file, context, data, fs):
        context.setdefault('lineno', 0)

        if not context.lineno:
            context.writer = self.writer_factory(file)
            context.writer.writeheader()

        context.writer.writerow(data)

        context.lineno += 1

        return bonobo.constants.NOT_MODIFIED

    __call__ = write