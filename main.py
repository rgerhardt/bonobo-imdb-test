import bonobo

from helpers import *

if __name__ == '__main__':

    graph = bonobo.Graph(
        UrlSoupPageFetcher('https://www.imdb.com/chart/top?ref_=nv_mv_250_6'),
        ChartPageParser(),
        MovieRankTranform(),
        DictCsvWriter(
            'movies.csv',
            fields=('rank', 'title_id', 'title', 'year', 'rating', 'link')
        ),
    )
    bonobo.run(graph)