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
    '''
    def __init__(self, show_title, show_air_years, show_tv_rating, show_genre, show_type, show_length, show_num_rating):
        if show_title == None:
            self.show_title = 'No Title'
        else:
            self.show_title = show_title
        if show_air_years == None:
            self.show_air_years = 'No Year(s)'
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
            self.show_num_rating = 'No Fan Rating'
        else:
            self.show_num_rating = show_num_rating

    def info(self):
        return (f"{self.show_title} ({self.show_air_years}): Is a {self.show_type} rated {self.show_tv_rating}, Genre(s) - {self.show_genre}, {self.show_length} long with a {self.show_num_rating} out of 10.")

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
            top_rated_dict[top_category.text.lower().strip().replace(' ', '_')] = BASE_URL+top_url
    return top_rated_dict

def get_top_show_info(top_show_url):
    '''Make an instances from a top rated show's URL.

    Parameters
    ----------
    site_url: string
        The URL for a top show page on imdb.com

    Returns
    -------
    instance
        a top rated show instance
    '''
    CACHE_DICT = load_cache()
    url_text = make_url_request_using_cache(top_show_url, CACHE_DICT)
    soup = BeautifulSoup(url_text, 'html.parser')
    show_info = soup.find(class_='title_wrapper')
    # print(show_info)

    show_details_list = []
    show_details = show_info.find_all('a')
    for detail in show_details:
        show_details_list.append(detail.text.strip())
        # print(detail.text.strip())
    # print(show_details_list)

    show_title = show_info.find('h1').text.strip()
    show_air_years = show_details_list[-1].split('(')[1][:-1]
    show_tv_rating = soup.find(class_='subtext').text.split()[0].strip()
    show_genre = show_details_list[:-1]
    show_type = show_details_list[-1].split('(')[0].strip()
    show_length = soup.find('time').text.strip()
    show_num_rating = soup.find(class_='ratingValue').text.strip().split('/')[0]
    # print(show_title)
    # print(show_air_years)
    # print(show_rating)
    # print(show_genre)
    # print(show_genre_type)
    # print(show_length)

    top_show = TopRatedShow(show_title, show_air_years, show_tv_rating, show_genre, show_type, show_length, show_num_rating)
    return top_show

if __name__ == "__main__":
    # top_movie_url = 'https://www.imdb.com/title/tt0111161/?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=e31d89dd-322d-4646-8962-327b42fe94b1&pf_rd_r=EW1HMTNTT51KCVXWB0PF&pf_rd_s=center-1&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_tt_1'
    # top_show = get_top_show_info(top_show_url)
    top_show_url = 'https://www.imdb.com/title/tt0903747/?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=12230b0e-0e00-43ed-9e59-8d5353703cce&pf_rd_r=1YHTMF2JWF8BMF9VG8WH&pf_rd_s=center-1&pf_rd_t=15506&pf_rd_i=toptv&ref_=chttvtp_tt_4'
    # top_show = get_top_show_info(top_show_url)
    # print(top_show.info())

    CACHE_DICT = load_cache()
    # url_text = make_url_request_using_cache(top_movie_url, CACHE_DICT)
    url_text = make_url_request_using_cache(top_show_url, CACHE_DICT)
    soup = BeautifulSoup(url_text, 'html.parser')
    show_info = soup.find(class_='title_wrapper')
    # print(show_info)

    show_details_list = []
    show_details = show_info.find_all('a')
    for detail in show_details:
        show_details_list.append(detail.text.strip())
        # print(detail.text.strip())
    # print(show_details_list)
    # print()

    show_title = show_info.find('h1').text.strip()
    show_air_years = show_details_list[-1].split('(')[1][:-1]
    show_tv_rating = soup.find(class_='subtext').text.split()[0].strip()
    show_genre = show_details_list[:-1]
    show_type = show_details_list[-1].split('(')[0].strip()
    show_length = soup.find('time').text.strip()
    show_num_rating = soup.find(class_='ratingValue').text.strip().split('/')[0]
    # print(show_fan_rating)
    # print(show_title)
    # print(show_air_years)
    # print(show_rating)
    # print(show_genre)
    # print(show_type)
    # print(show_length)

    top_show = TopRatedShow(show_title, show_air_years, show_tv_rating, show_genre, show_type, show_length, show_num_rating)
    # print(top_show.info())













    # state_dict = build_state_url_dict()
    # while True:
    #     state = input('Enter a state name (e.g. Michigan, michigan) or "exit": ')
    #     if state.isalpha:
    #         if state.lower() == 'exit':
    #             exit()
    #         if state.lower() not in state_dict.keys():
    #             print('[Error] Enter a proper state name!')
    #         else:
    #             state_url = state_dict[state.lower()]
    #             site_list = get_sites_for_state(state_url)
    #             print_header_for_state_search(state, state_dict)
    #             site_dict = {}
    #             count = 0
    #             for site in site_list:
    #                 count += 1
    #                 site_dict[count] = site.info()
    #                 print(f"[{count}] {site.info()}")
    #     else:
    #         print('[Error] Enter a proper state name!')
