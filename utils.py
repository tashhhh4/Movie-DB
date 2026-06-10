import os

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


def ensure_dir(dirname):
    """ Makes sure that a filesystem directory exists and creates it if it doesn't.
        Returns the directory name.
    """
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    return dirname
