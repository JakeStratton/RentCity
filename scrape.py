from bs4 import BeautifulSoup
import pandas as pd 
import ast
from datetime import datetime
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import sys
import numpy as np
import regex as re


# function to get rental info
def get_rental_info(urls):
     '''creates a pandas dataframe of rental info using beautiful soup to scrape
     from streeteasy.com

     Parameters
     ----------
     url: the URL of the rental page to scrape

     Returns
     -------
     rental_single_df: the dataframe of apartment info'''

     # use selenium with chromedriver to get dynamic JS page.  requests library won't wait for JS.
     chromedriver = "~/Downloads/chromedriver" # path to the chromedriver executable
     chromedriver = os.path.expanduser(chromedriver)
     print('chromedriver path: {}'.format(chromedriver))
     sys.path.append(chromedriver)
     driver = webdriver.Chrome(chromedriver)
     #rentals_info = []


     # open log file
     scrape_log = open('scrape_log.txt','a')


     for idx, url in enumerate(urls):
          try:
               driver.get(url) #get the page
               time.sleep(2)
               soup = BeautifulSoup(driver.page_source, 'html.parser') #make the soup

               result = str(datetime.now()) + ':::' + str(idx) + ':::' + str(url)
               scrape_log.write('\n%s' % (result))

               # get rental info and add raw data to list
               rental_info_raw = soup.find_all(defer=True) # gets rental info data by finding any tag that has a defer attribute
               rental_info_string = str(rental_info_raw[0])  # makes a string out of the relevant info
               rental_info = rental_info_string.split('\n') #creates a list of the raw info

               #clean data
               rental_info = [i for i in rental_info if i.startswith('googletag')] 
               rental_info = [x.replace('googletag.pubads().setTargeting(\'', '"') for x in rental_info] 
               rental_info = [x.replace('\',', '":') for x in rental_info]
               rental_info = [x.replace('");', '"') for x in rental_info]
               rental_info = [x.replace(');', '') for x in rental_info]
               rental_info = ','.join(rental_info) 
               rental_info = '{' + rental_info + '}'
               rentals_info = [rental_info]
               #rentals_info = rentals_info + rental_info#

          except Exception as e:
               result = str(idx) + str(datetime.now()) + ':::' + str(e) + ':::' + str(url)
               scrape_log.write('\nEXCEPTION: %s' % (result))
               print('EXCEPTION: ' + str(idx) + str(e) + result)

     # convert game_info to a list of dictionaries
     rentals_info_dicts = []
     for i in rentals_info:
          rentals_info_dicts.append(ast.literal_eval(i))

     #create df
     rentals_info_df = pd.DataFrame(rentals_info_dicts)
     
     # save csv file from dataframe
     rentals_info_df.to_csv('rentals_info.csv')

     return rentals_info_df


def get_rental_urls(start_page, end_page):
     base_url = 'https://streeteasy.com/for-rent/nyc?page='

     # use selenium with chromedriver to get dynamic JS page.  requests library won't wait for JS.
     chromedriver = "~/Downloads/chromedriver" # path to the chromedriver executable
     chromedriver = os.path.expanduser(chromedriver)
     print('chromedriver path: {}'.format(chromedriver))
     sys.path.append(chromedriver)
     driver = webdriver.Chrome(chromedriver)

     # open log file
     scrape_log = open('url_scrape_log.txt','a')

     urls = []
     for i in range(start_page, end_page):
          try:
               driver.get(base_url + str(i))
               time.sleep(2)
               listings = driver.find_elements_by_css_selector('article.item')
               for listing in listings:
                    item = listing.find_element_by_css_selector('.details-title a').get_attribute('href')
                    urls.append(item)
          except Exception as e:
               result = str(datetime.now()) + ':::' + str(e) + ':::' + str(i)
               scrape_log.write('\nEXCEPTION: %s' % (result))
               print('EXCEPTION: ' + str(e) + result)

     #create df
     urls_df = pd.DataFrame(urls)
     
     # save csv file from dataframe
     urls_df.to_csv('urls.csv')

     return urls





'''
          
if __name__ == '__main__':
    None

    '''