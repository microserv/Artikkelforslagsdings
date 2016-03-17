from twisted.internet import reactor, protocol
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
        
def send_query(query):
    fact = IndexQueryFactory(query)
    print("boop")
    reactor.connectTCP("127.0.0.1", 8001, fact)

