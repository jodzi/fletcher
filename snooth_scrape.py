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
        
def get_blend(soup, wine_dict):
    
    varieties_list = [u'Cabernet Sauvignon', u'Bordeaux Red Blends', u'Viognier', u'Rose', u'Rose Sparkling Wine', u'Gamay', \
                      u'Zinfandel', u'Rhone Red Blends', u'Merlot', u'Syrah', u'Sauvignon Blanc', u'Other Dessert', u'Sherry', \
                      u'Gewurztraminer', u'Non-Vintage Sparkling Wine', u'Muscat', u'Bordeaux White Blends', u'Pinot Blanc', \
                      u'Other Red Wine', u'Torrontes', u'Nebbiolo', u'Sangiovese', u'Gruner Veltliner', u'Junmai', u'Semillon', \
                      u'Tempranillo', u'Riesling', u'Dolcetto', u'Cabernet Franc', u'Grenache', u'Petite Sirah', u'Madeira', \
                      u'Other White Blends', u'Pinot Noir', u'Chardonnay', u'Albarino', u'Pinot Grigio', u'Fruit Wine', \
                      u'Pinotage', u'Junmai-Daiginjo', u'Other White Wine', u'Malbec', u'Rhone White Blends', u'Vintage Sparkling Wine', \
                      u'Primitivo', u"Nero d'Avola", u'Chenin Blanc', u'Other Red Blends', u'Junmai-Ginjo', u'Barbera', u'Mourvedre', \
                      u'Carmenere', u'Port']
                      
    other_whites = ['Verdejo', 'Cortese', 'Arneis', 'Vermentino', 'Verdelho', 'Trebbiano', 'Moschofilero', 'Sarganega', 'Verdiccio', 'Furmint']
    other_reds = ['Anglianico', 'Blaufrnkisch', 'Carignan', 'Bonarda', 'Teroldego', 'Tannat', 'Graciano', 'Mondeuse', 'Taouriga Nacional']
    sparkling = ['Prosecco', 'Lambrusco']
        
    if soup.find('div', {'class': 'wpp2014-reg_rat-region_vintage'}) != None:
        for label in soup.find('div', {'class': 'wpp2014-reg_rat-region_vintage'}).find_all('b'):
            if label.text.strip() == 'Varietal:' or label.text.strip() == 'Variety':             
                if label.find_next_sibling().text not in varieties_list:
                    if label.find_next_sibling().text in other_whites:
                        wine_dict['varietal'] = 'Other White Wine'
                    elif label.find_next_sibling().text in sparkling:
                        wine_dict['varietal'] = 'Non-Vintage Sparkling Wine'
                    elif label.find_next_sibling().text in other_reds:
                        wine_dict['varietal'] = 'Other Red Wine'
                    elif label.find_next_sibling().text == 'Isabella':
                        wine_dict['varietal'] = 'Pinot Noir'
                    elif label.find_next_sibling().text == 'Grner Veltliner':
                        wine_dict['varietal'] = 'Gruner Veltliner'
                    elif label.find_next_sibling().text == 'Albario':
                        wine_dict['varietal'] = 'Albarino'
                    elif label.find_next_sibling().text == 'Corvina':
                        wine_dict['varietal'] = 'Valpolicella'
                    elif label.find_next_sibling().text == 'Mourvdre':
                        wine_dict['varietal'] = 'Mourvedre'
                    elif label.find_next_sibling().text == 'Smillon':
                        wine_dict['varietal'] = 'Semillon'
                    elif label.find_next_sibling().text == 'Montepulciano':
                        wine_dict['varietal'] = 'Sangiovese'
                    elif label.find_next_sibling().text == 'Vernoccia':
                        wine_dict['varietal'] = 'Other White Blends'
                    elif label.find_next_sibling().text == 'Limberger':
                        wine_dict['varietal'] = 'Other Red Blends'
                    else:
                        try:
                            variety = raw_input('What variety is {0}: '.format(label.find_next_sibling().text))
                        except UnicodeError:
                            variety = raw_input('What variety is {0}: '.format(label.find_next_sibling().text.encode('ascii', 'ignore')))
                        wine_dict['varietal'] = variety
                else:
                    wine_dict['varietal'] = label.find_next_sibling().text
            elif label.text.strip() == 'Blend:':
                wine_blends = []
                blends = label.find_next_siblings()
                for blend in blends:
                    wine_blends.append(blend.text)
                variety = raw_input('What variety is {0}: '.format(wine_blends))
                wine_dict['varietal'] = variety
    else:
        wine_dict['varietal'] = 'N/A'
    
    return wine_dict    
    
    
          
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

#wines = []
#i = 1
#for url, html in wine_soup_html.items()[2000:]:
#    print '#{0} wine; building dictionary for {1}'.format(i, url)
#    soup = build_soup_page(html)
#    wine_dict = create_wine_doc(soup)
#    wine_dict = get_blend(soup, wine_dict)
#    wines.append(wine_dict)
#    i += 1
#    
# # Manual adjustments
#for wine in wines:
#    if wine['name'] == 'Walter Hansel Cahill Lane Vyd. Pinot Noir 2011':
#        wine['color'] = 'Red'
#    elif wine['name'] == 'J.P. Chenet Reserve Cabernet-Merlot 2011':
#        wine['color'] = 'Red'
#    elif wine['name'] == 'Alsace Willm Gewurztraminer 2013':
#        wine['color'] = 'White'
#    elif wine['name'] == 'Seppeltsfield Cellar No 8 Muscat NV':
#        wine['color'] = 'Red'
#    elif wine['name'] == 'Scharffenberger Brut Rose Excellence NV':
#        wine['color'] = 'Red'
#    elif wine['name'] == 'Graham\'s Vintage Porto 2011':
#        wine['color'] = 'Red'
#    elif wine['name'] == 'Zugibe Lemberger 2010':
#        wine['color'] = 'White'
#    elif wine['name'] == 'Cooks Brut California NV':
#        wine['color'] = 'White'
#    elif wine['name'] == 'Sato No Homare Pride of the Village Junmai Ginjo NV':
#        wine['color'] = 'White'
#    elif wine['name'] == 'Freixenet Carta Nevada Brut Spain Cataluna Cava 2006':
#        wine['color'] = 'White'
#    elif wine['name'] == 'Joseph Carr Cabernet Sauvignon Napa Valley 2012':
#        wine['color'] = 'Red'
#    elif wine['name'] == 'Hewitt Cabernet Rutherford 2011':
#        wine['color'] = 'Red'
#    elif wine['name'] == 'Plumpjack Merlot Napa Valley 2010':
#        wine['color'] = 'Red'
#    elif wine['name'] == 'Grgich Hills Cabernet Sauvignon Napa Valley 2011':
#        wine['color'] = 'Red'  
#
#wine_copy = wines[:]     
#for wine in wine_copy:
#    if wine['color'] == 'N/A':
#        wines.remove(wine)
#    
#for wine in wines:
#    if wine['color'] not in ['Amber', 'Clear', 'Red', 'White']:
#        wine['color'] = 'Rose'
    
#store_pickles('wine_dict_fresh.pkl', wines) 
#store_pickles('wine_dict_fresh_2.pkl', wines) 
#wines = eat_pickles('wine_dict.pkl')
    
#for wine in wines: 
#    snooth.insert({'color': wine['color'], 'name': wine['name'],
#                   'notes': wine['notes'], 'region': wine['region'],
#                   'reviews': wine['reviews'], 'varietal': wine['varietal']})
    