#!/usr/bin/env python
# encoding: utf-8
"""
TvdbUnitTests.py

Created by Ichabond on 2012-07-03.
"""

import unittest
from nose.tools import assert_raises

import tvdb_api

from pythonbits.TvdbParser import TVDB


def test_invalid_episode_identifier_causes_exit():
    tv = TVDB()
    tv.tvdb = None

    eps = ("S06 E01","S0601", "601", "S10", "SE10")
    for e in eps:
        assert_raises(SystemExit, tv.search, "Burn Notice", episode=e)
    assert_raises(TypeError, tv.search, "Burn Notice", episode="S01E01")  # valid


def test_search_for_show_returns_underlying_show():
    # mock out the underlying api call to tvdb_api
    tv = TVDB()
    tv.tvdb = {'Scrubs': tvdb_api.Show()}

    assert isinstance(tv.search("Scrubs"), tvdb_api.Show)
    

def test_search_for_episode_returns_underlying_episode():
    # mock out the underlying api call to tvdb_api
    tv = TVDB()
    tv.tvdb = {'Burn Notice': {6: {1: tvdb_api.Episode()}}}

    assert isinstance(tv.search("Burn Notice", episode="S06E01"), tvdb_api.Episode)


def test_search_for_season_returns_underlying_season():
    # mock out the underlying api call to tvdb_api
    tv = TVDB()
    tv.tvdb = {'Burn Notice': {6: tvdb_api.Season()}}

    assert isinstance(tv.search("Burn Notice", season=6), tvdb_api.Season)


def test_expected_keys_in_show_summary():
    tv = TVDB()
    tv.episode = None
    tv.season = None
    tv.show = mock_show_builder()

    summary = tv.summary()
    expected = ('series', 'seasons', 'network', 'rating', 'contentrating',
                'summary', 'url')
    for k in expected:
        assert k in summary


def mock_show_builder():
    show = tvdb_api.Show()
    show['seriesname'] = ''
    show['overview'] = ''
    show.__len__ = lambda self:  5
    show['network'] = 'ABC'
    show['rating'] = ''
    show['summary'] = ''
    show['contentrating'] = ''
    show['id'] = ''
    return show


def mock_episode_builder():
    episode = tvdb_api.Episode()
    episode['episodename'] = ''
    episode['director'] = ''
    episode['firstaired'] = ''
    episode['writer'] = ''
    episode['rating'] = ''
    episode['overview'] = ''
    episode['language'] = ''
    episode['seriesid'] = '1'
    episode['genre'] = ''
    episode['seasonid'] = ''
    episode['id'] = ''
    return episode


def mock_season_builder():
    season = tvdb_api.Season()
    season['overview'] = ''
    season.episodes = [mock_episode_builder(), mock_episode_builder()]


def test_expected_keys_in_episode_summary():
    tv = TVDB()
    tv.show = mock_show_builder()
    tv.season = None
    tv.episode = mock_episode_builder()
    tv.tvdb = {1: {'genre': ''}}

    summary = tv.summary()
    expected = ('title', 'director', 'aired', 'writer', 'rating', 'summary', 'language',
                'url', 'genre', 'series', 'seriessummary')
    for k in expected:
        assert k in summary


def test_expected_keys_in_season_summary():
    tv = TVDB()
    tv.show = mock_show_builder()
    tv.season = mock_season_builder()
    tv.episode = None

    summary = tv.summary()
    expected = ('series', 'url', 'summary')
    # doesn't test for the presence of episode\d keys
    for k in expected:
        assert k in summary, k
