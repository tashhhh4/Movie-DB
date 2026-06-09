import sys

from db import (
    list_all_movies,
    add_movie,
    delete_movie,
    update_movie,
    stats,
    random_movie,
    search_movie,
    list_by_rating,
    export_histogram,
    list_by_year,
    filter_movies,
)
from website import generate as generate_website
from console import (
    space,
    print_header,
    print_rainbow,
    show_menu_choices,
    execute_user_choice,
)
from inputs import get_user_input
from users import UserManager


def exit_app():
    """ Exits the application. """
    print("Bye!")
    sys.exit()

PROGRAM_TITLE = "My Movies Database"

should_flash_title = True
def set_should_flash_title(should):
    """ Setter method for global signal. """
    global should_flash_title
    should_flash_title = should

QUIT_COMMANDS = ["quit", "leave", "goodbye", "exit", "stop"]

QUIT_CHOICE = ("(Exit)", exit_app)

# Login Menu
LOGIN_MENU_HEADING = "Welcome to the Movie App! 🎬"
def make_login_function(user_name):
    def login():
        UserManager.login(user_name)
        print(f"Logged in as {user_name}.")
        set_should_flash_title(True)
    return login

def create_user() :
    name = get_user_input("Enter new user name: ")
    UserManager.create_user(name)

def show_login_menu():
    """ Prints the login (users) menu. """
    print_rainbow("Welcome to the Movie App! 🎬")
    space()
    print("Select a user:")

    users = UserManager.get_all_users()
    choices = [QUIT_CHOICE]
    for user_name in users:
        choices.append((user_name, make_login_function(user_name)))
    choices.append(("Create new user", create_user))

    show_menu_choices(choices)
    space()
    return choices

# Commands Menu
def logout():
    user = UserManager.get_user()
    UserManager.logout()
    print("Logged out {user}.")
    set_should_flash_title(True)

command_choices = [
    QUIT_CHOICE,
    ("List movies", list_all_movies),
    ("Add movie", add_movie),
    ("Delete movie", delete_movie),
    ("Update movie", update_movie),
    ("Stats", stats),
    ("Create rating histogram", export_histogram),
    ("Random movie", random_movie),
    ("Search movie", search_movie),
    ("Movies sorted by rating", list_by_rating),
    ("Movies sorted by year", list_by_year),
    ("Filter movies", filter_movies),
    ("Generate website", generate_website),
    ("Switch user", logout),
]

def show_commands_menu():
    """ Prints the main menu. """
    user = UserManager.get_user()
    print_rainbow(f"Welcome back, {user}!")
    user_movies = []
    if not user_movies:
        print(f"{user}, your movie collection is empty. Add some movies!")
    space()
    print("Menu:")
    show_menu_choices(command_choices)
    space()
    return command_choices


def show_menu():
    """ Prints either the login menu or the commands menu.
        Returns the list of choices used,
        and the number of choices available,
    """
    users = UserManager.get_all_users()
    current_user = UserManager.get_user()

    if current_user is None:
        show = show_login_menu
    else:
        show = show_commands_menu
    
    choices = show()
    num_choices = len(choices)
    if num_choices == 0:
        print("Error, no menu choices.")
        return

    return choices, num_choices


def show_program_title():
    """ Prints the title of the program. """
    print_header(PROGRAM_TITLE, width=40)
    space()


def main():
    """ Runs a loop to fetch and execute user commands from a menu
        until `0` or a quit signal is entered.

        If the no user is logged in, shows the login/users menu.
        Otherwise, shows the main list of choices.
    """

    # Program Main Loop
    while True:
        if should_flash_title:
            show_program_title()
            set_should_flash_title(False)

        choices, num_choices, = show_menu()

        user_input = get_user_input(f"Enter choice: (0 - {num_choices - 1}): ")

        if user_input.lower() in QUIT_COMMANDS:
            print("Goodbye!")
            break

        try:
            user_choice = int(user_input)
            executed_successfully = execute_user_choice(choices, user_choice)

            if executed_successfully:
                space()
                get_user_input("Press enter to continue")
                space()

        except ValueError:
            pass


if __name__ == "__main__":
    main()
