# -*- coding: utf-8 -*-
"""
Created on Fri May 22 11:21:03 2015

@author: josephdziados
"""

import urllib2
import re
from bs4 import BeautifulSoup
import pickle
import pandas as pd
import json
import csv
from pymongo import MongoClient

def build_soup_page(page = "", url = "", use_url=False):
    """
    Returns a BeautifulSoup object by calling the server using a passed url if 
    use_url = True, otherwise takes in a string of html and returns a 
    BeautifulSoup object.
    
    page = string
    url = string
    use_url = boolean
    """
    if use_url:
        page = urllib2.urlopen(url)
        return BeautifulSoup(page)
    else:
        return BeautifulSoup(page)
        
def store_pickles(filename, to_store):
    """Dumps information in to_store into a file named filename.
    
    filename = string
    to_store = list, dictionary, etc.    
    """  
    with open(filename, 'w') as f:
        pickle.dump(to_store, f)
        
        
def eat_pickles(filename):
    """Loads information from a pickle file.
    
    filename = string
    """
    
    with open(filename, 'r') as f:
        return pickle.load(f)
        
        
def create_wine_doc(soup): 
    
    indiv_wine = {}
 
     # Winemaker notes
    try:    
        indiv_wine['notes'] = soup.find('div', {'class': 'winemakers-notes'}).find('p').text
    except AttributeError:
        indiv_wine['notes'] = 'N/A'
    
     # Wine name 
    try:    
        name = soup.find('h1', {'id': 'wine-name'}).text.strip()
        indiv_wine['name'] = ' '.join(name.split())
    except:
        indiv_wine['name'] = 'N/A'
        
     # Region
    try:
        indiv_wine['region'] = soup.find('div', {'class': 'wpp2014-reg_rat-region'}).find('a').text
    except AttributeError:
        indiv_wine['region'] = 'N/A'
    
     # Color
    try:
        indiv_wine['color'] = soup.find('div', {'class': 'wpp2014-reg_rat-region_vintage'}).find('span').find_next_sibling().text
    except:
        indiv_wine['color'] = 'N/A'
    
     # Varietal    
    if soup.find('div', {'class': 'wpp2014-reg_rat-region_vintage'}) != None:
        for label in soup.find('div', {'class': 'wpp2014-reg_rat-region_vintage'}).find_all('b'):
            if label.text == 'Varietal:':
                indiv_wine['varietal'] = label.find_next_sibling().text
            elif label.text == 'Variety:':
                indiv_wine['varietal'] = label.find_next_sibling().text
            elif label.text == 'Blend:':
                wine_blends = []
                blends = label.find_next_siblings()
                for blend in blends:
                    wine_blends.append(blend.text)
                indiv_wine['varietal'] = wine_blends
    else:
        indiv_wine['varietal'] = 'N/A'
    
     # Reviews
    reviews = []
   
    if soup.find('div', {'id': 'external-reviews'}) != None:
        for el in soup.find('div', {'id': 'external-reviews'}).find_all('p'):
            reviews.append(el.text.strip())
    if soup.find('div', {'id': 'user-reviews'}) != None:
        for el in soup.find('div', {'id': 'user-reviews'}).find_all('p'):
            reviews.append(el.text.strip())
            
    indiv_wine['reviews'] = reviews
    
    return indiv_wine
    
#client = MongoClient()
#db = client.wines
#snooth = db.snooth
        
#wine_urls = []
#
#for page_num in xrange(2,1001):
#    print 'Scraping Page {0} ....'.format(page_num)
#    soup = build_soup_page(url='http://www.snooth.com/wines/?p={0}'.format(page_num), use_url=True)
#    for snippet in soup.find_all('div', {'class': 'snippet'}):
#        wine_urls.append(snippet.find('a').get('href'))
#    print 'Success'
    
#store_pickles('wine_urls.pkl', wine_urls)
#eat_pickles('wine_urls.pkl')

#wine_soup_html = {}
#
#for i, url in enumerate(wine_urls):
#    print 'Creating BS object {0}'.format(i)
#    wine_soup = build_soup_page(url=url, use_url=True)
#    wine_soup_html[url] = str(wine_soup)
#    print 'Success for url {0}'.format(url)

#store_pickles('wine_pages.pkl', wine_soup_html)
#wine_soup_html = eat_pickles('wine_pages.pkl')

wines = []

for url, html in wine_soup_html.items():
    print 'Building dictionary for {0}'.format(url)
    soup = build_soup_page(html)
    wine_dict = create_wine_doc(soup)
    wines.append(wine_dict)   
    
 # Manual adjustments
for wine in wines:
    if wine['name'] == 'Walter Hansel Cahill Lane Vyd. Pinot Noir 2011':
        wine['color'] = 'Red'
        
for wine in wines:
    if wine['name'] == 'J.P. Chenet Reserve Cabernet-Merlot 2011':
        wine['color'] = 'Red'
        
for wine in wines:
    if wine['name'] == 'Alsace Willm Gewurztraminer 2013':
        wine['color'] = 'White'
        
for wine in wines:
    if wine['name'] == 'Seppeltsfield Cellar No 8 Muscat NV':
        wine['color'] = 'Red'
        
for wine in wines:
    if wine['name'] == 'Scharffenberger Brut Rose Excellence NV':
        wine['color'] = 'Red'
        
for wine in wines:
    if wine['name'] == 'Graham\'s Vintage Porto 2011':
        wine['color'] = 'Red'
        
for wine in wines:
    if wine['name'] == 'Zugibe Lemberger 2010':
        wine['color'] = 'White'
        
for wine in wines:
    if wine['name'] == 'Cooks Brut California NV':
        wine['color'] = 'White'
        
for wine in wines:
    if wine['name'] == 'Sato No Homare Pride of the Village Junmai Ginjo NV':
        wine['color'] = 'White'
        
for wine in wines:
    if wine['name'] == 'Freixenet Carta Nevada Brut Spain Cataluna Cava 2006':
        wine['color'] = 'White'
        
for wine in wines:
    if wine['name'] == 'Joseph Carr Cabernet Sauvignon Napa Valley 2012':
        wine['color'] = 'Red'
        
for wine in wines:
    if wine['name'] == 'Hewitt Cabernet Rutherford 2011':
        wine['color'] = 'Red'
        
for wine in wines:
    if wine['name'] == 'Plumpjack Merlot Napa Valley 2010':
        wine['color'] = 'Red'
        
for wine in wines:
    if wine['name'] == 'Grgich Hills Cabernet Sauvignon Napa Valley 2011':
        wine['color'] = 'Red'  

wine_copy = wines[:]     
for wine in wine_copy:
    if wine['color'] == 'N/A':
        wines.remove(wine)
    
store_pickles('wine_dict.pkl', wines) 
    
#for wine in wines: 
#    snooth.insert({'color': wine['color'], 'name': wine['name'],
#                   'notes': wine['notes'], 'region': wine['region'],
#                   'reviews': wine['reviews'], 'varietal': wine['varietal']})
    
# Left off sorting out varities
varities = []
for wine in wines:
    if 'varietal' in wine.keys() and type(wine['varietal']) != list:
        varities.append(wine['varietal'])
varities = set(varities)
print varities