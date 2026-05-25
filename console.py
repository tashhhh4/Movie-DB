import random
import style


def space():
    """ Adds a blank line. """
    print()

def err(message):
    """ Prints in red. """
    print(style.RED + message + style.ENDC)


def print_rainbow(message, end="\n"):
    """ Prints in a crazy rainbow style! """
    colors = [
        style.RED,
        style.YELLOW,
        style.GREEN,
        style.CYAN,
        style.SBLUE,
        style.LPURP,
    ]
    i = random.randrange(0, len(colors))
    for c in message:
        print(colors[i] + c + style.ENDC, end="")
        i += 1
        if i == len(colors):
            i = 0
    print("", end=end)


def print_header(text, width):
    """ Prints a formatted primary header. """
    num_stars_left = width - len(text) - 2
    num_stars_right = width - len(text) - 2
    if len(text) % 2 != 0:
        num_stars_right -= 1

    print(style.LPURP + '*' * num_stars_left + style.ENDC, end="")
    print(f" {text} ", end="")
    print(style.LPURP + '*' * num_stars_right + style.ENDC)


def print_movie_dict(title, details):
    """ Prints one movie along with its year and rating. """
    year = f" ({details['year']})" if details["year"] else ""
    print(f"{title}{year}: {details['rating']:.1f}")


def show_menu_choices(choice_list):
    """
        Args:
            choice_list: [("Description", callable)]
    """
    for i, choice in enumerate(choice_list):
        print(style.CYAN + f"{i}" + style.ENDC + style.LPURP +
        f": {choice[0]}" + style.ENDC)


def execute_user_choice(choice_list, choice):
    """
        Calls the function from the choice list.
        Args:
            choice_list: [("Description", callable)]
            choice: int
        Returns:
            executed_successfully: boolean
    """
    index = choice
    if not 0 <= index <= len(choice_list) - 1:  # catch wrong indices
        return False

    space()

    _, function = choice_list[index]
    if not function:
        print("That function is not yet implemented!")
    else:
        function()
    return True
