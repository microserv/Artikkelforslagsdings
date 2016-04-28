from twisted.internet.defer import DeferredList
from twisted.internet.defer import Deferred
import nltk
from ast import literal_eval
import json
import re
from os import path

import client
import CONFIG

class Query(object):
    def __init__(self, d):
        self.d = d
        self.is_partial = d['Partial']
        self.raw_querystring = d['Query']
            
    def process(self):
        parts = self.tokenize(self.raw_querystring)
        normalized = self.normalize(parts)
        spellcheck = self.spellcheck(normalized)
        def complete_deferreds(dlist, spell_length):
            if not self.is_partial:
                RL_set = set()
                for elem in dlist[:-spell_length]:
                    elem_s = elem[1]
                    print(elem_s)
                    d = json.loads(elem_s)
                    if type(d) == int:
                        continue

                    if d.get("articleID"):
                        RL_set.update(d["articleID"])
                    elif d.get("Result"):
                        RL_set.update(d['Result'])

                RL = list(RL_set)
                    
            SL = []
            if spell_length > 0:
                for elem in dlist[-spell_length:]:
                    elem_s = elem[1]
                    mini_list = json.loads(elem_s)
                    SL.append(mini_list)
            
            if self.is_partial:
                d = {u'spell': SL}
            else:
                d = {u'spell': SL, u'results': RL}

            return d

        if not self.is_partial:
            
            deferreds = [Result_Query(norm).get_results() for norm in normalized]
            deferreds.extend(spellcheck)
            
            dlist = DeferredList(deferreds)
            dx = dlist.addCallback(lambda x:complete_deferreds(x,spell_length=len(spellcheck)))

            return dx
        else:
            deferreds = []
            deferreds.extend(spellcheck)
            
            dlist = DeferredList(deferreds)
            dx = dlist.addCallback(lambda x:complete_deferreds(x,spell_length=len(spellcheck)))            
            return dx
        
    #Encode for index (to dict)
    def tokenize(self, query):
        #remove additional whitespace, other than trailing ##Kanskje endre?
        s = re.sub('\s+', ' ', query).lstrip()
        parts = s.split()
        return parts

    def normalize(self, parts):
        '''normalize by stemming and converting to lowercase'''
        #stemmer = nltk.stem.snowball.NorwegianStemmer(ignore_stopwords=False)
        #words = [stemmer.stem(word).lower() for word in parts)]

        #do not actually stem at the moment, maybe later
        words = [word.lower() for word in parts]
        return words
        
    def spellcheck(self, parts):
        if self.is_partial:
            enhanced = [Spell_Query(word).correct() for word in parts[:-1]]
            if parts[-1] and self.raw_querystring[-1] and parts[-1]:
                enhanced.append(Spell_Query(parts[-1]).complete())
        else:
            enhanced = [Spell_Query(word).correct() for word in parts ]
        return enhanced
        
       
TRUE = False
#TRUE = True
class Spell_Query(object):
    def __init__(self, word):
        self.word = word
        self.spell_host = CONFIG.spell_host
    def correct(self):
        d = {'Type': 'correction', 'Search': TRUE, 'Query': self.word}
        result = client.send_query(d, self.spell_host)
        return result

    def complete(self):
        d = {'Type': 'completion', 'Search': TRUE, 'Query': self.word}
        result = client.send_query(d, self.spell_host)
        return result
        

class Result_Query(object):
    def __init__(self, word):
        self.word = word
        self.index_host = CONFIG.index_host
    def get_results(self):
        d = {'task': 'getArticles', 'word': self.word}
        result = client.send_query(d, self.index_host)
        return result
    
