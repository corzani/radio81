import asyncio
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


def create_shoutcast_player(
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


def close_player(shoutcast_player: ShoutCastPlayer):
    shoutcast_player.media_player.release()


def play_stream(shoutcast_player: ShoutCastPlayer, url):
    # This is temporary, I wouldn't execute play and stop within this function

    media_player = shoutcast_player.media_player
    media = Media(url)
    media_player.stop()
    media_player.set_media(media)
    media_player.play()

    return media


async def get_genre_stations(session, genre):
    async with session.post('/Home/BrowseByGenre',
                            data={'genrename': genre}, timeout=5) as resp:
        print("Status:", resp.status)
        print("Content-type:", resp.headers['content-type'])
        return await resp.json()


async def get_station_url(session, station_id):
    async with session.post('/Player/GetStreamUrl',
                            data={"station": station_id}, timeout=5) as resp:
        print("Status:", resp.status)
        print("Status:", resp.real_url)
        print("Content-type:", resp.headers['content-type'])
        response = await resp.json()
        print(f"Response: {response}")

        return response


async def load_stations(session, genre):
    stations = await get_genre_stations(session, genre)
    return list(map(
        lambda station: Station(
            name=station['Name'],
            id=station['ID'],
            url=''
        ),
        filter(
            lambda station: station['Name'], stations  # Stations that have a title
        )
    ))


async def play_station(shoutcast_player: ShoutCastPlayer, session, station):
    url = await get_station_url(session, station.id) if station.url == '' else station.url

    media = play_stream(shoutcast_player, url)

    return media, url
