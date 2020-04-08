#########################################
##### Name:      Josue Figueroa     #####
##### Uniqname:       josuef        #####
#########################################

from bs4 import BeautifulSoup
import requests
import json
import time

BASE_URL = "https://www.imdb.com"
CACHE_FILE_NAME = 'cache.json'
CACHE_DICT = {}

headers = {
    'User-Agent': 'UMSI 507 Course Project - Python Scraping',
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
    cache_dict: dict
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
        print("Using cache")
        return cache[url]
    else:
        print("Fetching")
        time.sleep(1)
        response = requests.get(url, headers=headers)
        cache[url] = response.text
        save_cache(cache)
        return cache[url]

############### BASE CLASS AND FUNCTIONS ###############
class TopMovieShow:
    '''Top Rated Movie

    Instance Attributes
    -------------------
    movie_title: string
        the title of a top rated movie
    movie_release_year: string
        the release year of a movie
    movie_rating: string
        the rating of a movie (e.g. 'PG', 'R')
    movie_genre: string
        the genre of a movie (e.g. 'Action', 'Horror')
    movie_country: string
        the country alpha-3 code (e.g. 'USA', 'GER')
    movie_length: string
        the total length (time) of a movie
    movie_num_rating: string
        the overall rating of a movie (out of 10)
    '''

    def __init__(self, movie_title, movie_release_year, movie_rating, movie_genre, movie_country, movie_length, movie_num_rating):
        if movie_title == None:
            self.movie_title = 'No Title'
        else:
            self.movie_title = movie_title
        if movie_release_year == None:
            self.movie_release_year = 'No Release Year'
        else:
            self.movie_release_year = movie_release_year
        if movie_rating == None:
            self.movie_rating = 'No Rating'
        else:
            self.movie_rating = movie_rating
        if movie_genre == None:
            self.movie_genre = 'No Genre'
        else:
            self.movie_genre = movie_genre
        if movie_country == None:
            self.movie_country = 'No Country'
        else:
            self.movie_country = movie_country
        if movie_length == None:
            self.movie_length = 'No Length'
        else:
            self.movie_length = movie_length
        if movie_num_rating == None:
            self.movie_num_rating = 'No Num Rating'
        else:
            self.movie_num_rating = movie_num_rating

    def info(self):
        return (f"{self.movie_title} ({self.movie_country}, {self.movie_release_year}): Is a {self.movie_genre} film rated {self.movie_rating}, {self.movie_length} long with a {self.movie_num_rating} rating out of 10.")


class TopRatedShow:
    '''Top Rated Show

    Instance Attributes
    -------------------
    show_title: string
        the title of a top rated TV show
    show_air_years: string
        the number of years of a TV show aired site
    show_rating: string
        the rating of a TV show (e.g. 'TV-G')
    show_genre: string
        the genre of a TV show (e.g. 'Documentary', 'Crime')
    show_type: string
        the type of a TV show (e.g. 'TV Mini Series', 'TV Series')
    show_length: string
        the total length (time) of an entire TV series or individual episodes
    show_num_rating: string
        the overall rating of a TV show (out of 10)
    '''
    def __init__(self, show_title, show_air_years, show_tv_rating, show_genre, show_type, show_length, show_num_rating):
        if show_title == None:
            self.show_title = 'No Title'
        else:
            self.show_title = show_title
        if show_air_years == None:
            self.show_air_years = 'No Air Year(s)'
        else:
            self.show_air_years = show_air_years
        if show_tv_rating == None:
            self.show_tv_rating = 'No Rating'
        else:
            self.show_tv_rating = show_tv_rating
        if show_genre == None:
            self.show_genre = 'No Genre'
        else:
            self.show_genre = show_genre
        if show_type == None:
            self.show_type = 'No Show Type'
        else:
            self.show_type = show_type
        if show_length == None:
            self.show_length = 'No Length'
        else:
            self.show_length = show_length
        if show_num_rating == None:
            self.show_num_rating = 'No Num Rating'
        else:
            self.show_num_rating = show_num_rating

    def info(self):
        return (f"{self.show_title} ({self.show_air_years}): Is a {self.show_type} rated {self.show_tv_rating}, Genre(s) - {self.show_genre}, {self.show_length} long with a {self.show_num_rating} rating out of 10.")

def build_top_rated_url_dict():
    ''' Make a dictionary that maps state name to state page url from "https://www.imdb.com"

    Parameters
    ----------
    None

    Returns
    -------
    dict
        key is a category name and value is the url
        e.g. {'top rated movies': 'https://www.imdb.com/chart/top/?ref_=nv_mv_250', ...}
    '''
    top_rated_dict = {}
    CACHE_DICT = load_cache()
    url_text = make_url_request_using_cache(BASE_URL, CACHE_DICT)
    soup = BeautifulSoup(url_text, 'html.parser')
    searching_list = soup.find_all(class_='ipc-list _1BHmFYrYdlAF0gND-D42MO ipc-list--baseAlt', recursive=True)
    for search in searching_list:
        top = search.find(class_='ipc-list__item nav-link sc-jTzLTM fjLstn ipc-list__item--indent-one')
        if top.text == 'Top Rated Movies' or top.text == 'Top Rated Shows':
            top_category = top
            top_url = top["href"]
            top_rated_dict[top_category.text.lower().strip().split()[-1]] = BASE_URL+top_url
    return top_rated_dict

def get_top_movie_info(top_movie_url):
    '''Make an instances from a top rated movies's URL.

    Parameters
    ----------
    top_movie_url: string
        The URL for a top movie page on imdb.com

    Returns
    -------
    instance
        a top rated movie instance
    '''
    CACHE_DICT = load_cache()
    url_text = make_url_request_using_cache(top_movie_url, CACHE_DICT)
    soup = BeautifulSoup(url_text, 'html.parser')
    movie_info = soup.find(class_='title_wrapper')

    movie_details_list = []
    movie_details = movie_info.find_all('a')
    for detail in movie_details:
        movie_details_list.append(detail.text.strip())

    movie_title = movie_info.find('h1').text.split('(')[0].strip()
    movie_release_year = movie_info.find('h1').text.split('(')[1].strip()[:-1]
    movie_rating = soup.find(class_='subtext').text.split()[0].strip()
    movie_genre = movie_details_list[1]
    movie_country = movie_details_list[-1].split('(')[1].strip()[:-1]
    movie_length = soup.find('time')
    if movie_length == None:
        movie_length = 'No Length'
    else:
        movie_length = movie_length.text.strip()
    movie_num_rating = soup.find(class_='ratingValue').text.strip().split('/')[0]

    top_movie = TopMovieShow(movie_title, movie_release_year, movie_rating, movie_genre, movie_country, movie_length, movie_num_rating)
    return top_movie

def get_top_show_info(top_show_url):
    '''Make an instances from a top rated show's URL.

    Parameters
    ----------
    top_show_url: string
        The URL for a top show page on imdb.com

    Returns
    -------
    instance
        a top rated show instance
    '''
    CACHE_DICT = load_cache()
    show_details_list = []
    url_text = make_url_request_using_cache(top_show_url, CACHE_DICT)
    soup = BeautifulSoup(url_text, 'html.parser')
    show_info = soup.find(class_='title_wrapper')

    show_details = show_info.find_all('a')
    for detail in show_details:
        show_details_list.append(detail.text.strip())

    show_title = show_info.find('h1').text.strip()
    show_air_years = show_details_list[-1].split('(')[1][:-1]
    show_tv_rating = soup.find(class_='subtext').text.split()[0].strip()
    show_genre = show_details_list[:-1]
    show_type = show_details_list[-1].split('(')[0].strip()
    show_length = soup.find('time')
    if show_length == None:
        show_length = 'No Length'
    else:
        show_length = show_length.text.strip()
    show_num_rating = soup.find(class_='ratingValue').text.strip().split('/')[0]

    top_show = TopRatedShow(show_title, show_air_years, show_tv_rating, show_genre, show_type, show_length, show_num_rating)
    return top_show

def get_sites_for_movies_or_shows(top_media_type, top_url):
    '''Make a list of movie/tv show instances from a movie/tv show URL.

    Parameters
    ----------
    top_url: string
        The URL for a movie/tv show page on imdb.com

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
        top_url = top.find('a')['href']
        top_full_url = BASE_URL + top_url
        # if len(top_movies_list) == 50 or len(top_shows_list) == 50:
        #     break
        # else:
        if top_media_type == 'movies':
            top_instance = get_top_movie_info(top_full_url)
            top_movies_list.append(top_instance)
        else:
            top_instance = get_top_show_info(top_full_url)
            top_shows_list.append(top_instance)
    if top_media_type == 'movies':
        return top_movies_list
    else:
        return top_shows_list

if __name__ == "__main__":
    top_media_type = input('Please indicate whether you want info for top rated movies or tv shows (e.g. Movies, movies, Shows, show) or "exit": ')
    while top_media_type.lower() != 'exit':
        top_rated_dict = build_top_rated_url_dict()
        # top_media_type = input('Please indicate whether you want info for top rated movies or tv shows (e.g. Movies, movies, Shows, show) or "exit": ')
        if top_media_type.isalpha:
            if top_media_type.lower() == 'exit':
                exit()
            if top_media_type.lower() not in top_rated_dict.keys():
                print('[Error] Incorrect input!')
            else:
                top_url = top_rated_dict[top_media_type.lower()]
                top_rated_list = get_sites_for_movies_or_shows(top_media_type.lower(), top_url)
                # print_header_for_state_search(top_media_type, top_media_type)
                top_rated_dict = {}
                count = 0
                for top_item in top_rated_list:
                    count += 1
                    top_rated_dict[count] = top_item.info()
                    print(f"[{count}] {top_item.info()}")
                print()
        else:
            print('[Error] Incorrect input!')
        print('This is the end of the program. Goodbye!')
        exit()
