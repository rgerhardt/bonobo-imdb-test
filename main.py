import bonobo

from helpers import *

if __name__ == '__main__':

    graph = bonobo.Graph(
        Top250MoviesPageExtractor(),
        MovieTranform(),
        DictCsvWriter(
            'movies.csv',
            fields=('rank', 'title_id', 'title', 'year', 'rating', 'link')
        ),
    )
    bonobo.run(graph)