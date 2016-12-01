# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 01:26:59 2016

@author: simon_hua
"""

import pandas as pd
import nltk
import re
from nltk.corpus import stopwords

tweets = pd.read_csv("Tweets.csv")

#stopwords = insignificant words
stops = set(stopwords.words('english'))

#separate into positive, neutral, and negative tweets
pos_tweets = tweets[tweets.airline_sentiment == "positive"]
neu_tweets = tweets[tweets.airline_sentiment == "neutral"]
neg_tweets = tweets[tweets.airline_sentiment == "negative"]

def extract_onewords(tweets, min_support = 1):
    #extract the texts into a list of tweets
    list_tweets = tweets.text.tolist()
    final_text = ""

    #append each tweet to make a giant string
    for i in range(len(list_tweets)):
        list_tweets[i] = list_tweets[i].lower()
        final_text = final_text + " " + list_tweets[i]
    
    #regular expressions
    final_text = re.sub(r"\@[a-z]+", "", final_text) #remove the @jetblue...
    final_text = re.sub(r"http\S+", "", final_text) #remove http....
    final_text = re.sub(r"&lt;3", "heartemojii", final_text) #heartemojii
    final_text = re.sub(r"&amp", "&", final_text)
    final_text = re.sub(r"[^a-z0-9\s]", "", final_text) #remove most punctuation

    #decode and tokenize for natural language processing
    final_text = final_text.decode('utf8')
    tokens = nltk.word_tokenize(final_text)

    #get rid of stopwords
    dummy1 = [] 
    for token in tokens:
      if token not in stops:
          dummy1.append(token)
  
    tokens = dummy1
    
    final_nltk = nltk.Text(tokens)

    #Frequency distribution of the most common words
    fdist = nltk.FreqDist(final_nltk)
    print fdist.most_common(100)
    
    #return a dictionary of only the words with support more than min support
    dic = dict(fdist)
    dic = { k:v for k, v in dic.items() if v >= min_support }
    
    return (dic)
    
    
oneword_pos = extract_onewords(pos_tweets)
oneword_neu = extract_onewords(neu_tweets)
oneword_neg = extract_onewords(neg_tweets)

################################################################################
# Scoring System
###

# Get the score of a list of tokens. Scoring is based on the frequency of a negative in each of the bags
# (i.e. if a word appears 172 times in a bag, then that word will count for 172 points.
def get_score(tweet_tokens):
    good_score = 0.0
    ok_score = 0.0
    bad_score = 0.0

    for token in tweet_tokens:
        good_score += fdist1[token]
        ok_score += fdist2[token]
        bad_score += fdist3[token]

    # Normalize the scores.
    totalScore = good_score + ok_score + bad_score
    good_score = good_score / totalScore
    ok_score = ok_score / totalScore
    bad_score = bad_score / totalScore

    # print "Good score: " + str(good_score)
    # print "Ok score: " + str(ok_score)
    # print "Bad score: " + str(bad_score)

    # Return as a tuple.
    return (good_score, ok_score, bad_score)

test_sentence = "This is a test sentence meant to give a bad score. Airline bad baggage failure annoying late flight delay"
test_score = get_score(nltk.word_tokenize(test_sentence))
print test_score
