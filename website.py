import os
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


# Website Generator
def generate():
    movies = [
        {"title": "Titanic", "poster_url": "https://m.media-amazon.com/images/M/MV5BMDdmZGU3NDQtY2E5My00ZTliLWIzOTUtMTY4ZGI1YjdiNjk3XkEyXkFqcGdeQXVyNTA4NzY1MzY@._V1_SX300.jpg", "rating": "8.0", "year": 1997},
        {"title": "Titanic", "poster_url": "https://m.media-amazon.com/images/M/MV5BMDdmZGU3NDQtY2E5My00ZTliLWIzOTUtMTY4ZGI1YjdiNjk3XkEyXkFqcGdeQXVyNTA4NzY1MzY@._V1_SX300.jpg", "rating": "8.0", "year": 1997},
        {"title": "Titanic", "poster_url": "https://m.media-amazon.com/images/M/MV5BMDdmZGU3NDQtY2E5My00ZTliLWIzOTUtMTY4ZGI1YjdiNjk3XkEyXkFqcGdeQXVyNTA4NzY1MzY@._V1_SX300.jpg", "rating": "8.0", "year": 1997},
    ]
    username = "Tasha"
    
    list_items = ''
    for movie in movies:
        list_items += f'<li><div class="movie"><img class="movie-poster" src="{movie["poster_url"]}" title><div class="movie-title">{movie["title"]}</div><div class="movie-year">{movie["year"]}</div>'

    html = load_text(TEMPLATE_FILE)
    css = load_text(STYLE_FILE)
    html = html.replace("__TEMPLATE_TITLE__", APP_TITLE)
    html = html.replace("__CSS_STYLE__", css)
    html = html.replace("__USERNAME__", username)
    html = html.replace("__TEMPLATE_MOVIE_GRID__", list_items)

    output_file = os.path.join(OUTPUT_DIR, f"{username}.html") 
    save_webpage(output_file, html)    

    print("Website was generated successfully.")