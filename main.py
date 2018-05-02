import bonobo

from helpers import *

if __name__ == '__main__':

    graph = bonobo.Graph(
        Top250MoviesPageExtractor(),
        MovieTranform(),
        DictCsvWriter(
            'movies.csv',
        ),
    )
    bonobo.run(graph)