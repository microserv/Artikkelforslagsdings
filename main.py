#!/usr/bin/env python
#-*- coding:utf8 -*-
from twisted.web import server, resource
from twisted.web.http_headers import Headers
from twisted.internet import reactor
from twisted.python import log
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import TCP4ClientEndpoint

import json

import CONFIG
import queries
import client

class SearchServer(resource.Resource):
    """Receives and responds to search queries"""
    isLeaf = True
    def __init__(self):
        pass
    def render_GET(self, request):
        if request.uri == '/static/swagger.json':
            with open(path.join('static', 'swagger.json')) as f:
                s = f.read()
            return s
        else:
            return NoResource().render(request)
    def render_POST(self, request):
        request_dict = json.load(request.content)
    
        result = self.process_query(request_dict)        
        print('Query: {}'.format(request_dict))
        #result.addCallback(lambda x:request.write(fx(x)))

        #Takes care of the case where response is a deferred by 
        #adding callbacks to write the result when the result is ready.
        if type(result) == list or type(result) == dict:
            request.write(json.dumps(result).encode('utf8'))
            request.finish()
        else:
            result.addCallback(lambda x:request.write(json.dumps(x).encode('utf8')))
            result.addCallback(lambda x:request.finish())      
        return server.NOT_DONE_YET

    def process_query(self, request_dict):
        """Send query for processing, i.e to generate a response depending on query parameters"""
        q = queries.Query(request_dict)
        return q.process()

if __name__ == '__main__':
    site=server.Site(SearchServer()) 
    reactor.listenTCP(CONFIG.SEARCH_SERVER_PORT,site)
    reactor.run()

