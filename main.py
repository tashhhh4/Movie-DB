import sys
import movies.manager as MovieManager
from users.manager import UserManager
from console import (
    space,
    err,
    print_header,
    print_rainbow,
    show_menu_choices,
    execute_user_choice,
)
from inputs import get_user_input
from website import generate as generate_website


# Program settings
PROGRAM_TITLE = "My Movies Database"

QUIT_COMMANDS = ["quit", "leave", "goodbye", "exit", "stop"]


# Extra utils
should_flash_title = True
def set_should_flash_title(should):
    """ Setter method for global signal. """
    global should_flash_title
    should_flash_title = should

def exit_app():
    """ Exits the application. """
    print("Bye!")
    sys.exit()
QUIT_CHOICE = ("(Exit)", exit_app)


# Login Menu
LOGIN_MENU_HEADING = "Welcome to the Movie App! 🎬"
def make_login_function(user):
    def login():
        UserManager.login(user["id"])
        print(f"Logged in as {user["name"]}.")
        set_should_flash_title(True)
    return login

def create_user() :
    """ Adds a new user. """
    name = get_user_input("Enter new user name: ")
    UserManager.create_user(name)

def show_login_menu():
    """ Prints the login (users) menu. """
    print_rainbow("Welcome to the Movie App! 🎬")
    space()
    print("Select a user:")

    users = UserManager.get_all_users()
    choices = [QUIT_CHOICE]
    for user in users:
        choices.append((user["name"], make_login_function(user)))
    choices.append(("Create new user", create_user))

    show_menu_choices(choices)
    space()
    return choices


# Commands Menu
def logout():
    user = UserManager.get_current_user()
    UserManager.logout()
    print(f"Logged out {user["name"]}.")
    set_should_flash_title(True)

command_choices = [
    (QUIT_CHOICE[0],            QUIT_CHOICE[1]),
    ("List movies",             MovieManager.list_all_movies),
    ("Add movie",               MovieManager.add_movie),
    ("Delete movie",            MovieManager.delete_movie),
    ("Update movie",            MovieManager.update_movie),
    ("Stats",                   MovieManager.stats),
    ("Create rating histogram", MovieManager.export_histogram),
    ("Random movie",            MovieManager.random_movie),
    ("Search movie",            MovieManager.search_movie),
    ("Movies sorted by rating", MovieManager.list_by_rating),
    ("Movies sorted by year",   MovieManager.list_by_year),
    ("Filter movies",           MovieManager.filter_movies),
    ("Generate website",        generate_website),
    ("Switch user",             logout),
]

def show_commands_menu():
    """ Prints the main menu. """
    user = UserManager.get_current_user()
    print_rainbow(f"Welcome back, {user["name"]}!")
    user_movies = MovieManager.get_all_movies()
    if not user_movies:
        err(f"{user["name"]}, your movie collection is empty. Add some movies!")
    space()
    print("Menu:")
    show_menu_choices(command_choices)
    space()
    return command_choices


def show_menu():
    """ Prints either the login menu or the commands menu.
        Returns the list of choices and number of available choices.
    """
    current_user = UserManager.get_current_user()

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
