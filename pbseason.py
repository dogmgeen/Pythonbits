#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SYNOPSIS

	python pbseason.py [-h,--help] [-v,--verbose]


DESCRIPTION

	Concisely describe the purpose this script serves.


ARGUMENTS

	-h, --help		show this help message and exit
	-v, --verbose		verbose output


AUTHOR

	tori@bB

"""
from pythonbits import utils

__appname__ = "pbseason"
__author__ = "tori@bB"
__version__ = (3, 0, '0-alpha')
__version_str__ = '.'.join(str(x) for x in __version__)
__indev__ = True

import argparse
from datetime import datetime
import sys
import os
import logging

logger = logging.getLogger(__appname__)


def main(args):
    # Retrieve show title from TVDB, IMDB, and Wikipedia if it exists.

    # Compute the sample screenshots.

    # Compute the mediainfo for each episode.

    # Create the Bittorrent file.
    pass


def setup_logger(args):
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    # todo: place them in a log directory, or add the time to the log's
    # filename, or append to pre-existing log
    log_file = os.path.join('/tmp', __appname__ + '.log')
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()

    if args.verbose:
        ch.setLevel(logging.DEBUG)
    else:
        ch.setLevel(logging.INFO)

    # create formatter and add it to the handlers
    line_numbers_and_function_name = logging.Formatter(
        "%(levelname)s [%(filename)s:%(lineno)s - %(funcName)20s() ]"
        "%(message)s")
    fh.setFormatter(line_numbers_and_function_name)
    ch.setFormatter(line_numbers_and_function_name)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)


def get_arguments():
    parser = argparse.ArgumentParser(
        description="Description printed to command-line if -h is called."
    )
    # during development, I set default to False so I don't have to keep
    # calling this with -v
    parser.add_argument('-v', '--verbose', action='store_true',
                        default=__indev__, help='verbose output')
    parser.add_argument('-P', '--season', dest='season_number',
                        type=int,
                        help='Season number')
    parser.add_argument('-T', '--title', dest='show_title',
                        required=True,
                        help='Show title')
    parser.add_argument('-N', '--num-screenshots', dest='screenshot_count',
                        type=int, default=2,
                        help='Number of screenshots to create (default: 2)')
    parser.add_argument('-o', '--output-dir', dest='output_directory',
                        type=utils.existing_directory,
                        default=utils.existing_directory('.'),
                        help='Directory to output screenshots, description'
                             ' text, and torrent file')
    parser.add_argument('season_directory', metavar='SEASON_DIRECTORY',
                        type=utils.existing_directory,
                        help='Directory containing the episodes for'
                             ' this season')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    try:
        start_time = datetime.now()

        args = get_arguments()
        setup_logger(args)

        # figure out which argument key is the longest so that all the
        # parameters can be printed out nicely
        logger.debug('Command-line arguments:')
        length_of_longest_key = len(max(vars(args).keys(),
                                        key=lambda k: len(k)))
        for arg in vars(args):
            value = getattr(args, arg)
            logger.debug('\t{argument_key}:\t{value}'.format(
                argument_key=arg.rjust(length_of_longest_key, ' '),
                value=value))

        logger.debug(start_time)

        main(args)

        finish_time = datetime.now()
        logger.debug(finish_time)
        logger.debug('Execution time: {time}'.format(
            time=(finish_time - start_time)
        ))
        logger.debug("#" * 20 + " END EXECUTION " + "#" * 20)

        sys.exit(0)

    except KeyboardInterrupt as e:  # Ctrl-C
        raise e

    except SystemExit as e:  # sys.exit()
        raise e

    except Exception as e:
        logger.exception("Something happened and I don't know what to do D:")
        sys.exit(1)
