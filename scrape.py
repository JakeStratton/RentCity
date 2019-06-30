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

url = 'https://streeteasy.com/building/parc-east/23h'

# function to get rental info
def get_rental_info(url):
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

     driver.get(url) #get the page
     time.sleep(2)
     soup = BeautifulSoup(driver.page_source, 'html.parser') #make the soup

     # get rental info and add raw data to list
     rental_info_raw = soup.find_all(defer=True) # gets rental info data by finding any tag that has a defer attribute
     rental_info_string = str(rental_info_raw[0])  # makes a string out of the relevant info
     rental_info = rental_info_string.split('\n') #creates a list of the raw info

     #clean data
     rental_info = [i for i in rental_info if i.startswith('googletag')] 
     rental_info = [x.replace('googletag.pubads().setTargeting(\'', '"') for x in rental_info] 
     rental_info = [x.replace('\',', '":') for x in rental_info]
     rental_info = [x.replace('");', '"') for x in rental_info]
     rental_info = ','.join(rental_info) 
     rental_info = '{' + rental_info + '}'
     rental_info = [rental_info]

     return rental_info


def get_rental_urls(start_page, end_page):
     base_url = 'https://streeteasy.com/for-rent/nyc?page='

     # use selenium with chromedriver to get dynamic JS page.  requests library won't wait for JS.
     chromedriver = "~/Downloads/chromedriver" # path to the chromedriver executable
     chromedriver = os.path.expanduser(chromedriver)
     print('chromedriver path: {}'.format(chromedriver))
     sys.path.append(chromedriver)
     driver = webdriver.Chrome(chromedriver)

     urls = []
     for i in range(start_page, end_page):
          driver.get(base_url + str(i))
          time.sleep(2)
          listings = driver.find_elements_by_css_selector('article.item')
          for listing in listings:
               item = listing.find_element_by_css_selector('.details-title a').get_attribute('href')
               urls.append(item)

     return urls


          
