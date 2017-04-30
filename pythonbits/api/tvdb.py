# Requires an authentication token
import pycountry
import tvdb_api
api = tvdb_api.Tvdb()

def get(show_title):
    show = api[show_title]
    canonical_dictionary = dict(show.data)

    # database URLs
    tvdb_url_format = 'http://thetvdb.com/?tab=series&id={id}'
    imdb_url_format = 'http://www.imdb.com/title/{imdb_id}/'

    canonical_dictionary['imdb'] = imdb_url_format.format(**show)
    canonical_dictionary['tvdb'] = tvdb_url_format.format(**show)

    show_language = pycountry.languages.get(alpha_2=show['language'])
    canonical_dictionary['language'] = show_language.name

    return canonical_dictionary