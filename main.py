#-*- coding:utf8 -*-
from twisted.web import server, resource
from twisted.web.client import Agent
from twisted.web.http_headers import Headers
from twisted.internet import reactor, defer
from twisted.python import log
from twisted.internet.task import deferLater
from twisted.web.server import NOT_DONE_YET


import json


import queries

#Convey searches to index and back
class SearchServer(resource.Resource):
    isLeaf = True
    def render_POST(self, request):
        request_dict = json.load(request.content)

        processed_query_dict = self.preprocess_query(request_dict)

        index_response = self.send_query_to_index(processed_query_dict)

        r = self.send_query_to_index(processed_query_dict)

        #process client result
        #...
        return ''
        
    def preprocess_query(self, request_dict):
        processed_query_dict = queries.Query(request_dict)
        return processed_query_dict

    def send_query_to_index(self,query):
        indexquery_string = json.dumps(query.prepare())
        agent = Agent(reactor)
        print(indexquery_string)
        #{"Query": "forskrift om utdanning ", "Partial": true}
        d = agent.request(
            'POST',
            'http://127.0.0.1:8001',
            Headers({'User-Agent': ['Twisted Search'],
                     'Accept':['application/json'], 
                     'Content-Type':['application/json']
                     }),
            indexquery_string)
        def asdfg(x):
            print(x)
        d.addCallback(lambda x: asdfg(x))

        #return NOT_DONE_YET
        return ""

#agent = Agent(reactor)
site=server.Site(SearchServer())               

reactor.listenTCP(8000,site)
reactor.run()

