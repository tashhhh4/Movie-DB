import os
import requests


COUNTRIES_API = "https://restcountries.com/v3.1"


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


def get_country_flag(country_name):
    """ Returns a url to a flag icon,
        or None if `country_name` is not found.
    """
    url = COUNTRIES_API + "/name/" + country_name
    response = requests.get(url)
    data = response.json()

    if not data:
        return None

    if "status" in data and data["status"] == 404:
        return None
    
    country = data[0]

    if "flags" not in country:
        return None

    if "svg" in country["flags"]:
        return country["flags"]["svg"]

    if "png" in country["flags"]:
        return country["flags"]["png"]

    return None