# This gathered info about a pokemon's stats, type, and name
# from Bulbapedia and assembled it in pokemondata.txt.
#
# It takes the stats from the first table after the "Stats"
# header on a Pokemon's page, which means nuances like
# Deoxys' formes or mega-evolutions aren't included. Also,
# if a pokemon's base stats were changed, this took whichever
# stats were listed in the first table.

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common import keys
import pandas as pd
import re
import time


def getPokeHTML(pokemon):
    thepokemontolookfor = pokemon
    bulbapedia = f'https://bulbapedia.bulbagarden.net/wiki/{thepokemontolookfor}'
    thehtml = requests.get(bulbapedia)
    return thehtml


pokemonnamestest = ['Doublade', 'Aegislash']
pokemonnames = pd.read_csv(filepath_or_buffer='pokemonnames.txt', delimiter='\n', header=None)

start = time.process_time()
for i in pokemonnames.iterrows():
# for j in pokemonnamestest:
    j = i[1][0]
    pokehtml = getPokeHTML(j)
    soup = BeautifulSoup(pokehtml.content, 'html.parser')

    # Time to get the stats!
    placewithbasestats = ''
    if soup.find('span', id="Base_stats") is None:
        placewithbasestats = soup.find('span', id="Stats").parent.find_next_sibling('table')
    if soup.find('span', id="Base_stats") is not None:
        placewithbasestats = soup.find('span', id="Base_stats").parent.find_next_sibling('table')
    HP = placewithbasestats.find_all('th')[4].find_all('div')[1].text
    Attack = placewithbasestats.find_all('th')[5].find_all('div')[1].text
    Defense = placewithbasestats.find_all('th')[6].find_all('div')[1].text
    SpAttack = placewithbasestats.find_all('th')[7].find_all('div')[1].text
    SpDefense = placewithbasestats.find_all('th')[8].find_all('div')[1].text
    Speed = placewithbasestats.find_all('th')[9].find_all('div')[1].text
    print(f'-----{j}-----')
    print(
        f"Health: {HP}, Attack: {Attack}, Defense: {Defense}, SpAttack: {SpAttack}, SpDefense: {SpDefense}, Speed: {Speed}")

    # Time to get the types!
    placewithtypes = soup.find('div', id='mw-content-text') \
        .find_all('table')[4] \
        .find_all('tr')[8] \
        .find('td') \
        .find('td') \
        .find_all('td')
    print(f'Types: {len(placewithtypes)}')
    type1 = placewithtypes[0].find('b').text
    type2 = ''
    if len(placewithtypes) == 2:
        type2 = placewithtypes[1].find('b').text
    print(f'Type 1: {type1}, Type 2: {type2}\n')
    with open('data/pokemondata.txt', 'a', encoding='utf-8') as file:
        file.write(f'{j},{HP},{Attack},{Defense},{SpAttack},{SpDefense},{Speed},{type1},{type2}\n')
end = time.process_time()
elapsed = (end - start) / 60
print(f'Total time: {elapsed} minutes.')
