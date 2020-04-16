#########################################
##### Name:      Josue Figueroa     #####
##### Uniqname:       josuef        #####
#########################################

from bs4 import BeautifulSoup
import requests
import json
import time
import sqlite3

BASE_URL = 'https://www.imdb.com'
TOP_RATED_DICT = {'movies': 'https://www.imdb.com/chart/top/?ref_=nv_mv_250',
                  'shows': 'https://www.imdb.com/chart/toptv/?ref_=nv_tvv_250'}
DBNAME = 'project4.sqlite'
GENRE_LIST = {  1: 'Action', 2: 'Adventure', 3: 'Animation', 4: 'Biography', 5: 'Comedy', 6: 'Crime',
                7: 'Documentary', 8: 'Drama', 9: 'Family', 10: 'Fantasy', 11: 'Film-Noir', 12: 'History',
                13: 'Horror', 14: 'Music', 15: 'Musical', 16: 'Mystery', 17: 'Reality-TV', 18: 'Romance',
                19: 'Sci-Fi', 20: 'Sport', 21: 'Talk-Show', 22: 'Thriller', 23: 'War', 24: 'Western'}
SHOW_TYPE_LIST = {1: 'TV Series', 2: 'TV Mini-Series'}
RATINGS_LIST = {1: 'G', 2: 'GP', 3: 'PG', 4: 'PG-13', 5: 'NC-17', 6: 'M', 7: 'R', 8: 'X', 9: 'TV-Y',
                10: 'TV-Y7', 11: 'TV-Y7-FV', 12: 'TV-G', 13: 'TV-PG', 14: 'TV-14', 15: 'TV-MA',
                16: 'Approved', 17: 'Passed', 18: 'Not Rated'}
CACHE_FILE_NAME = 'cache.json'
CACHE_DICT = {}
HEADERS = {
    'User-Agent': 'UMSI 507 Final Project - Python Crawling and Scraping',
    'From': 'josuef@umich.edu',
    'Course-Info': 'https://si.umich.edu/programs/courses/507'
}
############### CACHE FUNCTIONS ###############
def load_cache():
    ''' Opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary.
    if the cache file doesn't exist, creates a new cache dictionary

    Parameters
    ----------
    None

    Returns
    -------
    The opened cache: dict
    '''
    try:
        cache_file = open(CACHE_FILE_NAME, 'r')
        cache_file_contents = cache_file.read()
        cache = json.loads(cache_file_contents)
        cache_file.close()
    except:
        cache = {}
    return cache

def save_cache(cache):
    ''' Saves the current state of the cache to disk

    Parameters
    ----------
    cache: dict
        The dictionary to save

    Returns
    -------
    None
    '''
    cache_file = open(CACHE_FILE_NAME, 'w')
    contents_to_write = json.dumps(cache)
    cache_file.write(contents_to_write)
    cache_file.close()

def make_url_request_using_cache(url, cache):
    '''Check the cache for a saved result for this baseurl inside cache:
    values combo. If the result is found, return it. Otherwise send a new
    request, save it, then return it.

    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    cache: dict
        A cache with previously used url searches

    Returns
    -------
    dict
        the results of the query as a dictionary loaded from cache
        JSON
    '''
    if (url in cache.keys()):
        # print("Using cache")
        return cache[url]
    else:
        # print("Fetching")
        time.sleep(1)
        response = requests.get(url, headers=HEADERS)
        cache[url] = response.text
        save_cache(cache)
        return cache[url]

