from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from console import print_movie_dict

engine = None


def init_engine(debug=True, dbfile="data/movies.db"):
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
                title TEXT UNIQUE NOT NULL,
                year INTEGER NOT NULL,
                rating REAL NOT NULL,
                poster_url,
                user_id INTEGER,
                FOREIGN KEY(user_id) REFERENCES user(id) ON DELETE CASCADE
            )
        
        """))

        connection.commit()


def list_movies():
    """ Retrieve all movies from the database. """
    with engine.connect() as connection:
        result = connection.execute(text("""
        
            SELECT title, year, rating, poster_url FROM movies
        
        """))
        movies = result.fetchall()

    return {row[0]: {
        "year": row[1],
        "rating": row[2],
        "poster_url": row[3]
        } for row in movies
    }


def add_movie(title, year, rating, poster_url):
    """ Add a new movie to the database. """
    with engine.connect() as connection:
        try:
            connection.execute(text("""
            
                INSERT INTO movies (title, year, rating, poster_url)
                VALUES (:title, :year, :rating, :poster_url)
            
            """), {
                    "title": title,
                    "year": year,
                    "rating": rating,
                    "poster_url": poster_url
                }
            )
            connection.commit()
        except Exception as e:
            print(f"Error: {e}")


def delete_movie(title):
    """ Delete a movie from the database. """
    with engine.connect() as connection:
        try:
            connection.execute(text("""
            
                DELETE FROM movies
                WHERE title = :title
            
            """), {"title": title})
            connection.commit()
        except Exception as e:
            print(f"Error: {e}")


def update_movie(title, rating):
    """ Update the rating of a movie in the database. """
    with engine.connect() as connection:
        try:
            connection.execute(text("""
            
                UPDATE movies SET rating = :rating
                WHERE title = :title
            
            """), {"title": title, "rating": rating})
            connection.commit()
        except Exception as e:
            print(f"Error: {e}")


# Tests
if __name__ == "__main__":
    init_engine(dbfile="test.db", debug=False)
    print("sql engine initialized as", engine)

    add_movie("Example Movie", 2000, 5.0, "https://www.youtube.com/watch?v=5SZYz7lZRRI")
    add_movie("Other Movie", 2020, 6.0, "https://www.youtube.com/watch?v=5SZYz7lZRRI")

    print("Added 2 movies to the database.")

    for title, details in list_movies().items():
        print("    ", end="")
        print_movie_dict(title, details)

    update_movie("Example Movie", 10.0)
    update_movie("Other Movie", 1.0)

    print("Updated movies.")

    for title, details in list_movies().items():
        print("    ", end="")
        print_movie_dict(title, details)

    delete_movie("Example Movie")
    delete_movie("Other Movie")

    print("Cleaned up movies.")

    movies = list_movies()

    print("Movies in database:", len(movies))