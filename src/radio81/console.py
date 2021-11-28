import os
import sys

import aiohttp
import asyncio
import logging

from radio81.parser import argument_parser

log = logging.getLogger(__name__)


def logo(ver):
    log.info('')
    log.info('██████╗  █████╗ ██████╗ ██╗ ██████╗      █████╗  ██╗')
    log.info('██╔══██╗██╔══██╗██╔══██╗██║██╔═══██╗    ██╔══██╗███║')
    log.info('██████╔╝███████║██║  ██║██║██║   ██║    ╚█████╔╝╚██║')
    log.info('██╔══██╗██╔══██║██║  ██║██║██║   ██║    ██╔══██╗ ██║')
    log.info('██║  ██║██║  ██║██████╔╝██║╚██████╔╝    ╚█████╔╝ ██║')
    log.info('╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝ ╚═════╝      ╚════╝  ╚═╝')
    log.info(f'ALPHA {ver.ljust(34, " ")}quit: CTRL+C')
    log.info('Powered by SHOUTcast')
    log.info('----------------------------------------------------')


async def console_main(shoutcast_player, station_id=None):
    # This is a workaround to avoid VLC logging

    from radio81 import __version__
    from radio81.player import ShoutCastPlayer, play_station

    logo(__version__)
    player: ShoutCastPlayer = shoutcast_player

    # Should I maintain this client session open? What would it imply? I guess nothing...
    async with aiohttp.ClientSession(base_url='https://directory.shoutcast.com') as session:
        # Python is pointless in 2021... Use Kotlin instead...

        if station_id is None:
            station = await prompt_genre_and_stations(player, session)
        else:
            from radio81.genres import Station
            station = Station(name=station_id, id=station_id, url='')

        if station is None:
            log.error(f'No station selected, exiting...')
            return

        media, url = await play_station(player, session, station)

        if media is None:
            log.error(f'Error on {station.name} ({station.id}) - SKIPPED')
            return

        log.info('')
        log.info(f'Radio ID: {station.id} URL: "{url}"')
        await play_loop(media)
    # This is very bad but I can't retrieve the metachanged event from VLC
    # So... at the moment I'll stick with this solution

    # Are you serious?!?!?!? MediaMetaChanged doesn't work?
    # All examples online are with polling :(. Damn... Is it still a bug?


async def prompt_genre_and_stations(player, session):
    from radio81.genres import default_shoutcast_data
    from radio81.parser import select_genre, select_station
    from radio81.player import load_stations

    genres = default_shoutcast_data()
    player.genre = await select_genre(genres)
    stations = await load_stations(session, player.genre)
    if not stations:
        log.info(f'Wow... {player.genre} genre has no stations available. Nice pick!')
        log.info('Let me decide for you... What about Classic Rock?')
        stations = await load_stations(session, "Classic Rock")
    return await select_station(stations)


# This is an evil function for many reasons:
# PythonVlc library:
# doesn't trigger exceptions
# doesn't trigger some events like metachanged...
async def play_loop(media):
    from vlc import Meta

    current_media_title = 'Retrieving title...'

    # While true and polling... I never imagined to use those workarounds to update song titles...
    while True:
        media_title = media.get_meta(Meta.NowPlaying)
        if media_title != current_media_title and media_title is not None:
            current_media_title = media_title
            log.info(f'=> {media_title}')
        await asyncio.sleep(5)


def start():
    os.environ["VLC_VERBOSE"] = "-1"
    parsed_args = argument_parser().parse_args()
    station_id = parsed_args.id

    log_format = "%(message)s"
    logging.basicConfig(
        stream=sys.stdout,
        format=log_format,
        level=logging.INFO)

    from radio81.player import close_player
    from radio81.player import create_shoutcast_player

    async def start_radio():
        player = create_shoutcast_player()

        try:
            await console_main(player, station_id)
        finally:
            close_player(player)
        # except asyncio.CancelledError:

    try:
        asyncio.run(start_radio())
    except KeyboardInterrupt:
        log.info("CTRL+C Pressed, are you tired of music? You should not...")
    except asyncio.exceptions.TimeoutError:
        log.error(f'Timeout occurred during request')
    except Exception as e:
        print(e)
