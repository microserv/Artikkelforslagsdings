import nltk
from ast import literal_eval
import json
class Query(object):
    def __init__(self, d):
        self.d = d
        self.is_partial = d['Partial']
        self.raw_querystring = d['Query']

        if self.is_partial:
            self.query = {"Partial": True, "Query": self.raw_querystring}
        else:
            qs = process_query(self.raw_querystring)
            self.query = {"Partial": False, "Query": qs}

    #Encode for index (to dict)
    def prepare(self):
        return self.query

#Process the (complete) querystring with normalization/stemming and various enhancements 
def process_query(s):
    s2 = s
    s2 = _normalize_query(s2)
    s2 = _enhance_query(s2)
    return s2

#Stemming
def _normalize_query(s):
    pass

#Hva?
def _enhance_query(s):
    pass
