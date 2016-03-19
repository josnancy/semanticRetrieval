
from whoosh import qparser
from whoosh.analysis import RegexTokenizer
from whoosh.lang.porter import stem
from whoosh.lang.morph_en import variations
from whoosh.analysis import StopFilter


def queryParsing(query):
    print("inside queryParsing")
    tokenizer = RegexTokenizer()
    return_list = []   
    
    #Removing stop words
    stopper = StopFilter()
    tokens = stopper(tokenizer(query))

    for t in tokens:
        
        #converting to lower case
        t.text = t.text.lower()
        
        #stemming
        s=stem(t.text)
        return_list.append(s)
        
        #adding variations
        termVariations = variations(t.text)
        for u in termVariations:
            return_list.append(u)

    return return_list