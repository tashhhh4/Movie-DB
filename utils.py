def is_int(value):
    """ Checks if a value will successfully convert to an int. """
    try:
        int(value)
        return True
    except ValueError:
        return False


def is_float(value):
    """ Checks if a value will successfully convert to a float. """
    try:
        float(value)
        return True
    except ValueError:
        return False
        