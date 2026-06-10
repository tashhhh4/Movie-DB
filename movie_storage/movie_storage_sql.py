import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from utils import ensure_dir

DEBUG = False
DBDIR = ensure_dir("data")
DBFILE = os.path.join(DBDIR, "movies.db")

engine = None

def init_engine(debug=DEBUG, dbfile=DBFILE):
    """ Initialize the sql engine.
    Optional debug mode, generates verbose logging from SQL.
    Optional db filename parameter, useful for testing without destroying data.
    """
    global engine

    db_url = f"sqlite:///{dbfile}"

    engine = create_engine(db_url, echo=debug)

    # Test querying the users and movies table
    try:
        with engine.connect() as connection:
            result = connection.execute(text("""
            
                SELECT * FROM movies
                JOIN users ON users.id = movies.user_id
            
            """))
    except OperationalError:
        print("No database found. Initializing...")
        reset_schema()
        print("Ready!")


def reset_schema():
    """ Recreates the tables of the database.
    
            #########################
            DESTROYS EXISTING DATA!!!
            #########################
    
    """
    with engine.connect() as connection:
        connection.execute(text("""

            DROP TABLE IF EXISTS movies

        """))
        connection.execute(text("""
        
            DROP TABLE IF EXISTS users
        
        """))
        connection.commit()

    with engine.connect() as connection:
        connection.execute(text("""
        
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
        
        """))
        connection.execute(text("""

            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                year INTEGER NOT NULL,
                rating REAL NOT NULL,
                poster_url,
                user_id INTEGER NOT NULL,
                note TEXT,
                imdb_id TEXT,
                FOREIGN KEY(user_id) REFERENCES user(id) ON DELETE CASCADE
            )
        
        """))

        connection.commit()


def list_movies(user_id):
    """ Retrieve all of a user's movies from the database. """
    with engine.connect() as connection:
        result = connection.execute(text("""
        
            SELECT title, year, rating, poster_url, id, note, imdb_id
            FROM movies
            WHERE user_id = :user_id
        
        """), {"user_id": user_id})
        movies = result.fetchall()

    return {row[0]: {
        "year": row[1],
        "rating": row[2],
        "poster_url": row[3],
        "id": row[4],
        "note": row[5],
        "imdb_id": row[6],
        } for row in movies
    }


def add_movie(title, year, rating, poster_url, user_id, note, imdb_id):
    """ Add a new movie to the database. """
    with engine.connect() as connection:
        try:
            connection.execute(text("""
            
                INSERT INTO movies
                    (title, year, rating, poster_url, user_id, note, imdb_id)
                VALUES
                    (:title, :year, :rating, :poster_url, :user_id, :note, :imdb_id)
            
            """), {
                    "title": title,
                    "year": year,
                    "rating": rating,
                    "poster_url": poster_url,
                    "user_id": user_id,
                    "note": note,
                    "imdb_id": imdb_id,
                }
            )
            connection.commit()
        except Exception as e:
            print(f"Error: {e}")


def delete_movie(movie_id):
    """ Delete a movie from the database. """
    with engine.connect() as connection:
        try:
            connection.execute(text("""
            
                DELETE FROM movies
                WHERE id = :movie_id
            
            """), {"movie_id": movie_id})
            connection.commit()
        except Exception as e:
            print(f"Error: {e}")


def update_movie(movie_id, rating, note):
    """ Update the rating of a movie in the database. """
    with engine.connect() as connection:
        try:
            connection.execute(text("""
            
                UPDATE movies
                SET rating = :rating, note = :note
                WHERE id = :movie_id
            
            """), {"movie_id": movie_id, "rating": rating, "note": note})
            connection.commit()
        except Exception as e:
            print(f"Error: {e}")


# Users
def add_user(name):
    """ Adds a user. """
    with engine.connect() as connection:
        try:
            connection.execute(text("""
            
                INSERT INTO users (name)
                VALUES (:name)
            
            """), {"name": name})
            connection.commit()
        except Exception as e:
            print(f"Error: {e}")


def get_user(user_id):
    """ Retrieves a single user by id. """
    with engine.connect() as connection:
        result = connection.execute(text("""
        
            SELECT id, name
            FROM users
            WHERE id = :user_id
        
        """), {"user_id": user_id})
        users = result.fetchall()
        if not users:
            print("User not found!")
            return
    return {"id": users[0][0], "name": users[0][1]}


def list_users():
    """ Retrieves all users from the database. """
    with engine.connect() as connection:
        result = connection.execute(text("""
        
            SELECT id, name FROM users
        
        """))
        users = result.fetchall()

    return [{"id": u[0], "name": u[1]} for u in users]


# Init
if __name__ != "__main__":
    init_engine()


# Tests
if __name__ == "__main__":
    init_engine(dbfile="data/test.db", debug=False)
    print("sql engine initialized as", engine)

    add_movie("Example Movie", 2000, 5.0, "https://www.youtube.com/watch?v=5SZYz7lZRRI")
    add_movie("Other Movie", 2020, 6.0, "https://www.youtube.com/watch?v=5SZYz7lZRRI")

    print("Added 2 movies to the database.")

    for title, details in list_movies().items():
        print("    ", end="")
        # print_movie_dict(title, details)

    update_movie("Example Movie", 10.0)
    update_movie("Other Movie", 1.0)

    print("Updated movies.")

    for title, details in list_movies().items():
        print("    ", end="")
        # print_movie_dict(title, details)

    delete_movie("Example Movie")
    delete_movie("Other Movie")

    print("Cleaned up movies.")

    movies = list_movies()

    print("Movies in database:", len(movies))