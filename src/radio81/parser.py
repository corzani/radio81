from itertools import chain

from InquirerPy import inquirer

from argparse import Namespace, ArgumentParser

import logging

log = logging.getLogger(__name__)


def argument_parser() -> ArgumentParser:
    arg_parser = ArgumentParser(description='Radio 81 - A banal old tube radio', prog='radio81')
    arg_parser.add_argument('--id', metavar='STATION_ID', help='Play a station ')
    return arg_parser


async def select_genre(genres):
    list_genres = map(lambda genre: [genre] + list(genres[genre].sub_genres.keys()), list(genres.keys()))

    flat_list = list(chain(*list_genres))
    return await fuzzy_prompt(
        message="Select or Type a genre:",
        choices=flat_list
    )


async def select_station(stations):
    return await fuzzy_prompt(
        message="Select or Type a station:",
        choices=list(map(lambda station: {'name': station.name, 'value': station}, stations))
    )


async def fuzzy_prompt(**args):
    selected = inquirer.fuzzy(**args)

    result = await selected.application.run_async()

    # I hope they won't add any radio/genre called 'INQUIRERPY_KEYBOARD_INTERRUPT'

    log.debug(f'On choice "{args.get("message")}" you picked "{result}"')

    if result == 'INQUIRERPY_KEYBOARD_INTERRUPT':
        return None
    else:
        return result
