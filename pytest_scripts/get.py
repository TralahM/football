#!/usr/bin/env python

import http.client
import json
API='278236859e9f4dff94372b4af8037d31'

connection = http.client.HTTPConnection('api.football-data.org')
headers = { 'X-Auth-Token': API  }
connection.request('GET', '/v2/competitions/PL/matches', None, headers )
Response = json.loads(connection.getresponse().read().decode())
print(Response.keys())

#for i in range(len(Response['matches'])):
#    print(Response['matches'][i]['utcDate'].split('T')[0],Response['matches'][i]['homeTeam']['name'],'',Response['matches'][i]['awayTeam']['name'])

for k in Response.keys():
    print(k)
    if isinstance(Response[k],dict):
        for l in Response[k].keys():
            print(k,'-->',l)
            if isinstance(Response[k][l],dict):
                for j in Response[k][l].keys():
                    print(k,'-->',l,'-->',j)
    if isinstance(Response[k],list):
        if isinstance(Response[k][0],dict):
            for m in Response[k][0].keys():
                print(k, '[0] -->', m)
                if isinstance(Response[k][0][m],dict):
                    for n in Response[k][0][m].keys():
                        print(k, '[0] -->',m,'-->',n)
