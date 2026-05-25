# Runs and tests sql queries

from movie_storage_sql import ensure_schema, add_movie, list_movies

ensure_schema()

add_movie("The Devil Wears Prada", 2006, 6.5)
add_movie("The Butterfly Effect", 2004, 8.4)

movies = list_movies()
for movie in movies:
    print(movie)