############### DATABASE FUNCTIONS ###############
def create_database():
    '''Creates database to be populated with IMDb data

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    drop_movies = '''
        DROP TABLE IF EXISTS "Movies";
    '''
    create_movies = '''
        CREATE TABLE IF NOT EXISTS "Movies" (
            "Id"            INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            "MovieTitle"    TEXT NOT NULL,
            "FilmRatingId"  INTEGER NOT NULL,
            "Country"       TEXT NOT NULL,
            "ReleaseYear"   INTEGER NOT NULL,
            "FirstGenreId"  INTEGER NOT NULL,
            "Length"        TEXT NOT NULL,
            "NumberRating"  REAL NOT NULL
        );
    '''
    cur.execute(drop_movies)
    cur.execute(create_movies)

    drop_shows = '''
        DROP TABLE IF EXISTS 'Shows';
    '''
    create_shows = '''
        CREATE TABLE 'Shows' (
        'Id'            INTEGER PRIMARY KEY AUTOINCREMENT,
        "ShowTitle"     TEXT NOT NULL,
        "ShowRatingId"  INTEGER NOT NULL,
        "YearsAired"    TEXT NOT NULL,
        "FirstGenreId"  INTEGER NOT NULL,
        "ShowTypeId"    INTEGER NOT NULL,
        "Length"        TEXT NOT NULL,
        "NumberRating"  REAL NOT NULL
        );
    '''
    drop_show_types = '''
        DROP TABLE IF EXISTS 'ShowTypes';
    '''
    create_show_types = '''
        CREATE TABLE 'ShowTypes' (
        'Id'            INTEGER PRIMARY KEY AUTOINCREMENT,
        "ShowType"      TEXT NOT NULL
        );
    '''
    cur.execute(drop_shows)
    cur.execute(create_shows)
    cur.execute(drop_show_types)
    cur.execute(create_show_types)

    drop_genres = '''
        DROP TABLE IF EXISTS 'Genres';
    '''
    create_genres = '''
        CREATE TABLE 'Genres' (
        'Id'    INTEGER PRIMARY KEY AUTOINCREMENT,
        "Genre" TEXT NOT NULL
        );
    '''
    drop_ratings = '''
        DROP TABLE IF EXISTS 'Ratings';
    '''
    create_ratings = '''
        CREATE TABLE 'Ratings' (
        'Id'            INTEGER PRIMARY KEY AUTOINCREMENT,
        "Rating"      TEXT NOT NULL
        );
    '''
    cur.execute(drop_genres)
    cur.execute(create_genres)
    cur.execute(drop_ratings)
    cur.execute(create_ratings)

    conn.commit()

    insert_genres = '''
        INSERT INTO Genres
        VALUES (NULL, ?)
    '''
    for genre in GENRE_LIST.values():
        cur.execute(insert_genres, [genre])
    insert_show_types = '''
        INSERT INTO ShowTypes
        VALUES (NULL, ?)
    '''
    for show_type in SHOW_TYPE_LIST.values():
        cur.execute(insert_show_types, [show_type])
    insert_ratings = '''
        INSERT INTO Ratings
        VALUES (NULL, ?)
    '''
    for rating in RATINGS_LIST.values():
        cur.execute(insert_ratings, [rating])
    conn.commit()
    conn.close()

def populate_database(top_media_type, top_item):
    '''Populates the database with data from IMDb

    Parameters
    ----------
    top_media_type: string
        The media type to determine when to get movies or shows information
    top_item: class
        An instance of a top rated movie or show

    Returns
    -------
    None
    '''
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    rating_id = ''
    genre_id = ''
    show_type_id = ''
    for key, rating in RATINGS_LIST.items():
        if top_item.rating == rating:
            rating_id = key
    for key, genre in GENRE_LIST.items():
        if top_item.genre[0] == genre:
            genre_id = key
    if top_media_type == 'movies':
        insert_movie = '''
            INSERT INTO Movies
            VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)
        '''
        movie = [top_item.title, rating_id, top_item.country, int(top_item.release_year),
                 genre_id, top_item.length, float(top_item.num_rating)]
        cur.execute(insert_movie, movie)
    else:
        for key, show_type in SHOW_TYPE_LIST.items():
            if top_item.show_type == show_type:
                show_type_id = key
        insert_show = '''
        INSERT INTO Shows
        VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)
        '''
        show = [top_item.title, rating_id, top_item.air_years, genre_id,
                show_type_id, top_item.length, float(top_item.num_rating)]
        cur.execute(insert_show, show)

    conn.commit()
    conn.close()

############### QUERIES ###############
def execute_query(query):
    ''' Executes a given SQL query

    Parameters
    ----------
    query
        string : SQL string

    Returns
    -------
    query_results
        list : a list of tuples that represent the query result
    '''
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()
    query_results = cursor.execute(query).fetchall()
    connection.close()
    return query_results

def get_query(query_num):
    if query_num == 1:
        query = movie_avg_num_rating_by_first_genre()
        query_result = execute_query(query)
    elif query_num == 2:
        query = movie_avg_num_rating_by_rating()
        query_result = execute_query(query)
    elif query_num == 3:
        query = movie_data()
        query_result = execute_query(query)
    elif query_num == 4:
        query = show_avg_num_rating_by_show_type()
        query_result = execute_query(query)
    elif query_num == 5:
        query = show_avg_num_rating_by_first_genre()
        query_result = execute_query(query)
    elif query_num == 6:
        query = show_avg_num_rating_by_rating()
        query_result = execute_query(query)
    else:
        query = show_data()
        query_result = execute_query(query)
    return query_result

def print_query_results(query_results):
    ''' Pretty prints query results

    Parameters
    ----------
    query_results
        list : a list of tuples that represent raw query result

    Returns
    -------
    None
    '''
    grid_width = 20
    for row in query_results:
        col_list = []
        for col in row:
            if type(col) == str:
                if len(str(col)) > 15:
                    col = (str(col[0:15]) + '...')
            if type(col) == float:
                col = round(col, 1)
            col_list.append(str(col))
        print("".join(str(col).ljust(grid_width) for col in col_list))
    print()


def movie_avg_num_rating_by_first_genre():
    query = f'''
            SELECT			g.Genre, AVG(m.NumberRating) as AvgRating
            FROM			Movies as m
            JOIN				Genres as g
                ON			m.FirstGenreId = g.Id
            GROUP BY		g.Genre;
            '''
    return query

def movie_avg_num_rating_by_rating():
    query = f'''
            SELECT			r.Rating, AVG(m.NumberRating) as AvgRating
            FROM			Movies as m
            JOIN				Ratings as r
                ON			m.FilmRatingId = r.Id
            GROUP BY		r.Rating;
            '''
    return query


def movie_data():
    query = f'''
            SELECT			m.MovieTitle, r.Rating, m.Country, m.ReleaseYear, g.Genre as FirstGenre, m.Length, m.NumberRating
            FROM			Movies as m
            JOIN				Ratings as r
                ON			m.FilmRatingId = r.Id
            JOIN				Genres as g
                ON			m.FirstGenreId = g.Id;
            '''
    return query

def show_avg_num_rating_by_show_type():
    query = f'''
            SELECT			st.ShowType, AVG(s.NumberRating) as AvgRating
            FROM			Shows as s
            JOIN				ShowTypes as st
                ON			s.ShowTypeId = st.Id
            GROUP BY		st.ShowType;
            '''
    return query
def show_avg_num_rating_by_first_genre():
    query = f'''
            SELECT			g.Genre, AVG(s.NumberRating) as AvgRating
            FROM			Shows as s
            JOIN				Genres as g
                ON			s.FirstGenreId = g.Id
            GROUP BY		g.Genre;
            '''
    return query
def show_avg_num_rating_by_rating():
    query = f'''
            SELECT			r.Rating, AVG(s.NumberRating) as AvgRating
            FROM			Shows as s
            JOIN				Ratings as r
                ON			s.ShowRatingId = r.Id
            GROUP BY		r.Rating;
            '''
    return query
def show_data():
    query = f'''
            SELECT			s.ShowTitle, r.Rating, s.YearsAired, g.Genre as FirstGenre, st.ShowType, s.Length, s.NumberRating
            FROM			Shows as s
            JOIN				Ratings as r
                ON			s.ShowRatingId = r.Id
            JOIN				Genres as g
                ON			s.FirstGenreId = g.Id
            JOIN				ShowTypes as st
                ON			s.ShowTypeId = st.Id;
            '''
    return query

############### HELPER FUNCTIONS ###############
def print_result_options(item_count):
    print()
    print(f'Congrats! You now have access to the top {item_count} rated movies and shows!')
    print('Below are the different ways you can look at your results.')
    print()
    print(f'[1] Average Rating (out of 10) by First Movie Genre')
    print(f'[2] Average Rating (out of 10) by Film Rating')
    print(f'[3] Movies Data (All Movie Results)')
    print(f'[4] Average Rating (out of 10) by Show Type')
    print(f'[5] Average Rating (out of 10) by First Show Genre')
    print(f'[6] Average Rating (out of 10) by Show Rating')
    print(f'[7] Shows Data (All Show Results)')
    print()

############### BASE CLASS AND FUNCTIONS ###############
class TopMovieShow:
    '''Top Rated Movie

    Instance Attributes
    -------------------
    title: string
        the title of a top rated movie
    release_year: string
        the release year of a movie
    rating: string
        the rating of a movie (e.g. 'PG', 'R')
    genre: string
        the genre of a movie (e.g. 'Action', 'Horror')
    country: string
        the country alpha-3 code (e.g. 'USA', 'GER')
    length: string
        the total length (time) of a movie
    num_rating: string
        the overall rating of a movie (out of 10)
    '''
    def __init__(self, title, release_year, rating, genre, country, length, num_rating):
        self.title = title
        self.release_year = release_year
        self.rating = rating
        self.genre = genre
        self.country = country
        self.length = length
        self.num_rating = num_rating

    def info(self):
        return (f"{self.title} Rated: {self.rating} ({self.country}, {self.release_year}): {self.genre} {self.length} {self.num_rating} out of 10.")

class TopRatedShow:
    '''Top Rated Show

    Instance Attributes
    -------------------
    title: string
        the title of a top rated TV show
    air_years: string
        the number of years of a TV show aired site
    rating: string
        the rating of a TV show (e.g. 'TV-G')
    genre: string
        the genre of a TV show (e.g. 'Documentary', 'Crime')
    show_type: string
        the type of a TV show (e.g. 'TV Mini Series', 'TV Series')
    length: string
        the total length (time) of an entire TV series or individual episodes
    num_rating: string
        the overall rating of a TV show (out of 10)
    '''
    def __init__(self, title, air_years, rating, genre, show_type, length, num_rating):
        self.title = title
        self.air_years = air_years
        self.rating = rating
        self.genre = genre
        self.show_type = show_type
        self.length = length
        self.num_rating = num_rating

    def info(self):
        return (f"{self.title} Rated: {self.rating} ({self.air_years}): Genre(s) - {self.genre} {self.show_type} {self.length} {self.num_rating} out of 10.")

def get_top_movie_info(top_media_url):
    '''Make an instances from a top rated movies's URL.

    Parameters
    ----------
    top_media_url: string
        The URL for a top movie page on imdb.com

    Returns
    -------
    instance
        a top rated movie instance
    '''
    CACHE_DICT = load_cache()
    url_text = make_url_request_using_cache(top_media_url, CACHE_DICT)
    soup = BeautifulSoup(url_text, 'html.parser')
    movie_info = soup.find(class_='title_wrapper')

    movie_details_list = []
    movie_details = movie_info.find_all('a')
    for detail in movie_details:
        if detail == None:
            movie_details_list.append('None')
        else:
            movie_details_list.append(detail.text.strip())

    if movie_info.find('h1') == None:
        title = 'No Title'
        release_year = 'No Release Year'
    else:
        title = movie_info.text.split('(')[0].strip()
        release_year = movie_info.text.split('(')[1][0:4].strip()
    rating = soup.find(class_='subtext')
    if rating == None or 'Not' in rating.text:
        rating = 'Not Rated'
    elif rating.text.split()[0] in RATINGS_LIST.values():
        rating = rating.text.split()[0].strip()
    else:
        rating = 'Not Rated'
    genre = movie_details_list[1:-1]
    if genre == 'None':
        genre = 'No Genre'
    country = movie_details_list[-1]
    if country == 'None':
        country = 'No Country'
    else:
        country = country.split('(')[1].strip()[:-1]
    length = soup.find('time')
    if length == None:
        length = 'No Length'
    else:
        length = length.text.strip()
    num_rating = soup.find(class_='ratingValue')
    if num_rating == None:
        num_rating = 'No Rating'
    else:
        num_rating = num_rating.text.strip().split('/')[0]

    top_movie = TopMovieShow(title, release_year, rating, genre, country, length, num_rating)
    return top_movie

def get_top_show_info(top_media_url):
    '''Make an instances from a top rated show's URL.

    Parameters
    ----------
    top_media_url: string
        The URL for a top show page on imdb.com

    Returns
    -------
    instance
        a top rated show instance
    '''
    CACHE_DICT = load_cache()
    show_details_list = []
    url_text = make_url_request_using_cache(top_media_url, CACHE_DICT)
    soup = BeautifulSoup(url_text, 'html.parser')
    show_info = soup.find(class_='title_wrapper')

    show_details = show_info.find_all('a')
    for detail in show_details:
        if detail == None:
            show_details_list.append('None')
        else:
            show_details_list.append(detail.text.strip())

    title = show_info.find('h1')
    if title == None:
        title = 'No Title'
    else:
        title = title.text.strip()
    rating = soup.find(class_='subtext')
    if rating == None or 'TV-' not in rating.text.split()[0]:
        rating = 'Not Rated'
    else:
        rating = rating.text.split()[0].strip()
    air_years = show_details_list[-1]
    if air_years == 'None':
        air_years = 'No Air Year(s)'
    else:
        air_years = air_years.split('(')[1][:-1]
    genre = show_details_list[:-1]
    if 'None' in genre:
        genre = 'No Genre'
    show_type = show_details_list[-1]
    if show_type == 'None':
        show_type = 'No Type'
    else:
        show_type = show_type.split('(')[0].strip()
    length = soup.find('time')
    if length == None:
        length = 'No Length'
    else:
        length = length.text.strip()
    num_rating = soup.find(class_='ratingValue')
    if num_rating == None:
        num_rating = 'No Rating'
    else:
        num_rating = num_rating.text.strip().split('/')[0]

    top_show = TopRatedShow(title, air_years, rating, genre, show_type, length, num_rating)
    return top_show

def get_sites_for_movies_or_shows(top_media_type, top_url, item_count):
    '''Make a list of movie/tv show instances from a movie/tv show URL.

    Parameters
    ----------
    top_media_type: string
        The media type to determine when to get movies or shows information
    top_url: string
        The URL for a movie/tv show page on imdb.com
    item_count: int
        The number of instances of a movie or show to be created

    Returns
    -------
    list
        a list of movies/tv show instances
    '''
    top_movies_list = []
    top_shows_list = []
    CACHE_DICT = load_cache()
    url_text = make_url_request_using_cache(top_url, CACHE_DICT)
    soup = BeautifulSoup(url_text, 'html.parser')

    top_list = soup.find(class_='lister-list')
    tops = top_list.find_all('td', class_='titleColumn')

    for top in tops:
        top_media_url = top.find('a')['href']
        top_media_url = BASE_URL + top_media_url
        if len(top_movies_list) == 10 or len(top_shows_list) == 10:
            break
        else:
            if top_media_type == 'movies':
                    top_instance = get_top_movie_info(top_media_url)
                    top_movies_list.append(top_instance)
            else:
                top_instance = get_top_show_info(top_media_url)
                top_shows_list.append(top_instance)
    if top_media_type == 'movies':
        return top_movies_list
    else:
        return top_shows_list

if __name__ == "__main__":
    print('Welcome! We are here to help you find information on the top 250 rated movies and tv shows!')
    while True:
        item_count = input('How many items per media type would you like info on you want to see (min 50, max 250)? Or type "exit" to quit: ')
        print()
        if item_count.lower() == 'exit':
            print('Goodbye!')
            exit()
        if item_count.isdigit():
            if int(item_count) < 50 or int(item_count) > 250:
                print(item_count)
                print('[Error] Incorrect input!')
                continue
            else:
                create_database()
                for top_media_type, top_media_url in TOP_RATED_DICT.items():
                    print(f'Getting Top Rated {top_media_type.capitalize()}!')
                    top_url = top_media_url
                    top_rated_list = get_sites_for_movies_or_shows(top_media_type.lower(), top_url, int(item_count))
                    top_rated_dict = {}
                    count = 0
                    for top_item in top_rated_list:
                        count += 1
                        top_rated_dict[count] = top_item.info()
                        populate_database(top_media_type.lower(), top_item)
                while True:
                    print_result_options(item_count)
                    query_num = input('Which option would you like to choose? Or type "exit" to quit: ')
                    print()
                    if query_num.lower() == 'exit':
                        print('This is the end of the program. Goodbye!')
                        exit()
                    if query_num.isdigit():
                        if int(query_num) < 1 or int(query_num) > 7:
                            print('[Error] Incorrect input!')
                            continue
                        else:
                            result = get_query(int(query_num))
                            print_query_results(result)
                            # continue
                            # print('This is the end of the program. Goodbye!')
                            # exit()
                    else:
                        print('[Error] Incorrect input!')
                        continue
        else:
            print(item_count)
            print('[Error] Incorrect input!')
            continue
        print('This is the end of the program. Goodbye!')
        exit()
