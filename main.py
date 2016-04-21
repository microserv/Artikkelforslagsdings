#-*- coding:utf8 -*-
from twisted.web import server, resource
from twisted.web.http_headers import Headers
from twisted.internet import reactor
from twisted.python import log
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import TCP4ClientEndpoint

import json

import queries
import client

#Convey searches to index and back
class SearchServer(resource.Resource):
    isLeaf = True
    def __init__(self):
        pass
    def render_POST(self, request):
        request_dict = json.load(request.content)

        result = self.process_query(request_dict)        
        print('Query: {}'.format(request_dict))
        #result.addCallback(lambda x:request.write(fx(x)))
        #
        if type(result) == list or type(result) == dict:
            request.write(json.dumps(result).encode('utf8'))
            request.finish()
        else:
            result.addCallback(lambda x:request.write(json.dumps(x).encode('utf8')))
            result.addCallback(lambda x:request.finish())      
        return server.NOT_DONE_YET
        
    def process_query(self, request_dict):
        q = queries.Query(request_dict)
        return q.process()

site=server.Site(SearchServer()) 
reactor.listenTCP(8000,site)
reactor.run()

