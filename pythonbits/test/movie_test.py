# encoding: utf-8
from mock import patch, MagicMock
from nose.tools import raises
from StringIO import StringIO
import re

from pythonbits.movie import (Movie, lookup_movie,
                              MovieLookUpFailed)


sample_movies_list = [{'title': 'x', 'year': '1'},
                      {'title': 'x', 'year': '123'}]


@patch('imdbpie.Imdb.search_for_title', return_value=sample_movies_list)
def test_movie_list_created_with_appropriate_length(mock):
    l = lookup_movie('example')
    assert l.movies == sample_movies_list
    assert len(l) == 2


@patch('imdbpie.Imdb.search_for_title', return_value=sample_movies_list)
def test_movie_link_print_movies_prints_appropriate_number_of_lines(movie):
    l = lookup_movie('example')
    with patch('sys.stdout', new=StringIO()) as out:
        l.print_movies()

    output = out.getvalue().strip()
    assert output.startswith('1')
    assert len(output.split('\n')) == 2
    for line in output.split('\n'):
        assert re.match(r'\d+\: .*? \(\d+\)', line)


@raises(MovieLookUpFailed)
@patch('imdbpie.Imdb.search_for_title', return_value=[])
def test_lookup_raises_error_when_no_matches(mock):
    lookup_movie('example')


def test_summary_returns_unicode_object():
    m = MagicMock()

    movie = Movie({})
    with patch.object(movie, '_info', m):
        output = movie.summary

    assert 'Year' in output
    assert '[/quote]' in output
    assert isinstance(output, unicode)
