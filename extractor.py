import urllib.request, urllib.error, urllib.parse
import re
from lexyacc_movie import get_lexer_and_parser_for_movie_page
from lexyacc_cast import get_lexer_and_parser_for_cast_page

# scans the file containing genre links and returns the link for the input genre
# handles extra whitespaces at the left and right side of the genre string and performs case insensitive matching
def get_genre_url(input_genre):  
    genre = input_genre.strip().lower() 
    genre_url = None
    
    with open('rottentomatoes_genre_links.txt') as genre_link_file:
        genre_link_file_content = genre_link_file.readlines()
    
    for line_no in range(len(genre_link_file_content)):
        line = genre_link_file_content[line_no].strip().lower()
        if genre == line:
            genre_link = genre_link_file_content[line_no + 1].strip()
            genre_link = genre_link.replace('\u200b', '')
            return genre_link

    print("ERROR: genre link not found!")
    quit()


# prints all the possible genres for which links are available in the .txt file 
def get_genre_list():  
    with open('rottentomatoes_genre_links.txt') as genre_link_file:
        genre_link_file_content = genre_link_file.readlines()
    res = ''
    for i in genre_link_file_content[::2]:
        res += i 
    return res


# fetches the page content for the given url
def get_page_content(input_url):
    response = urllib.request.urlopen(input_url)
    file_content = response.read()
    return file_content.decode()


# fetches the page content for the input genre
def get_genre_page_content(input_genre):
    genre_url = get_genre_url(input_genre)
    genre_page_content = get_page_content(genre_url)
    return genre_page_content


# get the list of 100 movies in the genre page 
def get_movie_list(genre_page_content):
    
    movie_names_matches = re.findall('<td>\\s*<a\\s+href=".*"\\s+class="unstyled articleLink">\\s*(.*?)\\s*</a>\\s*</td>', genre_page_content)

    movie_list = []
    for matched_pattern in movie_names_matches:
        movie = matched_pattern
        movie_list.append(movie)

    return movie_list


# adds escape chars before special chars to match the str correctly using regex
def escape_str(s):
    new_s = ''
    special_chars = ['(', ')']
    for i in s:
        if i in special_chars:
            new_s += f"\{i}"
        else:
            new_s += i
    return new_s


# formats the movie name to match correctly using regex
def format_movie_name(movie_name):
    movie_escaped = escape_str(movie_name)
    movie_regex = '\\s*'
    movie_tokens = movie_escaped.split()
    for i in movie_tokens[:-1]:
        movie_regex += i
        movie_regex += '\\s+'
    movie_regex += movie_tokens[-1]
    movie_regex += '\\s*'
    return movie_regex


def get_movie_link_from_genre_page(movie_name, genre_page_content):
    
    formatted_movie_name = format_movie_name(movie_name)

    # get the link for the input movie from the genre page
    movie_link = None
    movie_link_match = re.findall('<td>\s*<a\s+href="(.*?)"\s+class="unstyled articleLink">\s*(' + formatted_movie_name + ')\s*</a>\s*</td>', genre_page_content, flags=re.IGNORECASE)
    for matched_pattern in movie_link_match:
        orig_movie_name = matched_pattern[1]
        movie_link = "https://www.rottentomatoes.com" + matched_pattern[0] # link found
        break
    
    return movie_link


def get_cast_info_from_cast_link(cast_link, cast_name):

    cast_page_content = get_page_content(cast_link)
    print(f'\nParsing the cast page for "{cast_name}"...') 
    lexer, parser = get_lexer_and_parser_for_cast_page()
    lexer.input(cast_page_content) # Give the lexer some input
    parsed_cast_info = parser.parse(cast_page_content) # Parse and get the parsed_cast_info

    if parsed_cast_info == None:
        print("ERROR: cannot parse the cast page!")
        quit()

    print(f"The cast page is parsed successfully!")
    return parsed_cast_info


