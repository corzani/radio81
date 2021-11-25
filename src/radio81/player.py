import dataclasses
from typing import Dict

import vlc
from vlc import Media, MediaParseFlag, MediaPlayer

from radio81.genres import Station, default_shoutcast_data


# def createShoutCastPlayerByGenre(
#         genres=default_shoutcast_data(),
#         media_player=MediaPlayer(),
#         default_genre=None,
#         default_sub_genre=None):
#     genre = next(iter(genres.values())) if default_genre is None else genres[default_genre]
#     genre = genre if default_sub_genre is None else genre.sub_genres[default_sub_genre]
#
#     return ShoutCastPlayer(
#         genres,
#         media_player,
#         genre,
#         current_genre
#     )


def createShoutCastPlayer(
        genres=default_shoutcast_data(),
        media_player=MediaPlayer(),
        genre='Rock'):
    return ShoutCastPlayer(
        genres,
        media_player,
        genre
    )


@dataclasses.dataclass
class ShoutCastPlayer:
    genres: Dict
    media_player: vlc.MediaPlayer
    genre: str


def closePlayer(shoutcast_player: ShoutCastPlayer):
    shoutcast_player.media_player.release()


def play_stream(shoutcast_player: ShoutCastPlayer, url):
    # This is temporary, I wouldn't execute play and stop within this function

    media_player = shoutcast_player.media_player

    media = Media(url)
    media.parse_with_options(MediaParseFlag.network, 0)
    media_player.stop()
    media_player.set_media(media)
    media.parse_with_options(1, 0)  # Why???!?!? Do I have to set up the parsing option for every media?
    media_player.play()

    return media


async def get_genre_stations(session, genre):
    async with session.post('/Home/BrowseByGenre',
                            data={'genrename': genre}, timeout=5) as resp:
        return await resp.json()


async def get_station_url(session, station_id):
    async with session.post('/Player/GetStreamUrl',
                            data={"station": station_id}, timeout=5) as resp:
        return await resp.json()


async def load_stations(session, shoutcast_player: ShoutCastPlayer, genre):
    shoutcast_player.currentGenreStations = map(lambda station: Station(name=station['Name'], id=station['ID'], url=''),
                                                await get_genre_stations(session, genre))
    return shoutcast_player.currentGenreStations


async def play_station(shoutcast_player: ShoutCastPlayer, session, station):
    try:
        url = await get_station_url(session, station.id) if station.url == '' else station.url

        media = play_stream(shoutcast_player, url)

        return media, url
    except Exception as e:
        print(e)
        return None
