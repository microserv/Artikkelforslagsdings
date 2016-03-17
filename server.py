#-*- coding:utf8 -*-
#from __builtins__ impor
from twisted.web import server, resource
import json

import queries
import client

#Convey searches to index and back
class Searches(resource.Resource):
    isLeaf = True
    def render_POST(self, request):
        d = json.load(request.content)
        query = queries.Query(d)
        qs = json.dumps(query.prepare())
        result = client.send_query(reactor, qs)

        #process client result
        #...
        return ''


#INPUT FRA SØKEFRONTEND/BRUKER:
##Kan optimiseres senere -- til f.eks {1|0, ...}, men for øyeblikket er lesbarhet å foretrekke.
#json
#{
#Partial : true|false
#Query : '...'
#}
#
#
#Delvis query, sendes mer eller mindre direkte videre til indeks for forslag til utfylling.
#   bruker --> søk
#   curl -i -H "Content-Type: application/json" -X POST -d '{"Partial":true, "Query":"Forskri"}' 127.0.0.1:8000
#
#
#Komplett query, output til indeks har diverse normaliseringer som stemming (Forskrifter->forskrift)
#   bruker -->søk
#   curl -i -H "Content-Type: application/json" -X POST -d '{"Partial":false, "Query":"Forskrifter"}' 127.0.0.1:8000
#--------------------------------------



#INPUT TIL INDEKS FRA SØK:
#json
#{
#Partial : true|false
#Query : '...'
#}
#
#
#Delvis query 
#   søk --> indeks
#   '{"Partial":true, "Query":"Forskri"}'
#forventer svar:
#   Liste over forslag til utfyllinger [Forskrift, Forskriftsansvarlig, Forskribblestudie, ...]
#   Format på returliste er ganske fritt
#
#Komplett query
#   søk --> indeks
#   '{"Partial":false, "Query":"Forskrift"}'
#forventer svar:
#   Liste over resultater.
#   Format på returliste er ganske fritt, men resultatlisten *må* inneholde URI til artikkelene eller dokumentene der hvert resultat kan finnes
#--------------------------------------

