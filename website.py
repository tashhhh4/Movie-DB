import os
import movies.manager as MovieManager
from users import UserManager
from utils import ensure_dir
from movies.lookup import get_movie_link


OUTPUT_DIR = ensure_dir("output")
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
    movie_dict = MovieManager.get_all_movies()
    for key, item in movie_dict.items():
        movie_list.append({
            "title": key,
            "poster_url": item["poster_url"],
            "rating": item["rating"],
            "year": item["year"],
            "note": item["note"],
            "imdb_id": item["imdb_id"],
        })
    return movie_list


# Website Generator
def generate():
    user = UserManager.get_current_user()
    movies = get_movies()

    if user:
        user_heading = f'{user["name"]}\'s Favorites'
        filename = f"movies_{user["name"]}.html"
    else:
        user_heading = ''
        filename = "movies.html"
    
    list_items = ''
    for movie in movies:
        list_items += (
            '<li> '
            '  <div class="movie"> '
           f'    <a href="{get_movie_link(movie["imdb_id"])}"> '
            '      <img class="movie-poster" '
           f'          src="{movie["poster_url"]}" '
           f'          alt="Poster for {movie["title"]}" '
           f'          title="{movie["note"]}" '
            '      > '
            '    </a> '
            '    <div class="movie-info"> '
            '      <div class="movie-info-header"> '
           f'        <span class="movie-title">{movie["title"]}</span> '
           f'        <span class="movie-year">({movie["year"]})</span> '
            '      </div> '
           f'      <span class="movie-rating">Rated {movie["rating"]}</span> '
            '    </div> '
            '  </div> '
            '</li> '
        )

    html = load_text(TEMPLATE_FILE)
    css = load_text(STYLE_FILE)

    html = html.replace("__TEMPLATE_TITLE__", APP_TITLE)
    html = html.replace("__CSS_STYLE__", css)
    html = html.replace("__USER_HEADING__", user_heading)
    html = html.replace("__TEMPLATE_MOVIE_GRID__", list_items)

    output_file = os.path.join(OUTPUT_DIR, filename) 
    save_webpage(output_file, html)    

    print("Website was generated successfully.")