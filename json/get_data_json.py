#!/usr/bin/env python

import http.client
import json
import argparse

API = '278236859e9f4dff94372b4af8037d31'
connection = http.client.HTTPConnection('api.football-data.org')
headers = {'X-Auth-Token': API}


def get_teams(ids=[]):
    for id in ids:
        connection.request('GET', '/v2/competitions/%d/teams' %
                           id, None, headers)
        Response = json.loads(connection.getresponse().read().decode())
        print(Response.keys())
        json.dump(response, open("teams_%d.json" % id, 'w'))


def get_schedules(ids=[]):
    for id in ids:
        connection.request('GET', '/v2/competitions/%d/matches' %
                           id, None, headers)
        Response = json.loads(connection.getresponse().read().decode())
        print(Response.keys())
        json.dump(response, open("matches_%d.json" % id, 'w'))


def get_leagues(id=[]):
    for id in ids:
        connection.request('GET', '/v2/competitions/%d' % id, None, headers)
        Response = json.loads(connection.getresponse().read().decode())
        print(Response.keys())
        json.dump(response, open("matches_%d.json" % id, 'w'))


if __name__ == '__main__':
    ps = argparse.ArgumentParser()
    league_ids = [2002, 2072, 2077, 2019, 2017]
    get_teams(league_ids)
    get_schedules(league_ids)
    get_leagues(league_ids)
