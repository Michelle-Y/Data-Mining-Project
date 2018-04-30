import pandas as pd
import numpy as np
import sys, nltk
import collections
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
        ss = sid.polarity_scores(sentence)
        if ss['compound'] >= 0.5:
            updated_list.append((sentence, POSITIVE))
        elif ss['compound'] <= -0.5:
            updated_list.append((sentence, NEGATIVE))
        else:
            updated_list.append((sentence, NEUTRAL))
    return updated_list

def formatForFile(ugly_text):
    tmp_var = '\n'.join(line.strip() for line in re.findall(r'.{1,80}(?:\s+|$)', ugly_text))
    return tmp_var

def findSentimentClusters(data_set):
    neg_set = []
    pos_set = []
    neu_set = []
    pos_set_words_lateEarly = []
    pos_set_words_mid = []
    pos_set_words_evening = []
    neg_set_words_lateEarly = []
    neg_set_words_mid = []
    neg_set_words_evening = []
    neu_set_words_lateEarly = []
    neu_set_words_mid = []
    neu_set_words_evening = []
    print ("Separating by sentiment to find clusters")
    for item in data_set:
        if item[1][1] == NEGATIVE:
            neg_set.append(item)
        elif item[1][1] == POSITIVE:
            pos_set.append(item)
        elif item[1][1] == NEUTRAL:
            neu_set.append(item)
    print(len(neu_set))
    print("Total Positive Tweets:")
    print(len(pos_set))
    print("Total Negative Tweets:")
    print(len(neg_set))
    print ("Done separating, looking for clusters in the positive set")
    pos_counts = [0,0,0]
    for item in pos_set:
        #Late night and early morning
        if (item[0]>=0) and (item[0]<=700):
            pos_set_words_lateEarly += tokenizer([item[1][0]])[0]
            pos_counts[0] += 1
        elif (item[0]>=2250) and (item[0]<=2400):
            pos_set_words_lateEarly += tokenizer([item[1][0]])[0]
            pos_counts[0] += 1
        elif (item[0]>700) and (item[0]<=1530):
            pos_set_words_mid += tokenizer([item[1][0]])[0]
            pos_counts[1] += 1
        else:
            pos_set_words_evening += tokenizer([item[1][0]])[0]
            pos_counts[2] += 1
    print ("Individual Pos Counts: ")
    print(pos_counts)

    print("Done splitting by time - pos set")
    print("Finding commonalities... - pos set")
    pos_first_count = collections.Counter(pos_set_words_lateEarly)
    pos_sec_count = collections.Counter(pos_set_words_mid)
    pos_third_count = collections.Counter(pos_set_words_evening)

    print("Writing pos commonalities out")
    f = open("pos_lateEarly.txt", "w+")
    f.write(formatForFile(str(pos_first_count.most_common(300))))
    f.close

    f = open("pos_mid.txt", "w+")
    f.write(formatForFile(str(pos_sec_count.most_common(300))))
    f.close()

    f = open("pos_evening.txt", "w+")
    f.write(formatForFile(str(pos_third_count.most_common(300))))
    f.close()
    print ("Done finding commonalities with pos set, moving on to neg set")

    neg_counts = [0,0,0]
    for item in neg_set:
        #Late night and early morning
        if (item[0]>=0) and (item[0]<=700):
            neg_set_words_lateEarly += tokenizer([item[1][0]])[0]
            neg_counts[0] += 1
        elif (item[0]>=2250) and (item[0]<=2400):
            neg_set_words_lateEarly += tokenizer([item[1][0]])[0]
            neg_counts[0] += 1
        elif (item[0]>700) and (item[0]<=1530):
            neg_set_words_mid += tokenizer([item[1][0]])[0]
            neg_counts[1] += 1
        else:
            neg_set_words_evening += tokenizer([item[1][0]])[0]
            neg_counts[2] += 1
    print("Individual Neg Counts:")
    print(neg_counts)

    print("Done splitting by time - neg set")
    print("Finding commonalities... - neg set")
    neg_first_count = collections.Counter(neg_set_words_lateEarly)
    neg_sec_count = collections.Counter(neg_set_words_mid)
    neg_third_count = collections.Counter(neg_set_words_evening)

    f = open("neg_lateEarly.txt", "w+")
    f.write(formatForFile(str(neg_first_count.most_common(300))))
    f.close()

    f = open("neg_mid.txt", "w+")
    f.write(formatForFile(str(neg_sec_count.most_common(300))))
    f.close()

    f = open("neg_evening.txt", "w+")
    f.write(formatForFile(str(neg_third_count.most_common(300))))
    f.close()
    print ("Done finding commonalities with neg set, moving on to neu set")

    neu_counts = [0,0,0]
    for item in neu_set:
        #Late night and early morning
        if (item[0]>=0) and (item[0]<=700):
            neu_set_words_lateEarly += tokenizer([item[1][0]])[0]
            neu_counts[0] += 1
        elif (item[0]>=2250) and (item[0]<=2400):
            neu_set_words_lateEarly += tokenizer([item[1][0]])[0]
            neu_counts[0] += 1
        elif (item[0]>700) and (item[0]<=1530):
            neu_set_words_mid += tokenizer([item[1][0]])[0]
            neu_counts[1] += 1
        else:
            neu_set_words_evening += tokenizer([item[1][0]])[0]
            neu_counts[2] += 1
    print("Individual Neu Counts:")
    print(neu_counts)

    print("Done splitting by time - neu set")
    print("Finding commonalities... - neu set")
    neu_first_count = collections.Counter(neu_set_words_lateEarly)
    neu_sec_count = collections.Counter(neu_set_words_mid)
    neu_third_count = collections.Counter(neu_set_words_evening)

    f = open("neu_lateEarly.txt", "w+")
    f.write(formatForFile(str(neu_first_count.most_common(300))))
    f.close()

    f = open("neu_mid.txt", "w+")
    f.write(formatForFile(str(neu_sec_count.most_common(300))))
    f.close()

    f = open("neu_evening.txt", "w+")
    f.write(formatForFile(str(neu_third_count.most_common(300))))
    f.close()
    print ("Done finding commonalities with neu set, should be done")


if __name__ == "__main__":
    print ("Starting cleaning process")
    print ("Step 1: Retrieve Data")

    first_path = './Data_Sets/set1.csv'
    set1 = getFirstFile(first_path)
    print ("Successfully retrieved the data sets")

    # Working with smaller subset to speed things up
    small_set = set1[:1000]

    print ("Moving on to sort the tweets")
    #CHANGE THIS FOR FINAL RUN. CHANGE 'small_set' TO 'set1'
    all_tweets, all_dates = getDateAndTweetList(set1)
    print ("Now tokenizing the tweets")
    tknzd_tweets = tokenizer(all_tweets)

    #Format for score function
    vader_tweets = VaderFormat(tknzd_tweets)
    print("Scoring each tweet")
    scored_tweets = VaderScore(vader_tweets)

    # Transform dates into just numbers for easier reference
    print("Formatting the dates")
    all_dates = tokenizer(all_dates)
    time_only = []
    for date in all_dates:
        time_only.append(int(date[3].replace(":","")))
    # At this point time_only is just the numbers
    # Combining this with scored tweets to have a singular reference to everything
    print("Combining into singular reference")
    all_data = list(zip(time_only, scored_tweets))

    print("Finding clusters")
    findSentimentClusters(all_data)
