import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import sys


def selenium_chrome():
    # use selenium with chromedriver to get dynamic JS page.  requests library won't wait for JS.
    chromedriver = "~/Downloads/chromedriver" # path to the chromedriver executable
    chromedriver = os.path.expanduser(chromedriver)
    print('chromedriver path: {}'.format(chromedriver))
    sys.path.append(chromedriver)
    driver = webdriver.Chrome(chromedriver)
    return None