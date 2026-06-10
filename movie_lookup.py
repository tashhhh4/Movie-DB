import requests
import secrets

API_URL = "http://www.omdbapi.com/"


def get_movie_link(imdb_id):
    return f"https://www.imdb.com/title/{imdb_id}/"


def get_movie_details(title_search):
    """ Searches OMDB API for the movie most relevant to the `title`.
    Provides the full title and year of the top match.
    Can also return None if no match is found.
    """
    try:
        response = requests.get(f"{API_URL}?apikey={secrets.API_KEY}&t={title_search}")
        data = response.json()

        if "Error" in data:
            if data["Error"] == "Invalid API key!":
                print("Movie lookup error: Invalid API key!")
                return

            if data["Error"] == "Movie not found!":
                print("Movie lookup error: Movie not found!")
                return

        return {
            "title": data["Title"],
            "year": data["Year"],
            "rating": data["imdbRating"],
            "poster_url": data["Poster"],
            "imdb_id": data["imdbID"],
        }
    
    except AttributeError:
        print("Movie lookup error: API Key is missing! "
              "Please create the value `API_KEY = \"<your_api_key_here>\"` in `secrets.py`. "
              "See the README file for further details.")
        return

# Tests
if __name__ == "__main__":
    details = get_movie_details("titanic")
    title, year, rating, poster_url = details
    print(f"{title}: {year} ({rating})")
    print(f"Poster: {poster_url}")

    details = get_movie_details("fake movie that doesn't exist`")
    print(details)
    