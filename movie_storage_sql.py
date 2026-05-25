from sqlalchemy import create_engine, text

DB_URL = "sqlite:///movies.db"

engine = create_engine(DB_URL, echo=True)

def ensure_schema():
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