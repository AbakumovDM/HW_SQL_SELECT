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
