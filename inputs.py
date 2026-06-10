import style
from movie_storage.movie_storage_sql import list_movies as get_movies
from users.manager import UserManager
from console import err


# General input wrapper function

def get_user_input(prompt):
    """ Gets user input and differentiates user's input with a cyan style. """
    user_input = input(prompt + style.CYAN).strip()
    print(style.ENDC, end="")
    return user_input


# Functions which repeat until valid input is entered

def get_movie_title(prompt):
    """ Gets a movie title.
        - Can't be empty
    """
    user = UserManager.get_current_user()
    movies = get_movies(user["id"])
    while True:
        title = get_user_input(prompt)
        if title == "":
            err("Movie title is required.")
            continue

        if title in movies:
            err(f"Movie {title} already exists!")
            continue

        return title


def get_movie_rating(prompt, optional=False):
    """ Gets a movie rating.
        - Must convert to float without errors.
        - Must be between 0 and 10
        - Can return None if `optional` is set to `True`.
    """
    while True:
        rating = get_user_input(prompt)

        if rating == "":
            if not optional:
                err("Rating is required.")
                continue

            return None

        try:
            rating = float(rating)
            if not 0.0 <= rating <= 10.0:
                err("Invalid rating.")
                continue

            return rating

        except ValueError:
            err("Invalid rating.")


def get_movie_year(prompt, optional=False):
    """ Gets a movie year.
        - Must successfully convert to an int.
        - Can return None if `optional` is set to `True`.
    """
    while True:
        year = get_user_input(prompt)

        if year == "":
            if not optional:
                err("Year is required.")
                continue

            return None

        try:
            year = int(year)
            return year

        except ValueError:
            err("Year invalid.")


def get_y_n(prompt):
    """ Gets a yes or no choice from the user, returned as a
        True or False value.
        Implicit not allowed.

        Returns:
            user_choice: boolean
    """
    while True:
        choice = get_user_input(prompt).upper()
        if choice == 'Y':
            return True
        if choice == 'N':
            return False

        err("Please enter \"Y\" or \"N\".")
