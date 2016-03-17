from twisted.web import server
from twisted.internet import reactor
import __builtin__

from server import Searches
from client import IndexQueryFactory

__builtin__.__dict__['reactor'] = reactor

reactor.listenTCP(8000, server.Site(Searches()))
reactor.run()

