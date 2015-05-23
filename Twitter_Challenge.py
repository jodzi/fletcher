# -*- coding: utf-8 -*-
"""
Created on Thu May 21 16:08:00 2015

@author: josephdziados
"""

import requests
from requests_oauthlib import OAuth1
from pymongo import MongoClient
import tweepy
import cnfg

client = MongoClient()
db = client.mentalhealth
mindfulness = db.mindfulness

config = cnfg.load(".twitter_config")

auth = tweepy.OAuthHandler(config["consumer_key"],
                           config["consumer_secret"])
auth.set_access_token(config["access_token"],
                      config["access_token_secret"])
               
api = tweepy.API(auth)

query = "mindfulness"
max_tweets = 100

mind_tweets = tweepy.Cursor(api.search, q=query).items(max_tweets)

for tweet in mind_tweets:
    mindfulness.insert({'text': tweet.text, 'user': tweet.user.name,
                        'fav_count': tweet.favorite_count, 
                        'retweet_count': tweet.retweet_count})
               