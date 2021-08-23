# Rotten-Tomatoes-Query-Answerer-Using-Web-Crawler

Crawls pages in the RottenTomatoes website and extracts the required information from them according to user queries by creating suitable grammar rules and parsing the HTML files/pages using the PLY package in python.


### WEBSITE INFO:
	RottenTomatoes is an IMDb like website where one can find an online database of information related to films, television programs
	and also cast, production crew, personal biographies, plot summaries, trivia, ratings, critic and fan reviews.
	
	
### DATA USED:
	-> The 'rottentomatoes_genre_links.txt' file contains URL links for ten different genre-wise top 100 movie lists.
	
	
### EXECUTING THE PROGRAM:
	-> Enter the command: python3 extractor.py 
	-> 'lexyacc_movie.py', 'lexyacc_cast.py', 'rottentomatoes_genre_links.txt' must be present in the same directory before execution.
		

### PROGRAM FLOW:

	-> The user has to first input one of the ten genres.
	-> The 'rottentomatoes_genre_links.txt' file is scanned to get the link of the genre page.
	-> Then the list of top 100 movies of that genre is printed on console by crawling the HTML file for that genre.
	-> The user then selects a particular movie name from the list.
	-> The corresponding movie page (HTML file) is downloaded/fetched (no need to save explicitly)
	-> The user is asked to input a query about the movie (list of available queries are printed on console)
	-> Syntax of the HTML files is studied to create grammar using PLY (or C code using Lex,Yacc) to extract the following fields of the movies.
		● Movie Name
		● Director
		● Writers
		● Producer
		● Original Language
		● Cast with the character name
		● Storyline
		● Box Office Collection
		● Runtime
		● YOU MIGHT ALSO LIKE - Similar kind of movie suggestions
		● WHERE TO WATCH - Online platforms where the movie can be seen.
		● Select a Movie From Another Genre
		(other fields except the above are ignored) 

	-> The program shows all the possible query fields a user can ask for (from the above list items). 
	-> If the query is valid, then the result is shown and the user is asked to put other queries in a loop.	
	
    Details about some of the options are given below:  
	
		YOU MIGHT ALSO LIKE: 
			-> The similar movies are displayed.
			-> The user can input from the listed movies and is again presented the same options list.
			-> Here, the code performs recursive crawling.
				Ex: 
				Movie1 → YOU MIGHT ALSO LIKE[list of movies] → user select one of them → the fields are displayed 
				→ again user may ask for YOU MIGHT ALSO LIKE
				[So basically it can go on until user wants to exit]
			-> Also, an option is added ("Previous Movie's Query Select Menu") for going back to the previous movie.
	
		CAST WITH THE CHARACTER NAME:
			-> The list of casts and their characters in the movie are shown and the user selects one cast from the list.
			-> Given the input, the actor/actress profile is fetched and the user can further query on the following options:
				● Highest Rated film
				● Lowest Rated film
				● Birthday
				● Other Movies
				● Previous Movie's Query Select Menu  
			-> For "OTHER MOVIES", the user inputs a year (as a filter) and the list of movies of the cast on or after that year are shown.
			-> The "PREVIOUS MOVIE'S QUERY SELECT MENU" option takes the user back to the query select option of the previous movie from which the current cast was select.

        SELECT A MOVIE FROM ANOTHER GENRE:
            -> The genre list is shown and the user selects one genre (same as in the beginning of the program)
            -> Then the list of top 100 movies in that genre is shown and the user selects one movie from this list.


### OTHER INFO:
	-> The codes parsing the movie pages are written in 'lexyacc_movie.py'.
	-> The codes parsing the cast pages are written in 'lexyacc_cast.py'.
	-> 'extractor.py' imports functions from 'lexyacc_movie.py', 'lexyacc_cast.py' to perform the required tasks.
	-> Matching of the user input for the genre name, movie name etc. with the actual names are done in case insensitive manner.
    -> The program was developed using Python version: 3.8.5 [OS: Ubuntu 20.04.2]
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
