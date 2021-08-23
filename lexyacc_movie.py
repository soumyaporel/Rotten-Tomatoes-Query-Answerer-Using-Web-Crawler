import ply.lex as lex
import ply.yacc as yacc

# List of token names.   This is always required
tokens = (
    'MOVIENAME',
    'ORIGLANG',
    'DIRECTOR',
    'CELEB', 'CASTCHAR',
    'LWRITER', 'LPRODUCER', 'LCASTCHAR', 
    'STORYLINE', 'BOXOFFICE', 'RUNTIME',
    'WHWATCH', 'ALSOLIKE',
)


def t_MOVIENAME(t):
    r'<title>(.+)\s+-\s+Rotten\s+Tomatoes</title>'
    t.value = t.lexer.lexmatch.group(2)
    return t


def t_ORIGLANG(t):
    r'<div\s+class="meta-label\s+subtle"\s+data-qa="movie-info-item-label">Original\s+Language:</div>\s*<div\s+class="meta-value"\s+data-qa="movie-info-item-value">(.+)\s*</div>'
    orig_lang = t.lexer.lexmatch.group(4) 
    t.value = orig_lang 
    return t


def t_DIRECTOR(t):
    r'<a\s+href="/celebrity/[^"]*?"\sdata-qa="movie-info-director">([^<]*?)</a>'
    t.value = t.lexer.lexmatch.group(6)
    return t


def t_CELEB(t):
    r'<a\s+href="/celebrity/.+">(.+)</a>'
    celeb_name = t.lexer.lexmatch.group(8)
    t.value = {'val': celeb_name}
    return t


def t_CASTCHAR(t):
    r'<a\s+href="(\s*/celebrity/.+\s*)"\s+class="unstyled\s+articleLink"\s+data-qa="cast-crew-item-link">\s*<span\s+title="(.+)">\s*.+\s*</span>\s*</a>\s*<span\s+class="characters\s+subtle\s+smaller"\s+title=".+">\s*<br\s*/>\s*([^<]*?)<br\s*/>\s*(</span>|Voice\s*</span>)'     
    cast_name = t.lexer.lexmatch.group(11).strip()
    cast_name = cast_name.replace("&#39;", "'")
    character_name = t.lexer.lexmatch.group(12).strip()
    character_name = character_name.replace("&#39;", "'")
    cast_char = {'link': "https://www.rottentomatoes.com" + t.lexer.lexmatch.group(10).strip(), 'cast': cast_name, 'character': character_name}
    t.value = cast_char 
    return t 


def t_LWRITER(t):
    r'<div\s+class="meta-label\s+subtle"\s+data-qa="movie-info-item-label">Writer:\s*</div>\s*<div\s+class="meta-value"\s+data-qa="movie-info-item-value">'
    t.value = {'val': 0}
    return t


def t_LPRODUCER(t):
    r'<div\s+class="meta-label\s+subtle"\s+data-qa="movie-info-item-label">Producer:\s*</div>\s*<div\s+class="meta-value"\s+data-qa="movie-info-item-value">'
    t.value = {'val': 0}
    return t


def t_LCASTCHAR(t):
    r'<div\s+class="castSection\s+"\s+data-qa="cast-section">'
    t.value = {'cast': 0}
    return t


def t_STORYLINE(t):
    r'<h2\s+class="panel-heading"\s+data-qa="movie-info-section-title">Movie\s+Info</h2>\s*<div\s+class="panel-body\s+content_body">\s*<div\s+class="sr-only\s+js-clamp-live-region"\s+aria-live="polite"></div>\s*<div\s+id="movieSynopsis"\s+class="movie_synopsis\s+clamp\s+clamp-6\s+js-clamp"\s+style="clear:both"\s+data-qa="movie-info-synopsis">\s*([^<]*?)\s*</div>'
    t.value = t.lexer.lexmatch.group(18).strip()
    return t


def t_RUNTIME(t):
    r'<li\s+class="meta-row\s+clearfix"\s+data-qa="movie-info-item">\s*<div\s+class="meta-label\s+subtle"\s+data-qa="movie-info-item-label">Runtime:</div>\s*<div\s+class="meta-value"\s+data-qa="movie-info-item-value">\s*<time\s+datetime=".+">\s*(.+)\s*</time>'
    t.value = t.lexer.lexmatch.group(20).strip()
    return t


def t_BOXOFFICE(t):
    r'<div\s+class=\"meta-label\s+subtle\"\s+data-qa=\"movie-info-item-label\">Box\s+Office\s+([^<]*?)</div>\s*<div\s+class=\"meta-value\"\s+data-qa=\"movie-info-item-value\">(.+)</div>\s*'
    t.value = t.lexer.lexmatch.group(23).strip()
    return t


def t_WHWATCH(t):
    r'<a\s+class="affiliate__link\s+affiliate__link--veneer\s+js-affiliate-link"\s+data-affiliate="(.+?)"\s+target="blank"\s+href="([^\s"]*)"\s+data-qa="affiliate-item-lnk">\s*<affiliate-icon\s+name="(.+)"\s+alignicon="left\s+center"></affiliate-icon>\s*<p\s+class="affiliate__text\s+affiliate__text--veneer\s+show-price\s+hide"\s+>'
    t.value = t.lexer.lexmatch.group(25).strip()
    return t


