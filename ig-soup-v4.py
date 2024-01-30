#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from pprint import pprint
import json

# For decode Unicode characters
import unidecode
# Search regex
import re
import time




# SRAPING XCLOUD LIST GAMES OK
##################################




# Headless Chrome and Selenium 


from selenium import webdriver
path = './drivers/geckodriver.exe'
driver = webdriver.Firefox(executable_path = path)

# ALGO
time.sleep(20)
my_data = []

def get_items(items):
    for itemGame in items:
        # get title game word
        title = itemGame.select('span.title')[0].get_text()

        print(title)

        # remove copyright in title
        title = title.replace('®','').replace('™','').replace(':','')
        
        # Remove word between parenthes in title after create store
        # title = re.sub(r"\([^()]*\)","", title)

        # remove last space in title - lstrip for first space
        title = title.rstrip()
        title = unidecode.unidecode(title)

        url = itemGame.select('a.cover')[0]["href"]

        print(url)

        store = re.search("game.*", url)[0]
        store = store.replace('game-','').replace('/','')

        print(store)

        price = '0'
        if not(len(itemGame.select('div.price')) == 0) :
            price = itemGame.select('div.price')[0].get_text()
            price = price[:-1]

        print(price)

        discount = '0'
        if not(len(itemGame.select('div.discount')) == 0) :
            discount = itemGame.select('div.discount')[0].get_text()
            discount = discount[1:-1]

        print(discount)

        # Insert data in array
        my_data.append({"title": title, "url": url, "store": store, "discount" : discount, "price" : price})


reached_end = False
p = 1

while not reached_end :

    # Get Url Games list Xcloud
    # Must use /en/search instead to get the english url of the games from https://www.instant-gaming.com/en/search/?type%5B0%5D=geforce-now&page=1
    #driver.get('https://www.instant-gaming.com/fr/rechercher/?type%5B0%5D=geforce-now&page=' + str(p))
    driver.get('https://www.instant-gaming.com/en/search/?type%5B0%5D=geforce-now&page=' + str(p))

    # Confirmation get url
    print('GAME LIST OK')

    # Introduction beautifulsoup, must use html5lib otherwise html.parser doesn't get all the divs
    # soup = BeautifulSoup(driver.page_source,'html5lib')
    soup = BeautifulSoup(driver.page_source,'html.parser')
    # print(soup.prettify())

    # get global items list
    my_items = soup.select('div.item.force-badge')
    get_items(my_items)

    print(p)

    p = p + 1

    if soup.find_all("div", {"class": "noresult-browse"}) :
        reached_end = True

    time.sleep(20)

with open('ig-soup.json', 'w') as outfile:
    json.dump(my_data, outfile)

    print('JSON OK')

driver.close()