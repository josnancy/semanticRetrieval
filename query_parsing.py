# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 18:18:37 2016

@author: nancy
"""

from whoosh import qparser
from whoosh.analysis import RegexTokenizer
from whoosh.lang.porter import stem
from whoosh.lang.morph_en import variations
from whoosh.analysis import StopFilter

def queryParsing(query):
   
    tokenizer = RegexTokenizer()
    return_list = []   
    
    #Removing stop words
    stopper = StopFilter()
    tokens = stopper(tokenizer(query))

    for t in tokens:
        
        #converting to lower case
        t.text = t.text.lower()
        
        #stemming
        #s=stem(t.text)
        
        #adding variations
        termVariations = variations(t.text)
        for u in termVariations:
            return_list.append(u)

    return return_list
