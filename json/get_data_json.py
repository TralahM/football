#!/usr/bin/env python

import http.client
import json
import argparse
from time import sleep

API = '278236859e9f4dff94372b4af8037d31'
connection = http.client.HTTPConnection('api.football-data.org')
headers = {'X-Auth-Token': API}


def get_teams(ids=[]):
    for id in ids:
        connection.request('GET', '/v2/competitions/%s/teams' %
                           id, None, headers)
        response = json.loads(connection.getresponse().read().decode())
        print(response.keys())
        json.dump(response, open("teams_%s.json" % id, 'w'))


def get_schedules(ids=[]):
    for id in ids:
        connection.request('GET', '/v2/competitions/%s/matches' %
                           id, None, headers)
        response = json.loads(connection.getresponse().read().decode())
        print(response.keys())
        json.dump(response, open("matches_%s.json" % id, 'w'))


def get_leagues(ids=[]):
    for id in ids:
        connection.request('GET', '/v2/competitions/%s' % id, None, headers)
        response = json.loads(connection.getresponse().read().decode())
        print(response.keys())
        json.dump(response, open("leagues_%s.json" % id, 'w'))


if __name__ == '__main__':
    ps = argparse.ArgumentParser()
    ps.add_argument('-i', action='store', dest='lid',
                    help="the league id or code", default='PL')
    args = ps.parse_args()
    league_ids = ['2002', 'PL', 'CL', '2019', '2017']
    get_teams(league_ids)
    sleep(30)
    get_schedules(league_ids)
    sleep(60)
    get_leagues(league_ids)
