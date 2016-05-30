from twisted.internet.defer import DeferredList
from twisted.internet.defer import Deferred
import nltk
from ast import literal_eval
import json
import re
from os import path

import comm
import client
import CONFIG

class Query(object):
    def __init__(self, d):
        self.d = d
        
        #Partial queries are queries where the user is still "typing", 
        #i.e the user has not commited the search yet.
        self.is_partial = d['Partial']
        self.raw_querystring = d['Query']
            
    def process(self):
        parts = self.tokenize(self.raw_querystring)
        normalized = self.normalize(parts)
        spellcheck = self.spellcheck(normalized)
        def complete_deferreds(dlist, spell_length):
            """Extract the eventual result from deferreds
               
               Input is a deferredlist, where the first (N-spell_length) elements are search results,
               and the last spell_length elements are spellcheck results 
            """
            
            #Partial searches have no search result, as no search is performed with partial search queries. 
            if not self.is_partial:
                RL_set = set()
                for elem in dlist[:-spell_length]:
                    elem_s = elem[1]
                    print(elem_s)
                    d = json.loads(elem_s)
                    
                    #404 for keyword
                    if type(d) == int:
                        continue

                    #Differing APIs, some have results under the key articleID, some under Results
                    if d.get("articleID"):
                        RL_set.update(d["articleID"])
                    elif d.get("Result"):
                        RL_set.update(d['Result'])

                RL = list(RL_set)
            
            #Spelling feedback. A list of lists. One for each word in the query.
            SL = []
            if spell_length > 0:
                for elem in dlist[-spell_length:]:
                    elem_s = elem[1]
                    mini_list = json.loads(elem_s)
                    SL.append(mini_list)
            
            #Partial searches do not have any search results to display
            if self.is_partial:
                d = {u'spell': SL}
            else:
                d = {u'spell': SL, u'results': RL}

            return d

        deferreds = []
        if not self.is_partial:
            #Send a search query to the index for a list of keyword matches, 
            #provided that the search query is not a partail query
            deferreds.extend([Result_Query(norm).get_results() for norm in normalized])
        
        #Extend with spellcheck feedback. 
        #No searches are performed with the spellcheck results, they are returned to the user as feedback.
        #The user has to decide whether to do another search using the feedback on spelling.
        deferreds.extend(spellcheck)
        dlist = DeferredList(deferreds)
        dx = dlist.addCallback(lambda x:complete_deferreds(x,spell_length=len(spellcheck)))            
        return dx
        
    #Encode for index (to dict)
    def tokenize(self, query):
        """remove additional whitespace, other than trailing. 
            
           Split into individual words.
        """
        s = re.sub('\s+', ' ', query).lstrip()
        parts = s.split()
        return parts

    def normalize(self, parts):
        '''normalize by stemming and converting to lowercase
        
           Stemming is currently skipped because spellcheck ignores stopwords.
           Treating all words the same in search is at the moment a cleaner solution.
        '''
        #stemmer = nltk.stem.snowball.NorwegianStemmer(ignore_stopwords=False)
        #words = [stemmer.stem(word).lower() for word in parts)]

        #skip stemming, just lowercase
        words = [word.lower() for word in parts]
        return words
        
    def spellcheck(self, parts):
        """Do the necessary queries for spellcheck on each of the words in the query"""

        #If the search is partial, the last word in the search query is assumed to be partial.
        #Partial words are queried for possible (auto)completions, rather than spelling corrections.
        #Partial words are not spellchecked, as it is difficult to spellcheck a word that is partially complete.
        if self.is_partial:
            #Spellcheck query for all but the last (partial) query word
            enhanced = [Spell_Query(word).correct() for word in parts[:-1]]
            if parts[-1] and self.raw_querystring[-1] and parts[-1]:
                #Query for completions of the last word in the query.
                enhanced.append(Spell_Query(parts[-1]).complete())
        else:
            #Send a spellcheck query for each word, resulting in a list of lists of suggestions for corrections
            enhanced = [Spell_Query(word).correct() for word in parts ]
        return enhanced
        
       
#In the current state of the microservice corpus, there is not a lot of articles.
#This results in the index of articles not having many known keywords.
#As a result it is hard to provide specialized spelling feedback.
#
#In that case, disable the use of the index frequency lists, and rather use a generic frequency list 
#The generic frequency list contains most common words, and will for demonstration purposes provide
#a better exposition of the spellcheck suggestion-features.
#
#(Set to True for the intended functionality, where search will provide specialized (based on article keywords)
#spelling feedback).
USE_SEARCH_FREQ = False
class Spell_Query(object):
    """Spelling queries. Completion and correction."""
    def __init__(self, word):
        self.word = word
        if CONFIG.spell_host == None:
            self.spell_host = 'http://{}:{}/'.format(comm.get_service_ip(CONFIG.spell_service_name, comm_host), CONFIG.spell_port)
        else:
            self.spell_host = CONFIG.spell_host
    def correct(self):
        """Query for finding corrections/edit distances to other more likely words"""
        d = {'Type': 'correction', 'Search': USE_SEARCH_FREQ, 'Query': self.word}
        result = client.send_query(d, self.spell_host)
        return result

    def complete(self):
        """Query for finding completions of the query word."""
        d = {'Type': 'completion', 'Search': USE_SEARCH_FREQ, 'Query': self.word}
        result = client.send_query(d, self.spell_host)
        return result
        

class Result_Query(object):
    """Retrieving results (articles) for a given keyword"""
    def __init__(self, word):
        self.word = word
        if CONFIG.index_host == None:
            self.index_host = 'http://{}:{}/'.format(comm.get_service_ip(CONFIG.index_service_name, comm_host), CONFIG.indexer_port)
        else:
            self.index_host = CONFIG.index_host
    def get_results(self):
        d = {'task': 'getArticles', 'word': self.word}
        result = client.send_query(d, self.index_host)
        return result
    
