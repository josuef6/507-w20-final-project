#########################################
##### Name:      Josue Figueroa     #####
##### Uniqname:       josuef        #####
##### Course: SI 507 Winter 2020    #####
##### Project: (Final) Project 4    #####
#########################################

import unittest
import proj4 as imdb

class Test_Get_Movie_Info(unittest.TestCase):
    def setUp(self):
        self.site_movie = imdb.get_top_movie_info('https://www.imdb.com/title/tt0068646/?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=e31d89dd-322d-4646-8962-327b42fe94b1&pf_rd_r=4Y22SSMQ0W9RRR10GDRB&pf_rd_s=center-1&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_tt_2')

    def test_1_1_title(self):
        self.assertEqual(self.site_movie.title, 'The Godfather')

    def test_1_2_release_year(self):
        self.assertEqual(self.site_movie.release_year, '1972')

    def test_1_3_rating(self):
        self.assertEqual(self.site_movie.rating, 'R')

    def test_1_4_genre(self):
        self.assertEqual(self.site_movie.genre, ['Crime', 'Drama'])

    def test_1_5_country(self):
        self.assertEqual(self.site_movie.country, 'USA')

    def test_1_6_length(self):
        self.assertEqual(self.site_movie.length, '2h 55min')

    def test_1_7_num_rating(self):
        self.assertEqual(self.site_movie.num_rating, '9.2')

    def test_1_8_phone(self):
        self.assertEqual(self.site_movie.info(), "The Godfather Rated: R (USA, 1972): ['Crime', 'Drama'] 2h 55min 9.2 out of 10.")

class Test_Get_Show_Info(unittest.TestCase):
    def setUp(self):
        self.site_show = imdb.get_top_show_info('https://www.imdb.com/title/tt5491994/?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=12230b0e-0e00-43ed-9e59-8d5353703cce&pf_rd_r=EHPG0GRTKBYBN79TKRR2&pf_rd_s=center-1&pf_rd_t=15506&pf_rd_i=toptv&ref_=chttvtp_tt_1')

    def test_2_1_title(self):
        self.assertEqual(self.site_show.title, 'Planet Earth II')
        self.assertEqual(self.site_show.air_years, '2016')
        self.assertEqual(self.site_show.rating, 'TV-G')
        self.assertEqual(self.site_show.genre, ['Documentary'])
        self.assertEqual(self.site_show.show_type, 'TV Mini-Series')
        self.assertEqual(self.site_show.length, '4h 58min')
        self.assertEqual(self.site_show.num_rating, '9.5')
        self.assertEqual(self.site_show.info(), "Planet Earth II Rated: TV-G (2016): Genre(s) - ['Documentary'] TV Mini-Series 4h 58min 9.5 out of 10.")

class Test_Get_Sites_For_Movies_Or_Shows(unittest.TestCase):
    def setUp(self):
        self.movie_list = imdb.get_sites_for_movies_or_shows('movies', 'https://www.imdb.com/chart/top/?ref_=nv_mv_250', 10)
        self.show_list = imdb.get_sites_for_movies_or_shows('shows', 'https://www.imdb.com/chart/toptv/?ref_=nv_tvv_250', 10)

    def test_3_1_return_type(self):
        self.assertEqual(type(self.movie_list), list)
        self.assertEqual(type(self.show_list), list)

    def test_3_2_length(self):
        self.assertEqual(len(self.movie_list), 10)
        self.assertEqual(len(self.show_list), 10)

    def test_3_3_contents(self):
        self.assertEqual(self.movie_list[9].title, 'The Lord of the Rings: The Fellowship of the Ring')
        self.assertEqual(self.movie_list[9].release_year, '2001')
        self.assertEqual(self.movie_list[9].rating, 'PG-13')
        self.assertEqual(self.movie_list[9].genre, ['Action', 'Adventure', 'Drama'])
        self.assertEqual(self.movie_list[9].country, 'USA')
        self.assertEqual(self.movie_list[9].length, '2h 58min')
        self.assertEqual(self.movie_list[9].num_rating, '8.8')
        self.assertEqual(self.movie_list[9].info(), "The Lord of the Rings: The Fellowship of the Ring Rated: PG-13 (USA, 2001): ['Action', 'Adventure', 'Drama'] 2h 58min 8.8 out of 10.")

        self.assertEqual(self.show_list[8].title, 'Game of Thrones')
        self.assertEqual(self.show_list[8].air_years, '2011–2019')
        self.assertEqual(self.show_list[8].rating, 'TV-MA')
        self.assertEqual(self.show_list[8].genre, ['Action', 'Adventure', 'Drama'])
        self.assertEqual(self.show_list[8].show_type, 'TV Series')
        self.assertEqual(self.show_list[8].length, '57min')
        self.assertEqual(self.show_list[8].num_rating, '9.3')
        self.assertEqual(self.show_list[8].info(), "Game of Thrones Rated: TV-MA (2011–2019): Genre(s) - ['Action', 'Adventure', 'Drama'] TV Series 57min 9.3 out of 10.")

if __name__ == '__main__':
    unittest.main()
