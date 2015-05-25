# -*- coding: utf-8 -*-
"""
Created on Sun May 24 13:15:57 2015

@author: josephdziados
"""

import urllib2
from bs4 import BeautifulSoup
import pickle

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
 
     # Winemaker notes    
    try:   
        indiv_wine['notes'] = soup.find('section', {'class': 'wineMakerNotes'}).find('p').text
    except AttributeError:
        indiv_wine['notes'] = 'N/A'
    
    # Acclaim review
    acclaims = []
    try:
        if soup.find('span', {'class': 'reviewText'}):
            for acclaim in soup.find_all('span', {'class': 'reviewText'}):
                acclaims.append(soup.find('span', {'class': 'reviewText'}).text)
            indiv_wine['acclaim'] = acclaims
        else:
            indiv_wine['acclaim'] = 'N/A'
    except:
        indiv_wine['acclaim'] = 'N/A'
    
    # Style
#    style = []    
#    try:    
#        if soup.find('ul', {'class': 'product-icons'}):
#            for desc in soup.find('ul', {'class': 'product-icons'}).find_all('li'):
#                style.append(', '.join(desc.text.split()))
#            if len(style) > 3:
#                indiv_wine['style'] = style[1]
#            else:
#                indiv_wine['style'] = 'N/A'
#        else:
#            indiv_wine['style'] = 'N/A'
#    except:
#        indiv_wine['style'] = 'N/A'
    
     # Wine name 
    try:
        indiv_wine['name'] = soup.find('section', {'class': 'productAbstract'}).find('h1').text.strip()
    except:
        indiv_wine['name'] = 'N/A'
        
     # Region & Varietal
    try:        
        reg_var = soup.find('section', {'class': 'productAbstract'}).find('h2').text.split('from')
        varietal, region = reg_var[0].strip(), reg_var[1].strip()
        indiv_wine['varietal'] = varietal
        indiv_wine['region'] = region
    except:
        indiv_wine['varietal'] = 'N/A'
        indiv_wine['region'] = 'N/A'
    
     # Reviews
    reviews = []
   
    if soup.find('div', {'class': 'reviewText'}) != None:
        for review in soup.find_all('div', {'class': 'reviewText'}):
            if review.text.strip() != '':
                reviews.append(review.text.strip()) 
                
    indiv_wine['reviews'] = reviews
    
    return indiv_wine
        
#wine_urls = []
#for wines in xrange(100, 7800, 100):
#    print '{0} wine urls scraped....'.format(wines)
#    soup = build_soup_page(url='http://www.wine.com/v6/wineshop/default.aspx?pagelength=100&Nao={0}'.format(wines), use_url=True)
#    for product in soup.find('ul', {'class': 'productList'}).find_all('div', {'class': 'productName'}):
#        wine_urls.append(product.find('a').get('href'))
#    print 'Success'
        
#store_pickles('wine_com_urls.pkl', wine_urls)
#wine_urls = eat_pickles('wine_com_urls.pkl')
        
#wine_soup_html = {}
#
#for i, url in enumerate(wine_urls):
#    print 'Creating BS object {0}'.format(i)
#    url = 'http://www.wine.com{0}'.format(url)
#    wine_soup = build_soup_page(url=url, use_url=True)
#    wine_soup_html[url] = str(wine_soup)
#    print 'Success for url {0}'.format(url)

#store_pickles('wine_com_html.pkl', wine_soup_html)
#wine_soup_html = eat_pickles('wine_com_html.pkl')

#wines = []
#i = 1
#
#for url, html in wine_soup_html.iteritems():
#    print 'Wine {0}: Building dictionary for {1}'.format(i, url)
#    soup = build_soup_page(html)
#    wine_dict = create_wine_doc(soup)
#    wines.append(wine_dict) 
#    i += 1

#store_pickles('wine_com_dict.pkl', wines)

