#from twisted.trial import unittestf
#from unittest import unittest
import unittest
import os
import requests
import json
from twisted.web import server, resource
from twisted.internet import reactor
#from twisted.python import log
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import TCP4ClientEndpoint
import twisted

import main
import CONFIG
import client
class basic_index(resource.Resource):
    isLeaf = True
    def __init_(self):
        pass
    def render_POST(self, request):
        request_dict = json.load(request.content)
        
        if request_dict['task'] == 'getArticles':
            s = json.dumps({'articleID':[1,2,3,4]})
        return s
        #elif request_dict['task'] == 'getSuggestions':
        #    return json.dumps(['katt', 'kattepus', 'kattesand'])
        
        #elif request_dict['task'] == 'getFrequencyList':
        #    return json.dumps({'katt':100, 'buss':60})
        
class basic_spell(resource.Resource):
    isLeaf = True
    def __init_(self):
        pass
    def render_POST(self, request):
        request_dict = json.load(request.content)
        
        q = request_dict['Query']
        typ = request_dict['Type']
        
        if q == 'appla':
            s = json.dumps(['apple', 'apply'])
        elif q == 'kott':
            s = json.dumps(['katt', 'kutt', 'kost'])
        else:
            if typ == 'completion':
                s = json.dumps(['katt', 'kattepus', 'kattesand'])
            elif typ == 'correction':
                s = json.dumps(['hoste', 'koste', 'poste'])
        return s        
SEARCHSERV = 'http://127.0.0.1:{}/'.format(CONFIG.SEARCH_SERVER_PORT)
class SEARCH(unittest.TestCase):
    def test_01_SETUP(self):
        '''Try to launch a mock spell- and index- service'''
        site_index=server.Site(basic_index())
        site_spell=server.Site(basic_spell())

        spell_port = int(CONFIG.spell_host.split(':')[-1].split('/')[0])        
        index_port = int(CONFIG.index_host.split(':')[-1].split('/')[0])        
        
        try:
            reactor.listenTCP(spell_port, site_spell)
            print('Started mock spell server')
        except twisted.internet.error.CannotListenError:
            raise
        try:
            reactor.listenTCP(index_port, site_index)
            print('Started mock index server')
        except twisted.internet.error.CannotListenError:
            raise
    #def test_02_partial(self):
        def compare_query(x,exp):
            x1 = json.loads(x)['spell']
            self.assertEqual(x1,exp)
        q = {'Partial':True, 'Query':'appla kott kat'}
        d = client.send_query(q, SEARCHSERV)
        d.addCallback(compare_query, [['apple', 'apply'], ['katt', 'kutt', 'kost'], ['katt', 'kattepus', 'kattesand']])
    
    #def test_03_complete(self):
        def compare_query(x,exp):
            x1 = json.loads(x)['spell']
            self.assertEqual(x1,exp)
            self.assertNotEqual(x1,None)
            
        q = {'Partial':False, 'Query':'appla kott moste'}
        d = client.send_query(q, SEARCHSERV)
        d.addCallback(compare_query, [['apple', 'apply'], ['katt', 'kutt', 'kost'], ['hoste', 'koste', 'poste']])

    #def test_04_complete_results(self):
        def compare_query(x,exp):
            x1 = json.loads(x)['results']
            self.assertEqual(x1,exp)
            self.assertNotEqual(x1,None)
            
        q = {'Partial':False, 'Query':'appla kott moste'}
        d = client.send_query(q, SEARCHSERV)
        d.addCallback(compare_query, [1,2,3,4])
    

        def compare_query(x,exp):
            x1 = json.loads(x)['spell']
            self.assertEqual(x1,exp)
        q = {'Partial':False, 'Query':'appla'}
        d = client.send_query(q, SEARCHSERV)
        d.addCallback(compare_query, [['apple', 'apply']])
        mainsite=server.Site(main.SearchServer()) 
        reactor.listenTCP(CONFIG.SEARCH_SERVER_PORT,mainsite)
        reactor.callLater(2,reactor.stop)
        reactor.run()
        
        
if __name__ == '__main__':
    unittest.main()
    
