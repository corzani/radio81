from dataclasses import dataclass

from typing import List, Dict


@dataclass
class Station:
    name: str
    id: str
    url: str


@dataclass
class SubGenre:
    name: str
    stations: List[Station]
    last_idx: int


@dataclass
class Genre(SubGenre):
    sub_genres: Dict[str, SubGenre]


@dataclass()
class Shoutcast(Dict[str, Genre]):
    pass


def create_shoutcast_struct(data):
    return Genre(name=data['name'],
                 stations=[],
                 last_idx=0,
                 sub_genres={genre: SubGenre(name=genre, stations=[], last_idx=0) for genre in
                             data['sub_genres']})


def default_shoutcast_data():
    return {genre.name: genre for genre in map(create_shoutcast_struct, shoutcast_genres)}


shoutcast_genres = [
    {
        'name': "Alternative",
        'sub_genres': [
            "Adult Alternative",
            "Britpop",
            "Classic Alternative",
            "College",
            "Dancepunk",
            "Dream Pop",
            "Emo",
            "Goth",
            "Grunge",
            "Hardcore",
            "Indie Pop",
            "Indie Rock",
            "Industrial",
            "LoFi",
            "Modern Rock",
            "New Wave",
            "Noise Pop",
            "Post Punk",
            "Power Pop",
            "Punk",
            "Ska",
            "Xtreme"]},
    {'name': "Blues",
     'sub_genres': ["Acoustic Blues",
                    "Chicago Blues",
                    "Contemporary Blues",
                    "Country Blues",
                    "Delta Blues",
                    "Electric Blues",
                    "Cajun and Zydeco"]},
    {'name': "Classical",
     'sub_genres': [
         "Baroque",
         "Chamber",
         "Choral",
         "Classical Period",
         "Early Classical",
         "Impressionist",
         "Modern",
         "Opera",
         "Piano",
         "Romantic",
         "Symphony"
     ]},
    {'name': "Country",
     'sub_genres': [
         "Alt Country",
         "Americana",
         "Bluegrass",
         "Classic Country",
         "Contemporary Bluegrass",
         "Contemporary Country",
         "Honky Tonk",
         "Hot Country Hits",
         "Western"]},
    {
        'name': "Easy Listening",
        'sub_genres': [
            "Exotica",
            "Light Rock",
            "Lounge",
            "Orchestral Pop",
            "Polka",
            "Space Age Pop"]},
    {
        'name': "Electronic",
        'sub_genres': [
            "Acid House",
            "Ambient",
            "Big Beat",
            "Breakbeat",
            "Dance",
            "Demo",
            "Disco",
            "Downtempo",
            "Drum and Bass",
            "Electro",
            "Garage",
            "Hard House",
            "House",
            "IDM",
            "Jungle",
            "Progressive",
            "Techno",
            "Trance",
            "Tribal",
            "Trip Hop",
            "Dubstep"
        ]},
    {
        'name': "Folk",
        'sub_genres': [
            "Alternative Folk",
            "Contemporary Folk",
            "Folk Rock",
            "New Acoustic",
            "Traditional Folk",
            "World Folk",
            "Old Time"
        ]
    }, {
        'name': "Themes",
        'sub_genres': [
            "Adult",
            "Best Of",
            "Chill",
            "Eclectic",
            "Experimental",
            "Female",
            "Heartache",
            "Instrumental",
            "LGBT",
            "Love and Romance",
            "Party Mix",
            "Patriotic",
            "Rainy Day Mix",
            "Reality",
            "Sexy",
            "Shuffle",
            "Travel Mix",
            "Tribute",
            "Trippy",
            "Work Mix"]
    }, {
        'name': "Rap",
        'sub_genres': [
            "Alternative Rap",
            "Dirty South",
            "East Coast Rap",
            "Freestyle",
            "Hip Hop",
            "Gangsta Rap",
            "Mixtapes",
            "Old School",
            "Turntablism",
            "Underground Hip Hop",
            "West Coast Rap"
        ]
    }, {
        'name': "Inspirational",
        'sub_genres': [
            "Christian",
            "Christian Metal",
            "Christian Rap",
            "Christian Rock",
            "Classic Christian",
            "Contemporary Gospel",
            "Gospel",
            "Praise and Worship",
            "Sermons and Services",
            "Southern Gospel",
            "Traditional Gospel"
        ]
    }, {
        'name': "International",
        'sub_genres': [
            "African",
            "Arabic",
            "Asian",
            "Bollywood",
            "Brazilian",
            "Caribbean",
            "Celtic",
            "Chinese",
            "European",
            "Filipino",
            "French",
            "Greek",
            "Hawaiian and Pacific",
            "Hindi",
            "Indian",
            "Japanese",
            "Hebrew",
            "Klezmer",
            "Korean",
            "Mediterranean",
            "Middle Eastern",
            "North American",
            "Russian",
            "Soca",
            "South American",
            "Tamil",
            "Worldbeat",
            "Zouk",
            "German",
            "Turkish",
            "Islamic",
            "Afrikaans",
            "Creole"]
    }, {
        'name': "Jazz",
        'sub_genres': [
            "Acid Jazz",
            "Avant Garde",
            "Big Band",
            "Bop",
            "Classic Jazz",
            "Cool Jazz",
            "Fusion",
            "Hard Bop",
            "Latin Jazz",
            "Smooth Jazz",
            "Swing",
            "Vocal Jazz",
            "World Fusion"]
    }, {
        'name': "Latin",
        'sub_genres': [
            "Bachata",
            "Banda",
            "Bossa Nova",
            "Cumbia",
            "Latin Dance",
            "Latin Pop",
            "Latin Rap and Hip Hop",
            "Latin Rock",
            "Mariachi",
            "Merengue",
            "Ranchera",
            "Reggaeton",
            "Regional Mexican",
            "Salsa",
            "Tango",
            "Tejano",
            "Tropicalia",
            "Flamenco",
            "Samba"]
    }, {
        'name': "Metal",
        'sub_genres': [
            "Black Metal",
            "Classic Metal",
            "Extreme Metal",
            "Grindcore",
            "Hair Metal",
            "Heavy Metal",
            "Metalcore",
            "Power Metal",
            "Progressive Metal",
            "Rap Metal",
            "Death Metal",
            "Thrash Metal"]
    }, {
        'name': "New Age",
        'sub_genres': [
            "Environmental",
            "Ethnic Fusion",
            "Healing",
            "Meditation",
            "Spiritual"]
    }, {
        'name': "Decades",
        'sub_genres': [
            "30s",
            "40s",
            "50s",
            "60s",
            "70s",
            "80s",
            "90s",
            "00s"]
    }, {
        'name': "Pop",
        'sub_genres': [
            "Adult Contemporary",
            "Barbershop",
            "Bubblegum Pop",
            "Dance Pop",
            "Idols",
            "Oldies",
            "JPOP",
            "Soft Rock",
            "Teen Pop",
            "Top 40",
            "World Pop",
            "KPOP"]
    }, {
        'name': "R&B and Urban",
        'sub_genres': [
            "Classic R&B",
            "Contemporary R&B",
            "Doo Wop",
            "Funk",
            "Motown",
            "Neo Soul",
            "Quiet Storm",
            "Soul",
            "Urban Contemporary"]
    }, {
        'name': "Reggae",
        'sub_genres': [
            "Contemporary Reggae",
            "Dancehall",
            "Dub",
            "Pop Reggae",
            "Ragga",
            "Rock Steady",
            "Reggae Roots"]
    }, {
        'name': "Rock",
        'sub_genres': [
            "Adult Album Alternative",
            "British Invasion",
            "Classic Rock",
            "Garage Rock",
            "Glam",
            "Hard Rock",
            "Jam Bands",
            "Piano Rock",
            "Prog Rock",
            "Psychedelic",
            "Rock & Roll",
            "Rockabilly",
            "Singer and Songwriter",
            "Surf",
            "JROCK",
            "Celtic Rock"]
    }, {
        'name': "Seasonal and Holiday",
        'sub_genres': [
            "Anniversary",
            "Birthday",
            "Christmas",
            "Halloween",
            "Hanukkah",
            "Honeymoon",
            "Kwanzaa",
            "Valentine",
            "Wedding",
            "Winter"]
    }, {
        'name': "Soundtracks",
        'sub_genres': [
            "Anime",
            "Kids",
            "Original Score",
            "Showtunes",
            "Video Game Music"]
    }, {
        'name': "Talk",
        'sub_genres': [
            "Comedy",
            "Community",
            "Educational",
            "Government",
            "News",
            "Old Time Radio",
            "Other Talk",
            "Political",
            "Scanner",
            "Spoken Word",
            "Sports",
            "Technology",
            "BlogTalk",
        ]
    }, {
        'name': "Misc",
        'sub_genres': []
    }, {
        'name': "Public Radio",
        'sub_genres': [
            "News",
            "Talk",
            "College",
            "Sports",
            "Weather",
        ]
    }]
