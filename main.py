#-*- coding:utf8 -*-
from twisted.web import server, resource
from twisted.web.client import Agent
from twisted.web.http_headers import Headers
from twisted.internet import reactor, defer
from twisted.python import log
from twisted.internet.task import deferLater
from twisted.web.server import NOT_DONE_YET

from server import Searches
from client import IndexQueryFactory

import json


import queries
import client
#Convey searches to index and back
class SearchServer(resource.Resource):
    isLeaf = True
    def render_POST(self, request):
        request_dict = json.load(request.content)
        #self.d_query = defer.Deferred()
        #self.d_query.addCallbacks(self.send_query, log.err)
        #reactor.callLater(0,self.preprocess_query, request_dict)
        
        q = self.preprocess_query(request_dict)
        print("P")
        r = self.send_query(q)
        return NOT_DONE_YET
        ##self.send_query(q)
        
        #process client result
        #...
        ##return ''
    def preprocess_query(self, request_dict):
        #if self.d_query is None:
        #    print('No deferred')
        #    return
        #d_query = self.d_query
        #self.d_query = None
        processed_query_dict = queries.Query(request_dict)
        #d_query.callback(processed_query_dict)
        #return
        return processed_query_dict
    def send_query(self,query):
        qs = json.dumps(query.prepare())
        d = agent.request(
            'POST',
            'http://127.0.0.1:8001',
            Headers({'Accept':['application/jsonrequest'], 'Content-Type':['application/jsonrequest']}),
            qs)
        d.addCallback(self.delayed)
        
    def delayed(self, request):
        print("Q")
        print(request)
def cbResponse(ignored):
    print 'Response received'
agent = Agent(reactor)
    
site=server.Site(SearchServer())               
reactor.listenTCP(8000,site)
reactor.run()

