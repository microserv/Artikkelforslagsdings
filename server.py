#-*- coding:utf8 -*-
from twisted.web import server, resource
from twisted.internet import reactor

class Searches(resource.Resource):
    isLeaf = True
    def render_POST(self, request):
        print(request.content.read())
        return ''


site = server.Site(Searches())
reactor.listenTCP(8000, site)
reactor.run()

#curl -i -H "Content-Type: application/json" -X POST -d {"key":"value"} 127.0.0.1:8000
