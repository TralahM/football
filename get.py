#!/usr/bin/env python

import http.client
import json
API='278236859e9f4dff94372b4af8037d31'

connection = http.client.HTTPConnection('api.football-data.org')
headers = { 'X-Auth-Token': API  }
connection.request('GET', '/v2/competitions/PL/matches', None, headers )
Response = json.loads(connection.getresponse().read().decode())
print(Response.keys())
print(len(Response['matches']))
print((Response['matches'][0].keys()))

for i in range(len(Response['matches'])):
    print(Response['matches'][i]['utcDate'].split('T')[0],Response['matches'][i]['homeTeam']['name'],'',Response['matches'][i]['awayTeam']['name'])

