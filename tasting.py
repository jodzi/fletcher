# -*- coding: utf-8 -*-
"""
Created on Thu May 28 15:11:09 2015

@author: josephdziados
"""

import urllib2
import re
from bs4 import BeautifulSoup
import pickle
import pandas as pd

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
        return BeautifulSoup(page, 'xml')
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
    
    # Name    
    indiv_wine['name'] = ' '.join(soup.find('div', {'align': 'left'}).text.encode('ascii', 'ignore').split())

    # Review
    indiv_wine['review'] = str(' '.join(soup.find_all('td', {'class': 'desctext'})[1].text.encode('ascii', 'ignore').split()))

    # Varietal, color
    #if soup.find_all('b')[7].find_next_sibling().previous_element:
    all_bs = [str(el) for el in soup.find_all('b')]
    if all_bs.index('<b>CATEGORY:</b>'):
        index = all_bs.index('<b>CATEGORY:</b>')
        varietal, color = soup.find_all('b')[index].find_next_sibling().previous_element.split(',')
    else:
        indiv_wine['varietal'] = None
    indiv_wine['varietal'] = varietal.strip()
    indiv_wine['color'] = color.strip()
    
    return indiv_wine
        
#wine_urls = []

#for i in range(0,10000,20):
#    print 'Collected {0} wines...'.format(i+20)
#    soup = build_soup_page(url='http://tastings.com/search_wine.lasso?se=k&sb=All&sf=ScoreForSort&dt=208&sk={0}'.format(i), use_url=True)
#    for link in soup.find_all('a', {'class': 'deschead'}):
#        wine_urls.append('http://www.tastings.com/{0}'.format(link['href']))
#    print 'Success...'

#store_pickles('tasting_urls.pkl', wine_urls)

#tasting_soup_html = {}
#
#for i, url in enumerate(wine_urls):
#    print 'Creating BS object {0}'.format(i)
#    wine_soup = build_soup_page(url=url, use_url=True)
#    tasting_soup_html[url] = str(wine_soup)
#    print 'Success for url {0}'.format(url)

#store_pickles('tasting_html.pkl', tasting_soup_html)
#tasting_html = eat_pickles('tasting_html.pkl')

#wines = []
#i = 1
#
#for url, html in tasting_html.iteritems():
#    print 'Wine {0}: Building dictionary for {1}'.format(i, url)
#    soup = build_soup_page(html)
#    wine_dict = create_wine_doc(soup)
#    wines.append(wine_dict) 
#    i += 1
    
#store_pickles('tasting_wines.pkl', wines)