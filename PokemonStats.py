# This will gather info about a pokemon's stats, type, and name
# from either Serebii or Bulbapedia, whichever is nicer.

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common import keys

print('Fingers crossed we can just do requests.get() for all this!')
