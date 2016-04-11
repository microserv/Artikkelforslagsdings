#-*- coding:utf8 -*-
from twisted.web import server, resource
from twisted.internet import reactor
import json

class IndexQueries(resource.Resource):
    isLeaf = True
    def render_POST(self, request):
        d = json.load(request.content)
        print("Index received: {}".format(d))
        
        if d['task'] == 'getFrequencyList':
            result = {'forskr_c1':1, 'forskr_c3':5, 'forskr_c2':120}
        
        elif d['task'] == 'getSuggestions':
            word = d['word']
            completions = ['{}_{}'.format(word,c) for c in ['c1', 'c2', 'c3']]
            result = {'suggestions' : completions}
        elif d['task'] == 'getArticles':
            word = d['word']
            locations = ['{}'.format(L) for L in ['http://1', 'http://2', 'http://3']]
            result = {'articleID' : locations}
        print(result)
        request.write(json.dumps(result))
        request.finish()
        return server.NOT_DONE_YET
site = server.Site(IndexQueries())
reactor.listenTCP(8001, site)
reactor.run()


