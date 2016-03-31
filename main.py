#-*- coding:utf8 -*-
from twisted.web import server, resource
from twisted.web.client import Agent
from twisted.web.http_headers import Headers
from twisted.internet import reactor, defer
from twisted.python import log
from twisted.internet.task import deferLater
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import TCP4ClientEndpoint

import json

import queries

class SearchIndexClient(Protocol):
    def connectionMade(self):
        self.transport.write(self.factory.requestquery)
        self.transport.loseConnection()

#Convey searches to index and back
class SearchServer(resource.Resource):
    isLeaf = True
    def render_POST(self, request):
        request_dict = json.load(request.content)

        processed_query_dict = self.preprocess_query(request_dict)

        index_response = self.send_query_to_index(processed_query_dict)
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
        #d = agent.request(
            #'POST',
            #'http://127.0.0.1:8001',
            #Headers({'User-Agent': ['Twisted Search'],
            #         'Accept':['application/json'], 
            #         'Content-Type':['application/json']
            #         }),
            #indexquery_string)
            
        QUERY = """
POST / HTTP/1.1
Host: 127.0.0.1:8001
User-Agent: FUCKJAVA
Content-Type: application/json
Content-Length: {LEN}

{JSON_STRING}""".strip().replace('\n', '\r\n').format(LEN=len(indexquery_string), JSON_STRING=indexquery_string)

        factory = Factory()
        factory.protocol = SearchIndexClient
        factory.requestquery = QUERY
        point = TCP4ClientEndpoint(reactor, "127.0.0.1", 8001)
        d = point.connect(factory)

        return ""

#agent = Agent(reactor)
site=server.Site(SearchServer()) 
reactor.listenTCP(8000,site)
reactor.run()

