from itertools import chain

from InquirerPy import inquirer


async def select_genre(genres):
    list_genres = map(lambda genre: [genre] + list(genres[genre].sub_genres.keys()), list(genres.keys()))

    flat_list = list(chain(*list_genres))
    selected = inquirer.fuzzy(
        message="Select or Type a genre:",
        choices=flat_list
    )

    result = await selected.application.run_async()
    return result


async def select_station(stations):
    selected = inquirer.fuzzy(
        message="Select or Type a station:",
        choices=list(map(lambda station: {'name': station.name, 'value': station}, stations))
    )

    result = await selected.application.run_async()
    return result
