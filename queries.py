import nltk
from ast import literal_eval
import json
import re

class Query(object):
    def __init__(self, d):
        self.d = d
        self.is_partial = d['Partial']
        self.raw_querystring = d['Query']

        if self.is_partial:
            qs = process_partial(self.raw_querystring)
            self.query = {"Partial": True, "Query": qs}
        else:
            qs = process_query(self.raw_querystring)
            self.query = {"Partial": False, "Query": qs}

    #Encode for index (to dict)
    def prepare(self):
        return self.query

#Process the (partial) query. Mainly process any complete words before the last (incomplete) words.
#The assumption is that if a query contains multiple words, all the words but the last are "complete",
#and can be considered a complete query
def process_partial(s):
    s2 = s
    s2 = re.sub('\s+', ' ', s2).lstrip()
    parts = s2.split()
    complete = ' '.join(parts[:-1])
    partial = parts[-1]
 
    complete = process_query(complete)
    s2 = ' '.join([complete, partial])
#Process the (complete) querystring with normalization/stemming and various enhancements 
def process_query(s):
    s2 = s
    s2 = re.sub('\s+', ' ', s2).lstrip()
    s2 = _normalize_query(s2)
    s2 = _enhance_query(s2)
    return s2

#Stemming
def _normalize_query(s):
    return s

#Hva?
def _enhance_query(s):
    return s