def show_cast_info(parsed_cast_info, cast_name):

        while True:

            cast_info_options = ["highest rated movie", "lowest rated movie", "birthday", "other movies", "Previous Movie's Query Select Menu"]
            
            print(f'\nAvailable options (for the cast "{cast_name}"):')
            for i in cast_info_options[:-1]:
                print(i.title())
            print("Previous Movie's Query Select Menu")
            
            selected_cast_info_option = input("\nChoose which information you want to see about the cast from the above list\n(type 'exit' to terminate the program):\n")
            selected_cast_info_option = selected_cast_info_option.strip().lower()

            if selected_cast_info_option == 'exit':
                print("Exiting...")
                quit() 

            if selected_cast_info_option == "previous movie's query select menu":
                print("\nGoing back to the query select menu for the previous movie...")
                return

            if selected_cast_info_option not in cast_info_options:
                print("ERROR: please select a valid option!")
                continue # give the user another chance

            print()
            for i in parsed_cast_info:
                if i == selected_cast_info_option:
                    if parsed_cast_info[i]:

                        if i == 'other movies':
                            while True:
                                try:
                                    input_year = int(input("Please enter a year:\n"))
                                    break
                                except:
                                    print("ERROR: please enter a valid year!\n")

                            print(f"\nThe list of movies of {cast_name} on or after the year {input_year}:\n")
                            
                            movie_shown = False
                            for j in parsed_cast_info[i]:
                                if j['year'] >= input_year:
                                    movie_shown = True
                                    print(f"{j['movie']} (year: {j['year']})")
                            if not movie_shown:
                                print("Sorry. No movies were found!")
                        else:
                            print(f'{i.title()} of {cast_name}:\n{parsed_cast_info[i]}')

                    else:
                        print("Sorry. The requested information is not available!")
        

def get_movie_info_from_movie_link(movie_link, input_movie_name):
    
    movie_page_content = get_page_content(movie_link)
    
    print(f'\nParsing the movie page for "{input_movie_name}"...') 
    lexer, parser = get_lexer_and_parser_for_movie_page()
    lexer.input(movie_page_content) # Give the lexer some input
    parsed_movie_info = parser.parse(movie_page_content) # Parse and get the parsed_movie_info

    if parsed_movie_info == None:
        print("ERROR: cannot parse the movie page!")
        quit()

    print(f"The movie page is parsed successfully!")
    return parsed_movie_info


