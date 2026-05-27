import requests
import secrets

API_URL = "http://www.omdbapi.com/"


def get_movie_details(title_search):
    """ Searches OMDB API for the movie most relevant to the `title`.
    Provides the full title and year of the top match.
    Can also return None if no match is found.
    """
    response = requests.get(f"{API_URL}?apikey={secrets.API_KEY}&t={title_search}")
    data = response.json()

    found_movie = data["Response"] == "True"

    if not found_movie:
        return None

    return data["Title"], data["Year"], data["imdbRating"]


# Tests
if __name__ == "__main__":
    details = get_movie_details("titanic")
    title, year, rating = details
    print(f"{title}: {year} ({rating})")

    details = get_movie_details("fake movie that doesn't exist`")
    print(details)
    