import os
import wget
import json
from bs4 import BeautifulSoup
import requests
from selenium import webdriver

import time

# For decode Unicode characters
import unidecode
import re

# url = 'https://www.nvidia.com/fr-fr/geforce-now/games'
# response = requests.get(url)

# if response.status_code != 200 :
#     print('Failed to get HTML', response.status_code, response.reason)
#     exit()


# html = response.text
# print(html)

# if not os.path.exists('gfnpc.json') :
#     fs = wget.download(url='https://static.nvidiagrid.net/supported-public-game-list/gfnpc.json', out='gfnpc.json')

# if not os.path.exists('gfngames.html') :
#     fs = wget.download(url='https://www.nvidia.com/fr-fr/geforce-now/games', out='gfngames.html')

# file = 'gfngames.html'
# with open(file, encoding='utf8') as f :
#      html = f.read()
#      print(html)

path = './drivers/geckodriver.exe'
browser = webdriver.Firefox(executable_path = path)
time.sleep(10)
browser.get('https://www.nvidia.com/fr-fr/geforce-now/games')
time.sleep(10)
data = {}
data['data'] = []
soup = BeautifulSoup(browser.page_source, 'html.parser')
items = soup.select('div.div-game-name')
time.sleep(10)
for item in items :
    title = item.select('span.game-name.highlight-green')[0].get_text()
    
    #store = 'N/A'

    # remove copyright in title
    title = title.replace('®','').replace('™','')
    
    # Create Store key and Extract Word between parenthese in title for value
    store = title[title.find('(')+1:title.find(')')]
    
    # Remove word between parenthes in title after create store
    title = re.sub(r"\([^()]*\)","", title)

    # remove last space in title - lstrip for first space
    title = title.rstrip()

    title = unidecode.unidecode(title)

    data['data'].append({'title' : title, 'store' : store})
    print(title)

with open('./gfndata.json', 'w') as outfile:
    json.dump(data, outfile)