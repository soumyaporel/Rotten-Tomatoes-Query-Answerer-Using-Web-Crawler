import ply.lex as lex
import ply.yacc as yacc

# List of token names.   This is always required
tokens = (
    'HIRATED', 'LORATED', 'BDAY',
    'LMOVIE', 'MOVIE', 
)


def t_HIRATED(t):
    r'Highest\s+Rated:\s*<span\s+class="label">\s*<span\s+class="[^"]*?"\s+title="[^"]*?">\s*</span>[^<]*?<a\s+class="[^"]*?"\s+href="([^"]*?)">\s*(.+)\s*</a>'
    movie = t.lexer.lexmatch.group(3)
    movie = movie.replace('\n', '')
    movie = ' '.join(movie.split())
    t.value = movie.strip()
    return t


def t_LORATED(t):
    r'Lowest\s+Rated:\s*<span\s+class="label">\s*<span\s+class="[^"]*?"\s+title="[^"]*?">\s*</span>[^<]*?<a\s+class="[^"]*?"\s+href="([^"]*?)">\s*(.+)\s*</a>'
    movie = t.lexer.lexmatch.group(6)
    movie = movie.replace('\n', '')
    movie = ' '.join(movie.split())
    t.value = movie.strip()
    return t


def t_BDAY(t):
    r'<p\s+class="celebrity-bio__item"\s+data-qa="celebrity-bio-bday">\s*Birthday:\s*(.+)\s*</p>'
    t.value = t.lexer.lexmatch.group(8)
    return t


def t_LMOVIE(t):
    r'Movies</h3>\s*<div\s+class="scroll-x">\s*<table>\s*<thead\s*class="celebrity-filmography__thead">[\s\S]*?</thead>\s*<tbody\s+class="celebrity-filmography__tbody">'
    t.value = 'lmovie'
    return t


def t_MOVIE(t):
    r'<tr\s*data-title="(.+)"\s*[^>]*?>\s*<td\s+class="celebrity-filmography__score-content">[\s\S]*?\s*<td\s+class="celebrity-filmography__year">\s*([0-9]+)\s*</td>\s*</tr>'
    movie_name = t.lexer.lexmatch.group(11)
    movie_name = movie_name.replace("&#39;", "'")
    t.value = {'movie': movie_name, 'year': int(t.lexer.lexmatch.group(12))}
    return t


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# Error handling rule
def t_error(t):
    t.lexer.skip(1)


# parsing rules
def p_start(p):
    '''
    start : hi_rated lo_rated b_day movies
    '''
    if p[4] != None: p[4].reverse()
    p[0] = {'highest rated movie': p[1], 'lowest rated movie': p[2], 'birthday': p[3], 'other movies': p[4]}


def p_hirated(p):
    '''
    hi_rated : HIRATED
            | empty
    '''
    if p[1] == None: # 2nd option
        return None # no tokens for this parsing were found. return.         
    p[0] = p[1]


def p_lorated(p):
    '''
    lo_rated : LORATED
             | empty
    '''
    if p[1] == None: # 2nd option
        return None # no tokens for this parsing were found. return.         
    p[0] = p[1]


def p_bday(p):
    '''
    b_day : BDAY
          | empty
    '''
    if p[1] == None: # 2nd option
        return None # no tokens for this parsing were found. return.         
    p[0] = p[1]


def p_movies(p):
    '''
    movies : LMOVIE MOVIE
           | movies MOVIE
           | empty
           | MOVIE empty 
    '''
    #print("x", p[1])
    if p[1] == None: # 4th option
        return None # no MOVIE tokens were found. return.

    if p[2] == None: # 5th option
        p[0] += p[1] # end recursion and return

    elif p[1] == 'lmovie': # 1st option
        p[0] = [p[2]] # get the first MOVIE

    else: # 2nd option
        p[0] = [p[2]]
        if p[1] != None:
            p[0] += p[1] # p[1] is the list of previous movies



def p_empty(p):
    'empty : '
    p[0] = None


def p_error(p):
    print('syntax error!!!')


def get_lexer_and_parser_for_cast_page():
    lexer = lex.lex(debug=0) # build the lexer
    parser = yacc.yacc(debug=0) # build the parser
    return (lexer, parser)
