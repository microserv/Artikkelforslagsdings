#-*- coding:utf8 -*-
from twisted.web import server, resource
from twisted.internet import reactor, defer
from twisted.python import log

from server import Searches
from client import IndexQueryFactory

from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import TCP4ServerEndpoint

import json


import queries
import client
#Convey searches to index and back
class SearchServer(resource.Resource):
    isLeaf = True
    def render_POST(self, request):
        request_dict = json.load(request.content)
        self.d_query = defer.Deferred()
        self.d_query.addCallbacks(self.send_query, log.err)
        reactor.callLater(0,self.preprocess_query, request_dict)
        
        #qs = json.dumps(query.prepare())
        #df = defer.Deferred()
        #result = reactor.call(client.send_query,self.reactor,qs)
        #result = client.send_query(reactor, qs)

        #process client result
        #...
        return ''
    def preprocess_query(self, request_dict):
        if self.d_query is None:
            print('No deferred')
            return
        d_query = self.d_query
        self.d_query = None
        processed_query_dict = queries.Query(request_dict)
        d_query.callback(processed_query_dict)
        return
    def send_query(self,query):
        qs = json.dumps(query.prepare())
        print(qs)

class SearchServerFactory(server.Site):
    def buildProtocol(self, addr):
        print(addr)
        return server.Site(SearchServer())               
reactor.listenTCP(8000, SearchServerFactory('127.0.0.1'))
reactor.run()

