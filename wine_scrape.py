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
        
def wine_com_doc(soup): 
    
    indiv_wine = {}
 
     # Winemaker notes    
#    try:   
#        indiv_wine['notes'] = soup.find('section', {'class': 'wineMakerNotes'}).find('p').text
#    except AttributeError:
#        indiv_wine['notes'] = 'N/A'
    
    # Acclaim review
#    acclaims = []
#    try:
#        if soup.find('span', {'class': 'reviewText'}):
#            for acclaim in soup.find_all('span', {'class': 'reviewText'}):
#                acclaims.append(soup.find('span', {'class': 'reviewText'}).text)
#            indiv_wine['acclaim'] = acclaims
#        else:
#            indiv_wine['acclaim'] = 'N/A'
#    except:
#        indiv_wine['acclaim'] = 'N/A'
    
     # Wine name 
    #try:
    name = soup.find('section', {'class': 'productAbstract'}).find('h1').text.strip()
    name = sorted(name.split())
    if name[0] in ['2014','2013','2012','2011', '2010', '2009', '2008', '2007', '2006', '2005', '2004', '2003', '2002', '2001', '2000', '1999', '1998', '1997', '1996']: 
        indiv_wine['name'] = name[1:]
        if soup.find_all('span', {'class': 'salesPrice'}):
            indiv_wine['price'] = soup.find('span', {'class': 'salesPrice'}).text
        elif soup.find('span', {'class': 'regularPrice'}):
            indiv_wine['price'] = soup.find('span', {'class': 'regularPrice'}).text
        elif soup.find('span', {'class': 'priceLabel'}):
            indiv_wine['price'] = soup.find('span', {'class': 'priceLabel'}).text
        #else:
        #    indiv_wine['price'] = 'Sold Out'
#    except:
#        indiv_wine['name'] = 'N/A'
         
     # Region & Varietal
#    try:        
#        reg_var = soup.find('section', {'class': 'productAbstract'}).find('h2').text.split('from')
#        varietal, region = reg_var[0].strip(), reg_var[1].strip()
#        indiv_wine['varietal'] = varietal
#        indiv_wine['region'] = region
#    except:
#        indiv_wine['varietal'] = 'N/A'
#        indiv_wine['region'] = 'N/A'
    
     # Reviews
#    reviews = []
#   
#    if soup.find('div', {'class': 'reviewText'}) != None:
#        for review in soup.find_all('div', {'class': 'reviewText'}):
#            if review.text.strip() != '':
#                reviews.append(review.text.strip()) 
#                
#    indiv_wine['reviews'] = reviews
    
    return indiv_wine
    
def tasting_wine_doc(soup): 
    
    indiv_wine = {}
    
    # Name    
    indiv_wine['name'] = ' '.join(soup.find('div', {'align': 'left'}).text.encode('ascii', 'ignore').split())

    # Review
    indiv_wine['review'] = str(' '.join(soup.find_all('td', {'class': 'desctext'})[1].text.encode('ascii', 'ignore').split()))

    # Varietal, color
    all_bs = [str(el) for el in soup.find_all('b')]
    if all_bs.index('<b>CATEGORY:</b>'):
        index = all_bs.index('<b>CATEGORY:</b>')
        varietal, color = soup.find_all('b')[index].find_next_sibling().previous_element.split(',')
    else:
        indiv_wine['varietal'] = None
    indiv_wine['varietal'] = varietal.strip()
    indiv_wine['color'] = color.strip()
    
    return indiv_wine
    
def snooth_get_blend(soup, wine_dict):
    
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
    
      
def snooth_wine_doc(soup): 
    
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

# Wine.com
#wine_com_urls = []
#for wines in xrange(100, 7800, 100):
#    print '{0} wine urls scraped....'.format(wines)
#    soup = build_soup_page(url='http://www.wine.com/v6/wineshop/default.aspx?pagelength=100&Nao={0}'.format(wines), use_url=True)
#    for product in soup.find('ul', {'class': 'productList'}).find_all('div', {'class': 'productName'}):
#        wine_urls.append(product.find('a').get('href'))
#    print 'Success'
        
#store_pickles('wine_com_urls.pkl', wine_urls)
#wine_urls = eat_pickles('wine_com_urls.pkl')
        
# Snooth.com
#wine_urls = []
#
#for page_num in xrange(2,1001):
#    print 'Scraping Page {0} ....'.format(page_num)
#    soup = build_soup_page(url='http://www.snooth.com/wines/?p={0}'.format(page_num), use_url=True)
#    for snippet in soup.find_all('div', {'class': 'snippet'}):
#        wine_urls.append(snippet.find('a').get('href'))
#    print 'Success'
    
#store_pickles('wine_urls.pkl', wine_urls)
#wine_urls = eat_pickles('wine_urls.pkl')
    
# Tasting.com
#wine_urls = []

#for i in range(0,10000,20):
#    print 'Collected {0} wines...'.format(i+20)
#    soup = build_soup_page(url='http://tastings.com/search_wine.lasso?se=k&sb=All&sf=ScoreForSort&dt=208&sk={0}'.format(i), use_url=True)
#    for link in soup.find_all('a', {'class': 'deschead'}):
#        wine_urls.append('http://www.tastings.com/{0}'.format(link['href']))
#    print 'Success...'

#store_pickles('tasting_urls.pkl', wine_urls)
#wine_urls = eat_pickles('wine_urls.pkl')
    
    
    

        
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
#
#wines = []
#i = 1
#
#for url, html in wine_soup_html.iteritems():
#    print 'Wine {0}: Building dictionary for {1}'.format(i, url)
#    soup = build_soup_page(html)
#    wine_dict = wine_com_doc(soup)
#    wines.append(wine_dict) 
#    i += 1

#store_pickles('wine_com_dict.pkl', wines)
#store_pickles('wine_com_prices.pkl', priced_wine)


