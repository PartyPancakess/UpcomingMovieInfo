# Upcoming Movies
A python program to scrape movie info from IMDB's upcoming movies section.

This console program can be used with Python's BeautifulSoup library.

## Commands
-INPUT: Loads the specified month's info on movies from IMDB's coming movies page. <br/>Example command: INPUT april_coming.txt

-LIST: Prints the movie names of loaded months. <br/>Example command: LIST

-LIST from: Prints the movie names of loaded months starting from the date specified. <br/>Example command: LIST from:2019-04-05

-LIST from-to: Prints the movie names of loaded months starting from and until the dates specified. <br/>Example command: LIST from:2019-04-05 to:2019-04-10

-LIST genre: Prints the movie names of loaded months with specified genre(s). <br/>Example command: LIST genre:Action,Sci-Fi

-INFO: Prints some information about the movie specified. <br/>Example command: INFO The Lion King
