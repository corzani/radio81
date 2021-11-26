import os

import aiohttp
import asyncio


def logo(ver):
    print('')
    print('██████╗  █████╗ ██████╗ ██╗ ██████╗      █████╗  ██╗')
    print('██╔══██╗██╔══██╗██╔══██╗██║██╔═══██╗    ██╔══██╗███║')
    print('██████╔╝███████║██║  ██║██║██║   ██║    ╚█████╔╝╚██║')
    print('██╔══██╗██╔══██║██║  ██║██║██║   ██║    ██╔══██╗ ██║')
    print('██║  ██║██║  ██║██████╔╝██║╚██████╔╝    ╚█████╔╝ ██║')
    print('╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝ ╚═════╝      ╚════╝  ╚═╝')
    print(f'ALPHA {ver}                    quit: CTRL+C')
    print('----------------------------------------------------')


async def console_main(shoutcast_player):
    # This is a workaround to exec
    from radio81.genres import default_shoutcast_data
    from radio81.parser import select_genre, select_station
    from radio81.player import load_stations, ShoutCastPlayer, play_station, close_player, create_shoutcast_player
    from radio81 import __version__

    logo(__version__)
    player: ShoutCastPlayer = shoutcast_player
    genres = default_shoutcast_data()

    # Should I maintain this client session open? What would it imply? I guess nothing...
    async with aiohttp.ClientSession(base_url='https://directory.shoutcast.com') as session:
        # Python is pointless in 2021... Use Kotlin instead...
        station = ''
        try:
            player.genre = await select_genre(genres)
            stations = await load_stations(session, player.genre)

            if not stations:
                print(f'Wow... {player.genre} genre has no stations available. Nice pick!')
                print('Let me decide for you... What about Classic Rock?')
                stations = await load_stations(session, "Classic Rock")

            station = await select_station(stations)
        except Exception as e:
            print(e)
            return

        media, url = await play_station(player, session, station)

        if media is None:
            print(f'Error on {station.name} ({station.id}) - SKIPPED')
            return

        await play_loop(media)
    # This is very bad but I can't retrieve the metachanged event from VLC
    # So... at the moment I'll stick with this solution

    # Are you serious?!?!?!? MediaMetaChanged doesn't work?
    # All examples online are with polling :(. Damn... Is it still a bug?


# This is an evil function for many reasons:
# PythonVlc library:
# doesn't trigger exceptions
# doesn't trigger some events like metachanged...
async def play_loop(media):
    from vlc import Meta

    while True:
        media_title = media.get_meta(Meta.NowPlaying)
        title = media_title if media_title is not None else 'Retrieving title...'
        # There is something better than this to handling one line refreshing,
        # even ncurses. But be patient it's an MVP...
        print(f'=> {title}'.ljust(70, ' '), end='\r')
        await asyncio.sleep(5)


def start():
    os.environ["VLC_VERBOSE"] = "-1"

    from radio81.player import close_player
    from radio81.player import create_shoutcast_player

    async def start_radio():
        player = create_shoutcast_player()

        try:
            await console_main(player)
        finally:
            close_player(player)
        # except asyncio.CancelledError:

    asyncio.run(start_radio())
