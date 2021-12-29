import time
from pprint import pprint
import sqlalchemy
import json
import sampling

def uniq_artist (value):
        value.capitalize()
        try:
                connection.execute(f"INSERT INTO artists(artist_name)Values('{value}');")
                for item in connection.execute(f"SELECT * FROM artists;").fetchall():
                        if item[1] == value:
                                return item[0]
        except:
                for item in connection.execute(f"SELECT * FROM artists;").fetchall():
                        if item[1] == value:
                                return item[0]

def unick_genre(genres, artist_id):
        for genre in genres:
                try:
                        connection.execute(f"INSERT INTO genre(genre_name)Values('{genre}');")
                        for item in connection.execute(f"SELECT * FROM genre;").fetchall():
                                if item[1] == genre:
                                        connection.execute(f"INSERT INTO genre_lists(artist_id,genre_id)Values({artist_id},{item[0]});")
                except:
                        try:
                                for item in connection.execute(f"SELECT * FROM genre;").fetchall():
                                        if item[1] == genre:
                                                connection.execute(f"INSERT INTO genre_lists(artist_id,genre_id)Values({artist_id},{item[0]});")
                        except:
                                print(f'отношение жанр{item[0]}-артист{artist_id} уже существует')
def albums_add(albums,artist_id):
        for album in albums:
                for name in album:
                        try:
                                connection.execute(f"INSERT INTO albums(album_name,album_year) Values('{name}','{album[name][0]}');")
                                for item in connection.execute(f"SELECT * FROM albums;").fetchall():
                                        if item[1] == name:
                                                connection.execute(f"INSERT INTO albums_lists(albums_id,artist_id)Values('{item[0]}','{artist_id}');")
                        except:
                                 try:
                                         for item in connection.execute(f"SELECT * FROM albums;").fetchall():
                                                 if item[1] == name:
                                                         connection.execute(f"INSERT INTO albums_lists(albums_id,artist_id)Values('{item[0]}','{artist_id}';")
                                 except:
                                         print(f'отношение альбом{item[0]}-артист{artist_id} уже существует')
                        tracks_add(item[0],album[name])


def tracks_add(album_id,track):
        for track_name in track[1:]:
                connection.execute(f"INSERT INTO tracks(timing,albums_id,track_name)Values({track_name[1]},'{album_id}','{track_name[0]}');")

def add_collection_list(coll):
        for item in coll:
                for name in item:
                        collect = add_collection([name,item[name][0]])
                        for track in item[name][1]:
                                track_id=find_track_id(track)
                                if track_id != None:
                                        try:
                                                connection.execute(f"INSERT INTO coll_list(coll_id,track_id)Values('{collect}','{track_id}');")
                                        except:
                                                print('keys value already exists', collect,' and ',track_id)
                                else:
                                        print(track,' not find')

def find_track_id(name):
        for item in connection.execute(f"SELECT * FROM tracks;").fetchall():
                if item[3] == name:
                        return item[0]

def add_collection(coll):
        try:
                connection.execute(f"INSERT INTO tracks_coll(collection_name, coll_year)Values('{coll[0]}','{coll[1]}');")
                for item in connection.execute(f"SELECT all from tracks_coll;").fetchall():
                        if item[1] == coll[0]:
                                return item[0]
        except:
                for item in connection.execute(f"SELECT * FROM tracks_coll").fetchall():
                        if item[1] == coll[0]:
                                return item[0]





database = 'postgresql://musus:12345@localhost:5432/music'
engine = sqlalchemy.create_engine(database)
connection = engine.connect()
with open('artists.json') as f:
    artists_list = json.load(f)
with open('collection.json') as file:
    coll = json.load(file)

for first_slice in artists_list:
        for second_slice in first_slice:
                artist_id = uniq_artist(second_slice)
                unick_genre(first_slice[second_slice][0]['Genre'],artist_id)
                albums_add(first_slice[second_slice][1]['Albums'],artist_id)
time.sleep(1)
add_collection_list(coll)
time.sleep(3)
pprint(sampling.show_me(database))