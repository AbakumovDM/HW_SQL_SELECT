import sqlalchemy
import psycopg2
from pprint import pprint

engine = sqlalchemy.create_engine('postgresql://nameuser:namepassword@localhost:5432/basename')

connection = engine.connect()

connection.execute('''SELECT album_name, album_release_year FROM albums WHERE album_release_year = '2018';''').fetchall()

connection.execute('''SELECT track_name, track_duration FROM tracks WHERE track_duration = (SELECT max(track_duration) FROM tracks);''').fetchall()

connection.execute('''SELECT track_name, track_duration FROM tracks WHERE track_duration >= '3.50';''').fetchall()

connection.execute('''SELECT collection_name FROM collection WHERE collection_release_year >= '2018' AND collection_release_year <= '2020';''').fetchall()

connection.execute('''SELECT artist_name FROM artist WHERE artist_name NOT LIKE '%% %%';''').fetchall()

connection.execute('''SELECT track_name FROM tracks WHERE track_name LIKE '%%my%%';''').fetchall()

с = connection.execute('''SELECT name_of_the_genre, COUNT(perform_id) FROM artist_genre a 
                        LEFT JOIN genre g ON a.genre_id = g.id 
                        GROUP BY name_of_the_genre;''').fetchall()
pprint(с)
pprint('_______________')
с = connection.execute('''SELECT COUNT(track_name) FROM tracks AS t 
                        JOIN albums AS a ON t.album_id = a.id 
                        WHERE album_release_year IN ('2019', '2020');''').fetchall()
pprint(с)
pprint('________________')
с = connection.execute('''SELECT COUNT(track_name) FROM tracks AS t 
                        JOIN albums AS a ON t.album_id = a.id 
                        WHERE album_release_year >='2018';''').fetchall()
pprint(с)
pprint('________________')
с = connection.execute('''SELECT AVG(track_duration), album_name FROM tracks AS t 
                        JOIN albums AS a ON t.album_id = a.id 
                        GROUP BY album_name;''').fetchall()
pprint(с)
pprint('________________')
с = connection.execute('''SELECT artist_name FROM artist AS ar
                        fUll OUTER JOIN artist_albums AS aa ON ar.id = aa.perform_id
                        fUll OUTER JOIN albums AS al ON aa.album_id = al.id
                        WHERE album_release_year != '2020';''').fetchall()
pprint(с)
pprint('________________')
с = connection.execute('''SELECT DISTINCT collection_name, artist_name FROM collection AS c
                        JOIN collection_of_tracks AS ct ON c.id = ct.collection_id
                        JOIN tracks AS tr ON ct.track_id = tr.id
                        JOIN albums AS al ON tr.album_id = al.id
                        JOIN artist_albums AS aa ON al.id = aa.album_id
                        JOIN artist AS ar ON aa.perform_id = ar.id
                        WHERE artist_name = 'queen';''').fetchall()
pprint(с)
pprint('________________')
с = connection.execute('''SELECT DISTINCT album_name, COUNT(genre_id) FROM albums AS al
                        JOIN artist_albums AS aa ON al.id = aa.album_id
                        JOIN artist AS ar ON aa.perform_id = ar.id
                        JOIN artist_genre AS ag ON ar.id = ag.perform_id
                        GROUP BY album_name
                        HAVING COUNT(genre_id) > 1 ;''').fetchall()
pprint(с)
pprint('________________')
с = connection.execute('''SELECT track_name FROM tracks AS tr
                        LEFT JOIN collection_of_tracks AS ct ON tr.id = ct.track_id
                        WHERE ct.track_id IS NULL;''').fetchall()
pprint(с)
pprint('________________')
с = connection.execute('''SELECT artist_name, track_duration FROM artist AS ar
                            JOIN artist_albums AS aa ON ar.id = aa.perform_id
                            JOIN albums AS al ON aa.album_id = al.id
                            JOIN tracks AS tr ON al.id = tr.album_id
                            WHERE track_duration = (
                                SELECT MIN(track_duration) FROM tracks);''').fetchall()
pprint(с)
pprint('________________')
c = connection.execute('''SELECT DISTINCT album_name FROM albums AS al
                             JOIN tracks AS tr ON al.id = tr.album_id
                             WHERE al.id IN (
                                 SELECT album_id FROM tracks
                                 GROUP BY album_id
                                 HAVING COUNT(id) = (
                                     SELECT COUNT(id) FROM tracks
                                     GROUP BY album_id
                                     ORDER BY COUNT limit 1))
                             ORDER BY album_name;''').fetchall()
pprint(c)