def t_ALSOLIKE(t):
    r'<a\shref="(.+)"\s+class="recommendations-panel__poster-link">\s*<tile-poster.+">\s*<tile-poster-image\s+slot="image">\s*<img[^<]*</tile-poster-image>\s*<tile-poster-meta\s+slot="meta">\s*<score[^<]*</score-icon-critic>\s*<score[^<]*</score-icon-audience>\s*<span\s+slot="title"\s+class="recommendations-panel__poster-title">(.+)</span>\s*</tile-poster-meta>\s*</tile-poster>\s*</a>'
    movie_name = t.lexer.lexmatch.group(30)
    movie_name = movie_name.replace("&#39;", "'")
    t.value = {'link': "https://www.rottentomatoes.com" + t.lexer.lexmatch.group(29), 'moviename': movie_name}
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
    start : movie_name also_likes movie_whwatches movie_storyline orig_lang director_names producer_names writer_names boxoffice_collection movie_runtime castchar_names
    '''
    if p[7] != None: p[7].reverse()
    if p[8] != None: p[8].reverse()
    if p[11] != None: p[11].reverse()
    p[0] = {'movie name': p[1], 'you might also like': p[2], 'where to watch': p[3], 'storyline': p[4], 'original language': p[5], 'director': p[6], 'producer': p[7], 'writers': p[8], 'box office collection': p[9], 'runtime': p[10], 'cast with the character name': p[11]}


def p_movie_name(p):
    '''
    movie_name : MOVIENAME
               | empty
    '''
    if p[1] == None: # 2nd option
        return None # no MOVIENAME tokens were found. return.         
    p[0] = p[1]


def p_director_names(p):
    '''
    director_names : DIRECTOR director_names
                   | DIRECTOR empty
                   | empty
    '''
    if p[1] == None: # 3rd option
        return None # no DIRECTOR tokens were found. return.

    p[0] = [p[1]] # the new director
    if p[2] != None: 
        p[0] += p[2] # list of previous directors


def p_writer_names(p):
    '''
    writer_names : LWRITER CELEB
                 | writer_names CELEB
                 | CELEB empty
                 | empty
    '''
    if p[1] == None: # 4th option
        return None # no WRITER tokens were found. return.

    if p[2] == None: # 3rd option
        p[0] += p[1]['val'] # end recursion and return

    elif type(p[1]) == dict: # 1st option
        p[0] = [p[2]['val']] # get the first writer

    else: # 2nd option
        p[0] = [p[2]['val']]
        if p[1] != None:
            p[0] += p[1] # p[1] is the list of previous writers


def p_producer_names(p):
    '''
    producer_names : LPRODUCER CELEB
                   | producer_names CELEB
                   | producer_names empty
                   | empty
    '''
    if p[1] == None: # 4th option
        return None # no PRODUCER tokens were found. return.

    if p[2] == None: # 3rd option
        p[0] += p[1]['val'] # end recursion and return

    elif type(p[1]) == dict: # 1st option
        p[0] = [p[2]['val']] # get the first producer

    else: # 2nd option
        p[0] = [p[2]['val']]
        if p[1] != None:
            p[0] += p[1] # p[1] is the list of previous producers


def p_orig_lang(p):
    '''
    orig_lang : ORIGLANG
              | empty
    '''
    if p[1] == None: # 2nd option
        return None # no ORIGLANG tokens were found. return.
    p[0] = p[1]


def p_castchar_names(p):
    '''
    castchar_names : LCASTCHAR CASTCHAR
                   | castchar_names CASTCHAR
                   | CASTCHAR empty
                   | empty
                   | LCASTCHAR empty
    '''
    if p[1] == None: # 4th option
        return None # no LCASTCHAR and CASTCHAR tokens were found. return.

    if type(p[1]) == dict and p[2] == None: # 5th option
        return None # no CASTCHAR tokens were found. return.

    if p[2] == None: # 3rd option
        p[0] += p[1]['cast'] # end recursion and return

    elif type(p[1]) == dict: # 1st option
        p[0] = [{'cast': p[2]['cast'], 'character': p[2]['character'], 'link': p[2]['link']}] # get the first cast

    else: # 2nd option
        p[0] = [{'cast': p[2]['cast'], 'character': p[2]['character'], 'link': p[2]['link']}]
        if p[1] != None:
            p[0] += p[1] # p[1] is the list of previous casts


def p_storyline(p):
    '''
    movie_storyline : STORYLINE
                    | empty
    '''
    if p[1] == None: # 2nd option
        return None # no STORYLINE tokens were found. return.
    p[0] = p[1]


def p_boxoffice(p):
    '''
    boxoffice_collection : BOXOFFICE
                         | empty
    '''
    if p[1] == None: # 2nd option
        return None # no BOXOFFICE tokens were found. return.
    p[0] = p[1]


def p_movie_runtime(p):
    '''
    movie_runtime : RUNTIME
                  | empty
    '''
    if p[1] == None: # 2nd option
        return None # no RUNTIME tokens were found. return.
    p[0] = p[1]


def p_whwatch(p):
    '''
    movie_whwatches : WHWATCH movie_whwatches
                    | WHWATCH empty
                    | empty
    '''
    if p[1] == None: # 3rd option
        return None # no WHWATCH tokens were found. return.
    
    p[0] = [p[1]] # the new where to watch platform name

    if p[2] != None: 
        p[0] += p[2] # list of previous platforms


def p_also_likes(p):
    '''
    also_likes : ALSOLIKE also_likes
               | ALSOLIKE empty
               | empty
    '''
    if p[1] == None: # 3rd option
        return None # no ALSOLIKE tokens were found. return.
    
    p[0] = [p[1]] # the new you might also like movie link and movie name

    if p[2] != None: 
        p[0] += p[2] # list of previous you might also likes


def p_empty(p):
    'empty : '
    p[0] = None


def p_error(p):
    print('syntax error!!!')


def get_lexer_and_parser_for_movie_page():
    lexer = lex.lex(debug=0) # build the lexer
    parser = yacc.yacc(debug=0) # build the parser
    return (lexer, parser)

