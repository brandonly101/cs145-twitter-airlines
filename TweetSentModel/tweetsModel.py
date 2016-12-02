# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 01:26:59 2016

@author: simon_hua
"""

from __future__ import division
import pandas as pd
import nltk
import re
from collections import Counter
from nltk.corpus import stopwords
from nltk.collocations import BigramCollocationFinder, TrigramCollocationFinder

# Converts a string to tokens
def string2tokens(string):
    #regular expressions
    string = re.sub(r"\@[a-z]+", "", string) #remove the @jetblue...
    string = re.sub(r"http\S+", "", string) #remove http....
    string = re.sub(r"&lt;3", "heartemojii", string) #heartemojii
    string = re.sub(r"&amp", "&", string)
    string = re.sub(r"[^a-z0-9\s]", "", string) #remove most punctuation
    
    string = string.decode('utf8')
    tokens = nltk.word_tokenize(string)
    return(tokens)

tweets = pd.read_csv("Kaggle/Tweets.csv")

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
    #print fdist.most_common(100)
    
    #return a dictionary of only the words with support more than min support
    dic = { k:v for k, v in fdist.items() if v >= min_support }

    return Counter(dic)

min_supp = 3

oneword_pos = extract_onewords(pos_tweets, min_supp)
oneword_neu = extract_onewords(neu_tweets, min_supp)
oneword_neg = extract_onewords(neg_tweets, min_supp)

bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()

def extract_bigrams(tweets, min_support = 1):
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
    final_nltk = nltk.Text(tokens)

    finder = BigramCollocationFinder.from_words(final_nltk)
    
    #only bigrams that satisfy minimum support
    finder.apply_freq_filter(min_support)
    
    finder = finder.ngram_fd.items()
    
    bigrams = {z[0]:z[1] for z in finder}
    
    return Counter(bigrams)

bigrams_pos = extract_bigrams(pos_tweets)
bigrams_neu = extract_bigrams(neu_tweets)
bigrams_neg = extract_bigrams(neg_tweets)

def extract_trigrams(tweets, min_support = 1):
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
    final_nltk = nltk.Text(tokens)

    finder = TrigramCollocationFinder.from_words(final_nltk)
    
    #only bigrams that satisfy minimum support
    finder.apply_freq_filter(min_support)
    
    finder = finder.ngram_fd.items()
    
    trigrams = {z[0]:z[1] for z in finder}
    
    return Counter(trigrams)

trigrams_pos = extract_trigrams(pos_tweets)
trigrams_neu = extract_trigrams(neu_tweets)
trigrams_neg = extract_trigrams(neg_tweets)

#return the 10 n-grams with the highest PMI
#finder.nbest(bigram_measures.pmi, 10)

################################################################################
# Scoring System
################################################################################

class TweetScoreMachine:
    def __init__(self, fd, bg = None, tg = None):
        self.freq_dist = fd
        self.bigram_dist = bg
        self.trigram_dist = tg
        self.sents = ['pos', 'neu', 'neg']

        self.n_freq_dist = Counter()
        self.n_bigram_dist = Counter()
        self.n_trigram_dist = Counter()

        for sent in self.sents:
            for key, count in fd[sent].iteritems():
                self.n_freq_dist[sent] += count
            for key, count in bg[sent].iteritems():
                self.n_bigram_dist[sent] += count
            for key, count in tg[sent].iteritems():
                self.n_trigram_dist[sent] += count

    # Get the score of a list of tokens. Scoring is based on the frequency of a negative in each of the bags
    # (i.e. if a word appears 172 times in a bag, then that word will count for 172 points.
    def get_score(self, tweet_tokens, bigrams = 0, trigrams = 0, bigram_factor = 2, trigram_factor = 3):
        scores = {}
        for sent in self.sents:
            scores[sent] = 0.0

        # For each word in the tweet, check to see if it is in the freq. dist.; if it is,
        # add the normalized points of it to the total score.
        for token in tweet_tokens:
            for sent in self.sents:
                if (self.freq_dist[sent][token] != 0.0):
                    scores[sent] += self.n_freq_dist[sent] / self.freq_dist[sent][token]

        # Factor in bigrams if the option is set.
        if (bigrams):
            for sent in self.sents:
                for i in range(0, len(tweet_tokens) - 1):
                    bigram = tweet_tokens[i] + tweet_tokens[i+1]
                    if (self.bigram_dist[sent][bigram] != 0.0):
                        scores[sent] += self.n_bigram_dist[sent] / self.bigram_dist[sent][bigram] * bigram_factor

        # Factor in trigrams if the option is set.
        if (trigrams):
            for sent in self.sents:
                for i in range(0, len(tweet_tokens) - 1):
                    trigram = tweet_tokens[i] + tweet_tokens[i+1]
                    if (self.trigram_dist[sent][trigram] != 0.0):
                        scores[sent] += self.n_trigram_dist[sent] / self.trigram_dist[sent][trigram] * trigram_factor

        # Normalize the scores.
        total_score = 0.0
        for sent in self.sents:
            total_score += scores[sent]
        for sent in self.sents:
            if (total_score != 0.0):
                scores[sent] /= total_score

        # Return as a tuple.
        return scores

fd = {'pos': oneword_pos, 'neu': oneword_neu, 'neg': oneword_neg}
bg = {'pos': bigrams_pos, 'neu': bigrams_neu, 'neg': bigrams_neg}
tg = {'pos': trigrams_pos, 'neu': trigrams_neu, 'neg': trigrams_neg}

scorer = TweetScoreMachine(fd, bg, tg)
# test_sentence = "annoying"
# test_score = scorer.get_score(nltk.word_tokenize(test_sentence))
# print test_score

f = open("file.txt", "w")

tweets_mat = tweets.as_matrix()
for i in range(0, 169):
    tweet_text = tweets.iloc[i].text
    tweet_sentiment = tweets.iloc[i].airline_sentiment
    tweet_line_print = "\" (should be: " + tweet_sentiment + ") " + str(scorer.get_score(string2tokens(tweet_text), 1, 1))
    # print tweet_line_print
    print >> f, tweet_line_print

f.close()
