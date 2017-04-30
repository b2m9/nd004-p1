import webbrowser
import os
import re
import csv

# Credits to Adarsh Nair, adarsh0806: https://github.com/adarsh0806
# Source: https://github.com/adarsh0806/ud036_StarterCode


class Movie:
    """Simple data structure to model a `Movie`."""
    def __init__(self, title, img, trailer):
        self.title = title
        self.img = img
        self.trailer = trailer


def create_movie_tiles_content(movies: list) -> str:
    """Creates HTML snippet for each entry in given list of `movies`.
    Returns snippet as `str`."""
    # The HTML content for this section of the page
    content = ''
    for movie in movies:
        # Extract the youtube ID from the url
        youtube_id_match = re.search(
            r'(?<=v=)[^&#]+', movie.trailer)
        youtube_id_match = youtube_id_match or re.search(
            r'(?<=be/)[^&#]+', movie.trailer)

        trailer_youtube_id = (youtube_id_match.group(0) if youtube_id_match
                              else None)

        # Append the tile for the movie with its content filled in
        content += movie_tile_content.format(
            title=movie.title,
            image_url=movie.img,
            trailer_id=trailer_youtube_id
        )

    return content


def open_movies_page(movies: list) -> None:
    """Create movie page out of given list of `movies`. Returns `None`."""
    # Create or overwrite the output file
    output_file = open('dist/fresh_tomatoes.html', 'w')

    # Replace the movie tiles placeholder generated content
    rendered_content = main_page_content.format(
        movie_tiles=create_movie_tiles_content(movies))

    # Output the file
    output_file.write(main_page_head + rendered_content)
    output_file.close()

    # open the output file in the browser (in a new tab, if possible)
    url = os.path.abspath(output_file.name)
    webbrowser.open('file://' + url, new=2)


def parse_template(path: str) -> str:
    """Parse given html file via `path` and return it as `str`."""
    template = ""

    with open(path) as file:
        for line in file.readlines():
            template = template + line

    return template


def get_movies(path: str) -> list:
    """Parse given csv file via `path` to list of instances of `Movie`."""
    movies = []

    with open(path) as file:
        for line in csv.DictReader(file):
            movies.append(Movie(line["title"],
                                line["img_url"],
                                line["trailer_url"]))

    return movies


if __name__ == "__main__":
    # Styles and scripting for the page
    main_page_head = parse_template("templates/header.html")

    # The main page layout and title bar
    main_page_content = parse_template("templates/body.html")

    # A single movie entry html template
    movie_tile_content = parse_template("templates/movie.html")

    open_movies_page(get_movies("data/movies.csv"))
