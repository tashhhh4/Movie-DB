### Destroys all existing data and recreates the movies table ###

from movie_storage_sql import init_engine, reset_schema

init_engine(dbfile="movies.db", debug=True)

reset_schema()