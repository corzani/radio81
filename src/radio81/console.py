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
    from vlc import Meta

    logo(__version__)
    player: ShoutCastPlayer = shoutcast_player
    genres = default_shoutcast_data()

    # Should I maintain this client session open? What would it imply? I guess nothing...
    async with aiohttp.ClientSession(base_url='https://directory.shoutcast.com') as session:
        player.genre = await select_genre(genres)
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
                # There is something better than this to handling one line refreshing,
                # even ncurses. But be patient it's an MVP...
                print(f'=> {title}'.ljust(70, ' '), end='\r')
                await asyncio.sleep(5)

        # Are you serious?!?!?!? MediaMetaChanged doesn't work?
        # All examples online are with polling :(. Damn... Is it still a bug?

        # print("Press enter for the next Rock station :). Don't you like classic rock? Go back to school...")

    # At the moment this is almost unreachable apart if you pass all the current genre stations :)
    close_player(player)


def start():
    os.environ["VLC_VERBOSE"] = "-1"

    from radio81.player import close_player
    from radio81.player import create_shoutcast_player

    async def start_radio():
        player = create_shoutcast_player()

        try:
            await console_main(player)
        except asyncio.CancelledError:
            close_player(player)

    asyncio.run(start_radio())
