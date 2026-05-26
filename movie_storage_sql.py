from sqlalchemy import create_engine, text

DB_URL = "sqlite:///movies.db"

engine = None


def init_engine(debug=True):
    """ Initialize the sql engine with an optional debug mode.
    """
    global engine
    engine = create_engine(DB_URL, echo=(debug == True))


def create_schema():
    """ Creates the movies table if it doesn't already exist. """
    with engine.connect() as connection:
        connection.execute(text("""

            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT UNIQUE NOT NULL,
                year INTEGER NOT NULL,
                rating REAL NOT NULL
            )
        
        """))
        connection.commit()


def list_movies():
    """ Retrieve all movies from the database. """
    with engine.connect() as connection:
        result = connection.execute(text("""
        
            SELECT title, year, rating FROM movies
        
        """))
        movies = result.fetchall()

    return {row[0]: {"year": row[1], "rating": row[2]} for row in movies}


def add_movie(title, year, rating):
    """ Add a new movie to the database. """
    with engine.connect() as connection:
        try:
            connection.execute(text("""
            
                INSERT INTO movies (title, year, rating)
                VALUES (:title, :year, :rating)
            
            """),
            {"title": title, "year": year, "rating": rating})
            connection.commit()
            print(f"Movie '{title}' added successfully.")
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
            print(f"Movie '{title}' was deleted.")
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
            print(f"Movie '{title}' updated.")
        except Exception as e:
            print(f"Error: {e}")


# Tests
if __name__ == "__main__":
    print("engine is", engine)
    init_engine()
    print("after running init. engine is", engine)

    create_schema()

    add_movie("The Devil Wears Prada", 2006, 6.5)
    add_movie("The Butterfly Effect", 2004, 8.4)

    movies = list_movies()
    for movie in movies:
        print(movie)

    update_movie("The Butterfly Effect", 7.0)
    delete_movie("The Devil Wears Prada")

    print("After modifying data:")
    print(list_movies())