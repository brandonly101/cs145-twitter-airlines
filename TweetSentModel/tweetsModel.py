# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 01:26:59 2016

@author: simon_hua
"""

import pandas as pd
import nltk

tweets = pd.read_csv("../Kaggle/Tweets.csv")

#separate into positive, neutral, and negative tweets
pos_tweets = tweets[tweets.airline_sentiment == "positive"]
neu_tweets = tweets[tweets.airline_sentiment == "neutral"]
neg_tweets = tweets[tweets.airline_sentiment == "negative"]

#extract the texts into a list of tweets
list_pos_tweets = pos_tweets.text.tolist()
final_pos_text = ""

#append each tweet to make a giant string
for i in range(len(list_pos_tweets)):
    final_pos_text = final_pos_text + " " + list_pos_tweets[i]

#decode and tokenize for natural language processing
final_pos_text = final_pos_text.decode('utf8')
pos_tokens = nltk.word_tokenize(final_pos_text)
good = nltk.Text(pos_tokens)

#most common pairs of words
# print "\n *** MOST COMMON GOOD WORD COLLOCATIONS ***\n"
# good.collocations()

#Frequency distribution of the most common words
fdist1 = nltk.FreqDist(good)

#==============================================================================
# #extract the texts into a list of tweets
# list_pos_tweets = pos_tweets.text.tolist()
# final_pos_text = ""
#
# #append each tweet to make a giant string
# for i in range(len(list_pos_tweets)):
#     final_pos_text = final_pos_text + " " + list_pos_tweets[i]
#
# #decode and tokenize for natural language processing
# final_pos_text = final_pos_text.decode('utf8')
# pos_tokens = nltk.word_tokenize(final_pos_text)
# good = nltk.Text(pos_tokens)
#
# #most common pairs of words
# good.collocations()
#
# #Frequency distribution of the most common words
# fdist1 = nltk.FreqDist(good)
#==============================================================================
fdist1.most_common(100)

#extract the texts into a list of tweets
list_neu_tweets = neu_tweets.text.tolist()
final_neu_text = ""

#append each tweet to make a giant string
for i in range(len(list_neu_tweets)):
    final_neu_text = final_neu_text + " " + list_neu_tweets[i]

#decode and tokenize for natural language processing
final_neu_text = final_neu_text.decode('utf8')
neu_tokens = nltk.word_tokenize(final_neu_text)
ok = nltk.Text(neu_tokens)

#most common pairs of words
# print "\n *** MOST COMMON OK WORD COLLOCATIONS ***\n"
# ok.collocations()

#Frequency distribution of the most common words
fdist2 = nltk.FreqDist(ok)
fdist2.most_common(100)

#extract the texts into a list of tweets
list_neg_tweets = neg_tweets.text.tolist()
final_neg_text = ""

#append each tweet to make a giant string
for i in range(len(list_neg_tweets)):
    final_neg_text = final_neg_text + " " + list_neg_tweets[i]

#decode and tokenize for natural language processing
final_neg_text = final_neg_text.decode('utf8')
neg_tokens = nltk.word_tokenize(final_neg_text)
bad = nltk.Text(neg_tokens)

#most common pairs of words
# print "\n *** MOST COMMON BAD WORD COLLOCATIONS ***\n"
# bad.collocations()

#Frequency distribution of the most common words
fdist3 = nltk.FreqDist(bad)
fdist3.most_common(100)

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