def show_movie_info(parsed_movie_info, is_first_level_of_recursion):

        while True:

            movie_info_options = ["Movie Name", "Director", "Writers", "Producer", "Original Language", "Cast With the Character Name", "Storyline", "Box Office Collection", "Runtime"]
            movie_info_options.extend(["YOU MIGHT ALSO LIKE", "WHERE TO WATCH"])
            movie_info_options.append("Select a Movie From Another Genre")
            if not is_first_level_of_recursion:
                movie_info_options.append("Previous Movie's Query Select Menu")

            orig_movie_name = parsed_movie_info['movie name']
            
            print(f'\nAvailable options (for the movie "{orig_movie_name}"):')
            for i in movie_info_options:
                print(i)
            
            selected_movie_info_option = input("\nChoose which information you want to see about the movie from the above list\n(type 'exit' to terminate the program):\n")
            selected_movie_info_option = selected_movie_info_option.strip().lower()

            if selected_movie_info_option == 'exit':
                print("Exiting...")
                quit() 

            if not is_first_level_of_recursion and selected_movie_info_option == "previous movie's query select menu":
                print("\nGoing back to the query select menu for the previous movie...")
                return 

            if selected_movie_info_option == 'select a movie from another genre':
                show_genre_select_menu()

            if selected_movie_info_option not in map(lambda x: x.strip().lower(), movie_info_options):
                print("ERROR: please select a valid option!")
                continue # give the user another chance

            print(f'\nFetching the information about "{selected_movie_info_option.title()}" for the movie "{orig_movie_name}"...\n')

            for i in parsed_movie_info:
                if i == selected_movie_info_option:
                    if parsed_movie_info[i]:

                        if i == 'director':
                            if len(parsed_movie_info[i]) == 1:
                                print(f'{i.title()}:\n{parsed_movie_info[i][0]}')
                            else:
                                print("The list of directors:")
                                for j in parsed_movie_info[i]:
                                    print(j)
                        

                        elif i == 'producer':
                            if len(parsed_movie_info[i]) == 1:
                                print(f'{i.title()}:\n{parsed_movie_info[i][0]}')
                            else:
                                print("The list of producers:")
                                for j in parsed_movie_info[i]:
                                    print(j)
                        

                        elif i == 'writers':
                            if len(parsed_movie_info[i]) == 1:
                                print(f'Writer:\n{parsed_movie_info[i][0]}')
                            else:
                                print("The list of writers:")
                                for j in parsed_movie_info[i]:
                                    print(j)  
                        

                        elif i == 'cast with the character name':
                            print("The list of cast with the character name:\n")
                            for j in parsed_movie_info[i]:
                                m_character  = j['character'].replace('\n', '')
                                m_character = ' '.join(m_character.split())
                                print(f"Cast: {j['cast']}\t|\tCharacter name: {m_character}")
                            
                            while True:
                                input_cast_name = input("\nSelect a cast name from the above list:\n").strip().lower()
                                input_cast_dict = None
                                for j in parsed_movie_info[i]:
                                    m_cast  = j['cast'].replace('\n', '')
                                    m_cast = ' '.join(m_cast.split())
                                    m_cast = m_cast.strip().lower()
                                    if m_cast == input_cast_name: # cast matched with input!
                                        input_cast_dict = j
                                        break
                                if input_cast_dict == None: # invalid input. give the user another chance.
                                    print("ERROR: please correctly select a cast from the list!")
                                    continue
                                else:
                                    break # as cast matched with input
                    
                            parsed_cast_info = get_cast_info_from_cast_link(input_cast_dict['link'], input_cast_dict['cast'])
                            show_cast_info(parsed_cast_info, input_cast_dict['cast'])

                            
                        elif i == 'WHERE TO WATCH'.lower():
                            print("The list of online platforms:")
                            for j in parsed_movie_info[i]:
                                print(j)


                        elif i == 'YOU MIGHT ALSO LIKE'.lower():
                            print("The list of movies you might also like:")
                            for j in parsed_movie_info[i]:
                                print(j['moviename'])
                            
                            while True:
                                might_also_like_input_movie = input("\nSelect a movie from the above list:\n")
                                might_also_like_input_movie_link = None
                                # search for the movie link 
                                for j in parsed_movie_info[i]:
                                    if j['moviename'].lower() == might_also_like_input_movie.lower():
                                        might_also_like_input_movie_link = j['link']
                                if might_also_like_input_movie_link == None:
                                    print("ERROR: please correctly select a movie from the list!")
                                    continue
                                else:
                                    break # movie link obtained
                            show_movie_info(parsed_movie_info=get_movie_info_from_movie_link(might_also_like_input_movie_link, might_also_like_input_movie), is_first_level_of_recursion=False) # recurse on the new movie


                        else:
                            print(f'{i.title()}:\n{parsed_movie_info[i]}')

                    else:
                        print("Sorry. The requested information is not available!")


def show_genre_select_menu():
    
    # select a genre get content of the genre page
    genre_list = get_genre_list().split("\n")
    print(f"\nAvailable genres:\n\n{get_genre_list()}") 
    while True:
        input_genre = input("Choose a genre from the above list:\n")
        input_genre = input_genre.strip().lower()
        if input_genre not in map(lambda x: x.strip().lower(), genre_list):
            print("ERROR: please select a valid genre!\n")
            continue # give the user another chance
        else:
            break
    
    print(f"\nFetching the page for the input genre ({input_genre})...")
    genre_page_content = get_genre_page_content(input_genre) 

    # show list of top 100 movies for this genre
    print(f'\nList of the top 100 movies for the input genre "{input_genre}":\n')
    movie_list = get_movie_list(genre_page_content) 
    for i in movie_list:
        print(i)

    while True:
        # select a movie name and fetch the movie page
        movie_name = input("\nEnter a movie name from the above list:\n")
        movie_link = get_movie_link_from_genre_page(movie_name, genre_page_content)
        if movie_link == None:
            print("ERROR: movie not found! Please try again.")
        else:
            break

    print(f'\nFetching the page for the input movie "{movie_name}"...')

    # parse the fetched movie page
    parsed_movie_info = get_movie_info_from_movie_link(movie_link, movie_name)
    
    # display query select menu for this movie
    show_movie_info(parsed_movie_info=parsed_movie_info, is_first_level_of_recursion=True)
    

def main():
    show_genre_select_menu()    
                        

if __name__ == '__main__':
    main()