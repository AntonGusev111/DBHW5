import sqlalchemy
from pprint import pprint

def show_me(database):
    engine = sqlalchemy.create_engine(database)
    connection = engine.connect()

    artist_to_genre = 'Количество исполнителей в каждом жанре: ' + str(connection.execute("""select genre.genre_name, count(genre_lists.artist_id) from genre_lists
                                             join genre on genre.id = genre_lists.genre_id 
                                             group by genre.genre_name;""").fetchall())

    tracks_in_19_20 = 'Количество треков, вошедших в альбомы 2019-2020 годов: ' + str(connection.execute("""select albums.album_name, count(tracks.id) from tracks
                                            join albums on albums.id = tracks.albums_id
                                            where album_year between 2019 and 2020 
                                            group by albums.album_name;""").fetchall())

    average_duration_by_album = 'Средняя продолжительность треков по каждому альбому: ' + str(connection.execute("""select albums.album_name , AVG(tracks.timing) from tracks
                                                      left join albums on albums.id = tracks.albums_id 
                                                      group by albums.album_name; """).fetchall())

    artists_who_not_albums_in_20 = 'Все исполнители, которые не выпустили альбомы в 2020 году' + str(connection.execute("""select artists.artist_name from artists
                                                        join albums_lists on artists.id = albums_lists.artist_id 
                                                        join albums on albums_lists.albums_id = albums.id
                                                        where albums.album_year not in ('2020')
                                                        group by artists.artist_name;""").fetchall())

    collection_where_there_is_artist = 'Названия сборников, в которых присутствует Metalica: ' + str(connection.execute("""select tracks_coll.collection_name from tracks_coll
                                                             join coll_list on tracks_coll.id = coll_list.coll_id 
                                                             join tracks on coll_list.track_id = tracks.id 
                                                             join albums on tracks.albums_id = albums.id 
                                                             join albums_lists on albums.id = albums_lists.albums_id 
                                                             join artists on albums_lists.artist_id = artists.id 
                                                             where artists.artist_name in ('Metalica');""").fetchall())

    albums_where_more_1_genre_artist = 'Название альбомов, в которых присутствуют исполнители более 1 жанра:' + str(connection.execute("""select distinct albums.album_name from albums 
                                                             join albums_lists on albums.id = albums_lists.albums_id
                                                             join artists on albums_lists.artist_id = artists.id
                                                             join genre_lists on artists.id = genre_lists.artist_id
                                                             where genre_lists.genre_id >=(select count(genre_lists.genre_id) from genre_lists);""").fetchall())


    tracks_that_are_not_in_coll = 'Наименование треков, которые не входят в сборники:' +  str(connection.execute("""select tracks.track_name from tracks
                                                        left join coll_list on tracks.id = coll_list.track_id 
                                                        left join tracks_coll on coll_list.coll_id = tracks_coll.id
                                                        where tracks_coll.collection_name is null;""").fetchall())

    shortest_track_artist = 'Исполнители, написавшие самый короткий по продолжительности трек' + str(connection.execute("""select artists.artist_name from artists 
                                                join albums_lists on artists.id = albums_lists.artist_id
                                                join albums on albums_lists.albums_id = albums.id
                                                join tracks on albums.id = tracks.albums_id
                                                where tracks.timing = (select min(tracks.timing) from tracks);""").fetchall())

    smollest_album ='Название альбомов, содержащих наименьшее количество треков' + str(connection.execute("""select  albums.album_name, count(tracks.id) from albums
                                           join tracks on albums.id = tracks.albums_id
                                           group by albums.album_name
                                           having count(tracks.id) <= (select  
                                           count(tracks.id)  from albums 
                                           join tracks on albums.id = tracks.albums_id
                                           group by albums.album_name
                                           order by count(tracks.id) ASC
                                           LIMIT 1)
                                           ;""").fetchall())


    return artist_to_genre, tracks_in_19_20, average_duration_by_album, artists_who_not_albums_in_20, \
           collection_where_there_is_artist, albums_where_more_1_genre_artist, tracks_that_are_not_in_coll, \
           tracks_that_are_not_in_coll, shortest_track_artist, smollest_album


