# encoding: utf-8
import sys
from imdbpie import Imdb


class MovieLookUpFailed(Exception):
    pass


class MovieList(object):
    def __init__(self, movies):
        self.movies = movies

    def print_movies(self):
        for index, movie in enumerate(self.movies, start=1):
            print u"%s: %s (%s)" % (index,
                                    movie['title'],
                                    movie['year'])
        
    def get_selection(self):
        self.print_movies()

        while True:
            try:
                user_choice = int(raw_input(u'Select the correct movie [1-%s]: '
                                            % len(self))) - 1
            except (IndexError, ValueError):
                print >> sys.stderr, u"Bad choice!"
            else:
                if user_choice >= 0 and user_choice < len(self):
                    break
                else:
                    print >> sys.stderr, u"Bad choice!"

        return Movie(Imdb().get_title_by_id(
            self.movies[user_choice]['imdb_id']))

    def __len__(self):
        return len(self.movies)


def lookup_movie(movie_name):
    movie_matches = Imdb().search_for_title(movie_name)
    if not movie_matches:
        raise MovieLookUpFailed("No movies matching this name!")
    else:
        return MovieList(movie_matches)


class Movie(object):
    def __init__(self, imdb_info):
        self._info = imdb_info

    def __getattr__(self, key):
        return getattr(self._info, key)

    @property
    def summary(self):
        if self.directors_summary:
            directors = u"\nDirector(s): {}".format(
                u" | ".join(d.name for d in self.directors_summary))
        if self.writers_summary:
            writers = u"\nWriter(s): {}".format(
                u" | ".join(w.name for w in self.writers_summary))


        return self.MOVIE_SUMMARY_TEMPLATE.format(
            description=self.plot_outline,
            url=u"http://www.imdb.com/title/%s" % self.imdb_id,
            title=self.title,
            year=self.year,
            mpaa=self.certification,
            rating=self.rating,
            votes=self.votes,
            runtime=self.runtime,
            directors=locals().get('directors', u''),
            writers=locals().get('writers', u''))

    MOVIE_SUMMARY_TEMPLATE = \
    u"""
[b]Description[/b]
[quote]
{description}
[/quote]
[b]Information:[/b]
[quote]
IMDB Url: {url}
Title: {title}
Year: {year}
MPAA: {mpaa}
Rating: {rating}/10
Votes: {votes}
Runtime: {runtime}{directors}{writers}
[/quote]


Year: {year}


Movie Description:
{description}
"""
