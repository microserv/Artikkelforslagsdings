from twisted.internet import protocol
from twisted.web.client import Agent
from twisted.web.http_headers import Headers
import json

class IndexQuery(protocol.Protocol):
    def connectionMade(self):
        self.transport.write(self.POST)

class IndexQueryFactory(protocol.ClientFactory):
    def __init__(self, query):
        self.query = query
        self.POST = self.construct_jsonpost(query)

    def construct_jsonpost(self, d):
        src = '''POST /request HTTP/1.1
                 Accept: application/jsonrequest
                 Content-Length: {}
                 Content-Type: application/jsonrequest
                 
                 {}
              '''
        src = '\n'.join(x.strip() for x in src.split('\n'))
        
        dump = json.dumps(d)
        
        src = src.format(len(dump), dump)
        print(src)
        return src

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed")
        

    def clientConnectionLost(self, connector, reason):
        print("Connection lost")
        
def send_query(reactor, query):
    agent = Agent(reactor)
    defer = agent.request(
    'POST',
    'http://127.0.0.1:8001',
    Headers({'Accept':['application/jsonrequest'], 'Content-Type':['application/jsonrequest']}),
    json.dumps(query))
    print(defer)
    print(dir(defer))
