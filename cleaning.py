import pandas as pd
import numpy as np
import sys, nltk
from nltk.tokenize import TweetTokenizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pylab as plt
import re

NEGATIVE = 0
POSITIVE = 1
NEUTRAL = 2

def getFirstFile(loc):
    title = ('EmotionLevel', 'TwitterID', 'PostTime', 'IsQuery', 'Username', 'content')
    data_set = pd.read_csv(loc, names=title, usecols=[0,1,2,3,4,5], encoding="ISO-8859-1")
    data_set = data_set.drop('TwitterID', 1)
    data_set = data_set.drop('IsQuery', 1)
    return data_set

def getDateAndTweetList(data_set):
    all_tweets = data_set['content'].tolist()
    all_dates = data_set['PostTime'].tolist()
    return all_tweets, all_dates

# Takes a list of tweets as sentences
def tokenizer(tweet_set):
    tknzr = TweetTokenizer(strip_handles=True)
    tknzd_tweets = []
    for sent in tweet_set:
        tmp_sent = tknzr.tokenize(sent)
        tknzd_tweets.append(tmp_sent)
    return tknzd_tweets

def VaderFormat(tweet_set):
    # Replace real URLs with 'URL'
    print ("Tweets tokenized, now removing URLs")
    compl_tweets = []
    for sent in tweet_set:
        tmp_sent = []
        for word in sent:
            word = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', word)
            tmp_sent.append(word)
        # Transforms the list to a singular string for Vader
        compl_tweets.append(" ".join(str(x) for x in tmp_sent))
    return compl_tweets

def VaderScore(tweet_set):
    sid = SentimentIntensityAnalyzer()
    updated_list = []
    for sentence in tweet_set:
        print (sentence)
        ss = sid.polarity_scores(sentence)
        if ss['compound'] >= 0.5:
            updated_list.append((sentence, POSITIVE))
        elif ss['compound'] <= -0.5:
            updated_list.append((sentence, NEGATIVE))
        else:
            updated_list.append((sentence, NEUTRAL))
    return updated_list

if __name__ == "__main__":
    print ("Starting cleaning process")
    print ("Step 1: Retrieve Data")

    first_path = './Data_Sets/set1.csv'
    set1 = getFirstFile(first_path)
    print ("Successfully retrieved the data sets")

    # Working with smaller subset to speed things up
    small_set = set1[:1000]

    print ("Moving on to sort the tweets")
    all_tweets, all_dates = getDateAndTweetList(small_set)
    print ("Now tokenizing the tweets")
    tknzd_tweets = tokenizer(all_tweets)
    vader_tweets = VaderFormat(tknzd_tweets)
    print("Scoring each tweet")
    scored_tweets = VaderScore(vader_tweets[:10])
    print(scored_tweets)
