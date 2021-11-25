from vlc import Meta

import aiohttp
import asyncio

from radio81.genres import default_shoutcast_data
from radio81.parser import select_genre, select_station
from radio81.player import load_stations, ShoutCastPlayer, play_station, closePlayer, createShoutCastPlayer
from radio81 import __version__


def logo():
    print('')
    print('██████╗  █████╗ ██████╗ ██╗ ██████╗      █████╗  ██╗')
    print('██╔══██╗██╔══██╗██╔══██╗██║██╔═══██╗    ██╔══██╗███║')
    print('██████╔╝███████║██║  ██║██║██║   ██║    ╚█████╔╝╚██║')
    print('██╔══██╗██╔══██║██║  ██║██║██║   ██║    ██╔══██╗ ██║')
    print('██║  ██║██║  ██║██████╔╝██║╚██████╔╝    ╚█████╔╝ ██║')
    print('╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝ ╚═════╝      ╚════╝  ╚═╝')
    print(f'ALPHA {__version__}                    quit: CTRL+C')
    print('----------------------------------------------------')


async def console_main(player: ShoutCastPlayer):
    logo()
    genres = default_shoutcast_data()
    selected_genre = await select_genre(genres)
    player.genre = selected_genre

    # Should I maintain this client session open? What would it imply? I guess nothing...
    async with aiohttp.ClientSession(base_url='https://directory.shoutcast.com') as session:
        stations = await load_stations(session, player, player.genre)
        station = await select_station(stations)

        try:
            media, url = await play_station(player, session, station)
        except Exception as e:
            print(e)
            media = None

        if media is None:
            print(f'Error on {station} ({station.id}) - SKIPPED')
        else:

            # This is very bad but I can't retrieve the metachanged event from VLC
            # So... at the moment I'll stick with this solution
            while True:
                media_title = media.get_meta(Meta.NowPlaying)
                title = media_title if media_title is not None else 'Retrieving title...'
                # It must be something better than this, if not the size of the window would change the behaviour
                print(f'=> {title}', end='\r')
                await asyncio.sleep(5)

        # Are you serious?!?!?!? MediaMetaChanged doesn't work?
        # All examples online are with polling :(. Damn... Is it still a bug?

        # print("Press enter for the next Rock station :). Don't you like classic rock? Go back to school...")

    # At the moment this is almost unreachable apart if you pass all the current genre stations :)
    closePlayer(player)


def start():
    async def start_radio():
        player = createShoutCastPlayer()

        try:
            await console_main(player)
        except asyncio.CancelledError:
            closePlayer(player)

    asyncio.run(start_radio())
