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
from console import (
    space,
    print_header,
    print_rainbow,
    show_menu_choices,
    execute_user_choice,
)
from inputs import get_user_input


def exit_app():
    """ Exits the application. """
    print("Bye!")
    sys.exit()


PROGRAM_TITLE = "My Movies Database"

menu_choices = [
    ("Exit", exit_app),
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
]
NUM_CHOICES = len(menu_choices)

quit_commands = ["quit", "leave", "goodbye", "exit", "stop"]


def show_menu():
    """ Prints the main menu. """
    print_rainbow("Menu:")
    show_menu_choices(menu_choices)
    space()

def show_program_title():
    """ Prints the title of the program. """
    print_header(PROGRAM_TITLE, width=40)
    space()


def main():
    """ Runs a loop to fetch and execute user commands from a menu
        until `0` or a quit signal is entered.
    """
    if len(menu_choices) == 0:
        print("Error, no menu choices.")
        return

    show_program_title()
    show_menu()

    # Program Main Loop
    while True:
        user_input = get_user_input(f"Enter choice: (0 - {NUM_CHOICES - 1}): ")

        if user_input.lower() in quit_commands:
            print("Goodbye!")
            break

        try:
            user_choice = int(user_input)
            executed_successfully = execute_user_choice(menu_choices, user_choice)

            if executed_successfully:
                space()
                get_user_input("Press enter to continue")
                space()
                show_menu()

        except ValueError:
            pass


if __name__ == "__main__":
    main()
