from twisted.internet import reactor, protocol

class IndexQuery(protocol.Protocol):
    def connectionMade(self):
        

class IndexQueryFactoy(protocol.ClientFactory):
    def __init__(self, query):
        pass

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed")
        

    def clientConnectionLost(self, connector, reason):
        print("Connection lost")
        
def send_query(query):
    f = IndexQueryFactory(query)
    reactor.connectTCP("localhost", 8000, f)
    reactor.run()

