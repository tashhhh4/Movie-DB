import statistics
import random
from matplotlib import pyplot
from console import err, space, print_rainbow, print_movie_dict
from inputs import (
    get_user_input,
    get_movie_title,
    get_movie_rating,
    get_movie_year,
    get_y_n,
)
import movie_storage.movie_storage_sql as db
from movie_lookup import get_movie_details
from users import UserManager


def get_all_movies():
    """ Returns all of a user's movies as a list. """
    user = UserManager.get_current_user()
    return db.list_movies(user["id"])


def list_all_movies():
    """ Prints all the movies in a vertical list. """
    user = UserManager.get_current_user()

    movies = db.list_movies(user["id"])
    num_movies = len(movies)
    s = "" if num_movies == 1 else "s"

    print(f"{num_movies} movie{s} in total")
    for title, details in movies.items():
        print_movie_dict(title, details)


def add_movie():
    """ Adds a movie to the database by title.
    Automatically fills in title with corrected spelling, year, and IMDB rating.
    Prompts user if automatic lookup fails to find a rating.
    """
    user = UserManager.get_current_user()

    title = get_movie_title("Enter movie name: ")

    try:
        details = get_movie_details(title)
    except AttributeError:
        print("Unable to fetch movie details because API Key is missing! "
              "Please create the value `API_KEY = \"<your_api_key_here>\"` in `secrets.py`. "
              "See the README file for further details.\n\n(Movie was not added.)")
        return

    if not details:
        print(f"Movie {title} was not found.")
        return

    title, year, rating, poster_url = details

    try:
        rating = float(rating)
    except ValueError:
        rating = get_movie_rating(f"Enter missing rating for {title}: ")

    db.add_movie(title, year, rating, poster_url, user["id"])
    print(f"Movie {title} successfully added.")
    print(f"Year: {year}")
    print(f"Rating (IMDB): {rating}")
    print(f"Poster: {poster_url}")


def delete_movie():
    """ Removes the movie with the matching title from the database.
        Prints an error if the movie doesn't exist.
    """
    user = UserManager.get_current_user()

    movies = db.list_movies(user["id"])

    title = get_user_input("Enter movie name to delete: ")

    try:
        movie_id = movies[title]["id"]
    except KeyError:
        err(f"Movie {title} doesn't exist!")
        return
    
    db.delete_movie(movie_id)

    print(f"Movie {title} successfully deleted.")


def update_movie():
    """ Update the rating of an existing movie.
        Prints an error if the movie doesn't exist.
    """
    user = UserManager.get_current_user()

    movies = db.list_movies(user["id"])

    title = get_user_input("Enter movie name: ")

    try:
        movie_id = movies[title]["id"]
    except KeyError:
        err(f"Movie {title} doesn't exist!")
        return

    rating = get_movie_rating("Enter new rating: ")

    db.update_movie(movie_id, rating)
    print(f"Movie {title} successfully updated.")


def stats():
    """ Prints statistics about your entire dataset.
        - Average rating
        - Median rating
        - Best rated movie(s)
        - Worst rated movie(s)
    """
    user = UserManager.get_current_user()

    movies = db.list_movies(user["id"])

    details = movies.values()
    ratings = [item["rating"] for item in details]
    average_rating = statistics.mean(ratings)
    median_rating = statistics.median(ratings)
    best_movie_title = max(movies, key=lambda k: movies[k]["rating"])
    best_movie_rating = movies[best_movie_title]["rating"]
    worst_movie_title = min(movies, key=lambda k: movies[k]["rating"])
    worst_movie_rating = movies[worst_movie_title]["rating"]

    print(f"Average rating: {average_rating:.1f}")
    print(f"Median rating: {median_rating:.1f}")
    print(f"Best movie: {best_movie_title}, {best_movie_rating}")
    print(f"Worst movie: {worst_movie_title}, {worst_movie_rating}")


def random_movie():
    """ Print a random movie with its rating. """
    user = UserManager.get_current_user()

    movies = db.list_movies(user["id"])

    titles_list = list(movies.keys())
    index = random.randrange(0, len(titles_list))
    title = titles_list[index]
    rating = movies[title]["rating"]

    print("Your movie for tonight: ", end="")
    print_rainbow(title, end="")
    print(f", it's rated {rating:.1f}!")


def search_movie():
    """ All movies that match the query are printed, with their ratings. """
    user = UserManager.get_current_user()

    movies = db.list_movies(user["id"])

    query = get_user_input("Enter part of movie name: ")

    hits = {}
    for title in movies.keys():
        if query.lower() in title.lower():
            hits[title] = movies[title]
    for title, details in hits.items():
        print_movie_dict(title, details)


def list_by_rating():
    """ Prints all the movies, sorted by rating from highest to lowest. """
    user = UserManager.get_current_user()
    movies = db.list_movies(user["id"])
    while len(movies) > 0:
        highest_rated = max(movies, key=lambda k: movies[k]["rating"])
        print_movie_dict(highest_rated, movies[highest_rated])
        del movies[highest_rated]


def list_by_year():
    """ Prints all the movies, sorted by year in either
        descending or ascending order.
    """
    order_by_newest = get_y_n("Do you want the latest movies first? (Y/N) ")

    user = UserManager.get_current_user()
    movies = db.list_movies(user["id"])
    while len(movies) > 0:
        sort_func = max if order_by_newest else min
        next_movie = sort_func(movies, key=lambda k: movies[k]["year"])
        print_movie_dict(next_movie, movies[next_movie])
        del movies[next_movie]


def filter_movies():
    """ Prints a subset of the movies depending on user inputs. """
    min_rating = get_movie_rating("Enter minimum rating (leave blank for no minimum rating): ",
                                optional=True)
    start_year = get_movie_year("Enter start year (leave blank for no start year): ",
                                optional=True)
    end_year = get_movie_year("Enter end year (leave blank for no end year): ",
                            optional=True)
    space()

    user = UserManager.get_current_user()
    movies = db.list_movies(user["id"])
    filtered_movies = {}
    for title, details in movies.items():
        valid = True
        if min_rating is not None and details["rating"] < min_rating:
            valid = False
        if start_year is not None and details["year"] < start_year:
            valid = False
        if end_year is not None and details["year"] > end_year:
            valid = False

        if valid:
            filtered_movies[title] = details

    print("Filtered movies:")
    for title, details in filtered_movies.items():
        print_movie_dict(title, details)


def export_histogram():
    """ Saves a histogram as a .png in the local file storage. """
    user = UserManager.get_current_user()

    movies = db.list_movies(user["id"])

    ratings = [item["rating"] for key, item in movies.items()]

    pyplot.hist(ratings, bins=20, color="skyblue", edgecolor="black")
    pyplot.xlabel("Ratings")
    pyplot.ylabel("Frequency")
    pyplot.title("Distribution of Movie Ratings")

    filename = get_user_input("Name the file (without extension) to save: ")
    filename += ".png"

    pyplot.savefig(filename)
