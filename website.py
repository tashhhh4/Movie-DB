import os
from db import get_all_movies


OUTPUT_DIR = "output"
STATIC_DIR = "static"
TEMPLATE_FILE = os.path.join(STATIC_DIR, "index_template.html")
STYLE_FILE = os.path.join(STATIC_DIR, "style.css")
APP_TITLE = "My Movie App"


# IO Utils
def save_webpage(filename, html):
    if filename == TEMPLATE_FILE:
        print("Error: Tried to overwrite template file! Please choose a different filename.")
        return

    with open(filename, "w", encoding="utf-8") as file:
        file.write(html)

def load_text(filename):
    with open(filename, "r", encoding="utf-8") as file:
        data = file.read()
        return data


# Movie List Helper
def get_movies():
    movie_list = []
    movie_dict = get_all_movies()
    for key, item in movie_dict.items():
        movie_list.append({
            "title": key,
            "poster_url": item["poster_url"],
            "rating": item["rating"],
            "year": item["year"],
        })
    return movie_list


# Website Generator
def generate():
    movies = get_movies()

    username = "Tasha"
    # username = None

    if username:
        user_heading = f'{username}\'s Favorites'
        filename = f"movies_{username}.html"
    else:
        user_heading = ''
        filename = "movies.html"
    
    list_items = ''
    for movie in movies:
        list_items += f'<li><div class="movie"><img class="movie-poster" src="{movie["poster_url"]}" title><div class="movie-title">{movie["title"]}</div><div class="movie-year">{movie["year"]}</div>'

    html = load_text(TEMPLATE_FILE)
    css = load_text(STYLE_FILE)
    html = html.replace("__TEMPLATE_TITLE__", APP_TITLE)
    html = html.replace("__CSS_STYLE__", css)
    html = html.replace("__USER_HEADING__", user_heading)
    html = html.replace("__TEMPLATE_MOVIE_GRID__", list_items)

    output_file = os.path.join(OUTPUT_DIR, filename) 
    save_webpage(output_file, html)    

    print("Website was generated successfully.")