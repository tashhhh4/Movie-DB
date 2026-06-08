# MovieDB
A command line app for managing your own personal list of favorite movies!


## Features
- Add, update, delete, and view movies in your database.
- Automatic saving after every operation.
- Command-Line interface (CLI)
- Generate statistics, printed to the terminal or as a PNG image.
- Generate an HTML website based on your movies.


## How to install and run
### Using uv (very easy)
uv is a wrapper that simplifies installing, running, and distributing Python projects! If you don't have it, you can follow the instructions to install it here: https://docs.astral.sh/uv/getting-started/installation/

    uv venv
    uv pip install -r requirements.txt
    
    uv run main.py

### Manually configuring venv and installing requirements
(Note: the commands for creating and activating venv can vary depending on your operating system and python installation)

    python -m venv .venv
    source ./.venv/bin/activate

    pip install -r requirements.txt

    python main.py