#-*- coding:utf8 -*-
from twisted.web import server, resource
from twisted.internet import reactor

class Searches(resource.Resource):
    isLeaf = True
    def render_GET(self, request):
        args=request.args
        for arg in args:
          print('{}: {}'.format(arg,args[arg]))
        return ''


site = server.Site(Searches())
reactor.listenTCP(8000, site)
reactor.run()

#{'title': ['Boks'], 'Author': ['TRK']}
#↓
#curl -i -H "Accept: application/json" "127.0.0.1:8000/getName?Author=TRK&title=Boks"
