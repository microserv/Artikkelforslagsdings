#-*- coding:utf8 -*-
from twisted.web import server, resource
from twisted.internet import reactor
import json

class IndexQueries(resource.Resource):
    isLeaf = True
    def render_POST(self, request):
        d = json.load(request.content)
        print("Index received: {}".format(d))
        return "ABC"

site = server.Site(IndexQueries())
reactor.listenTCP(8001, site)
reactor.run()


