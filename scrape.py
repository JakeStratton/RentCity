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
    soup = BeautifulSoup(driver.page_source, 'html.parser') #make the soup

    # get rental info
    rental_info = []
    rental_info_raw = soup.find_all(defer=True) # gets rental info data by class
    '''for data in rental_info_raw.find_all('div'):  # for loop to go through rental info
        rental_info.append(data.get_text()) # add rental info to list'''

    return rental_info

