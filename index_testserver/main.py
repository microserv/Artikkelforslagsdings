#-*- coding:utf8 -*-
from twisted.web import server, resource
from twisted.internet import reactor
import json

class IndexQueries(resource.Resource):
    isLeaf = True
    def render_POST(self, request):
        d = json.load(request.content)
        print("Index received: {}".format(d))
        
        if not 'Partial' in d:
            result = "{'a':1, 'b':5, 'c':120}"
        
        elif d['Partial'] == True:
            word = d['Query']
            completions = ['{}_{}'.format(word,c) for c in ['c1', 'c2', 'c3']]
            result = "{'Result' : %s}" % (completions)
        else:
            word = d['Query']
            locations = ['{}'.format(L) for L in ['http://1', 'http://2', 'http://3']]
            result = "{'Result' : %s}" % (locations)
        print(result)
        #request.write(result)
        #request.finish()
        #return server.NOT_DONE_YET
        return result
site = server.Site(IndexQueries())
reactor.listenTCP(8001, site)
reactor.run()


