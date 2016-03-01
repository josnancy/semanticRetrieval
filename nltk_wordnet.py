# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 09:00:33 2016

@author: nancy
"""

from nltk.corpus import wordnet

def getSynonyms(text):
    synonyms = []
    for syn in wordnet.synsets(text):
        for l in syn.lemmas():
            synonyms.append(l.name())
    return set(synonyms)

def getSimilarWords(text):
    similarWords=[]
    for ss in wordnet.synsets(text):
        for sim in ss.similar_tos():
            similarWords.append(sim.name())
    return set(similarWords)

        

