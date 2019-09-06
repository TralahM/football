#!/usr/bin/env python
"""
-----------------------------------------------
File:fetch_matches.py
Author: Tralah M Brian
Email: <musyoki.tralah@students.jkuat.ac.ke>
Github: <https://github.com/TralahM/>
LICENSE: MIT, CREATIVE-COMMONS
COPYRIGHT: (2019) All Rights Reserved
-----------------------------------------------

Description: A script to obtain data from football-data.org and load/update
it to a MySQL Database on a remote Server....
Useful for obtaining football data for applications, research, analytics, data
science or even machine learning!.....
"""
import os
try:
    os.system('pip install pandas numpy sqlalchemy MySQLdb')
except Exception as e:
    print(e)

import pandas as pd
from pandas.io import sql
from sqlalchemy import create_engine
import http.client
import json
import argparse

API = '278236859e9f4dff94372b4af8037d31'
DB_USER = 'root'
DB_PASS = 'password'
DB_HOST = 'localhost'
DB_NAME = 'betmeback'
try:
    ENGINE = create_engine(
        'mysql://{0}:{1}@{2}/{3}'.format(DB_USER, DB_PASS, DB_HOST, DB_NAME)
    )
except Exception as e:
    print(e)


def update_db_teams(dataframe):
    with ENGINE.connect() as conn, conn.begin():
        dataframe.to_sql('teams', conn, if_exists='replace')
        dataframe.to_sql('allteams', conn, if_exists='replace')


def update_db_schedules(dataframe):
    with ENGINE.connect() as conn, conn.begin():
        dataframe.to_sql('schedules', conn, if_exists='replace')
        dataframe.to_sql('fixtures', conn, if_exists='replace')


def update_db_leagues(dataframe):
    with ENGINE.connect() as conn, conn.begin():
        dataframe.to_sql('leagues', conn, if_exists='replace')


def get_team_number(code):
    res = teams(code)
    return res['count']


def get_match_number(code):
    res = fixtures(code)
    return res['count']


def league_list(Response):
    columns = ['league_id', 'caption', 'league', 'start_date', 'end_date',
               'number_of_teams', 'number_of_matches', 'current_matchday']
    league_id = Response[id]
    caption = Response['area']['name']+" "+Response['name']
    league = Response['code']
    start_date = Response['currentSeason']['startDate']
    end_date = Response['currentSeason']['endDate']
    number_of_teams = get_team_number(league)
    number_of_matches = get_match_number(league)
    current_matchday = Response['currentSeason']['currentMatchday']
    with open(competition_code+"_league.csv", "w") as cf:
        cf.writelines(','.join(columns)+"\n")
        cf.writelines(','.join(str(k) for k in [
                      league_id, caption, league, start_date, end_date, number_of_teams, number_of_matches, current_matchday])+'\n')
        print(','.join(str(k) for k in [league_id, caption, league, start_date,
                                        end_date, number_of_teams, number_of_matches, current_matchday])+'\n')


def team_list(Response):
    columns = ['betradar_id', 'league_id', 'name', 'short_name', 'crest_url']
    league_id = Response['competition']['id']
    competition_code = Response['competition']['code']
    teams = Response['teams']
    with open(competition_code+"_teams.csv", "w") as cf:
        cf.writelines(','.join(columns)+"\n")
        for team in teams:
            ln = list()
            ln.append(team["id"])
            ln.append(competion_code)
            ln.append(team["name"])
            ln.append(team["shortName"])
            ln.append(team["crestUrl"])
            print(','.join(str(i) for i in ln))
            cf.writelines(str(','.join(str(i) for i in ln))+"\n")
        print("\t\tDone!")


def match_list(Response):
    columns = ['match_id', 'match_date', 'match_time', 'home_team_id', 'home_team_name', 'away_team_id',
               'away_team_name', 'league_id', 'match_day', 'home_team_score', 'away_team_score', 'status', 'Winner']

    matches = Response['matches']
    nmatches = len(matches)
    competition_code = Response['competition']['code']
    league_id = Response['competition']['id'].__str__()
    with open(competition_code+".csv", 'w') as cf:
        cf.writelines(','.join(columns)+"\n")
        for match in matches:
            ln = list()
            ln.append(match['id'])
            ln.append(match['utcDate'].split('T')[0])
            ln.append(match['utcDate'].split('T')[1].split('Z')[0])
            ln.append(match['homeTeam']['id'].__str__())
            ln.append(match['homeTeam']['name'])
            ln.append(match['awayTeam']['id'].__str__())
            ln.append(match['awayTeam']['name'])
            ln.append(league_id)
            ln.append(match['matchday'])
            ln.append(match['score']['fullTime']['homeTeam'].__str__())
            ln.append(match['score']['fullTime']['awayTeam'].__str__())
            ln.append(match['status'].__str__())
            ln.append(match['score']['winner'])
            print(','.join(str(i) for i in ln))
            cf.writelines(str(','.join(str(i) for i in ln))+"\n")
        print("\t\tDone!")
    cf.close()


def unify_teams_csv():
    team_csv = ["PL_teams.csv", "BL1_teams.csv",
                "SA_teams.csv", "PD_teams.csv", "CL_teams.csv"]
    dfs = [pd.read_csv(fl) for fl in team_csv]
    master_teams = pd.concat(dfs, axis=0)
    return master_teams


def unify_matches_csv():
    match_csv = ["PL.csv", "BL1.csv", "SA.csv", "PD.csv", "CL.csv"]
    dfs = [pd.read_csv(fl) for fl in match_csv]
    master_fixtures = pd.concat(dfs, axis=0)
    return master_fixtures


def generate_csvs():
    league_ids = ['PL', '2002', '2019', '2014', 'CL']
    for lid in league_ids:
        match_list(fixtures(lid))
        team_list(teams(lid))
        league_list(leagues(lid))
    print("done getting csv data")


def fixtures(Code):
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = {'X-Auth-Token': API}
    connection.request('GET', '/v2/competitions/%s/matches' %
                       Code, None, headers)
    Response = json.loads(connection.getresponse().read().decode())
    return Response


def leagues(Code):
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = {'X-Auth-Token': API}
    connection.request('GET', '/v2/competitions/%s' %
                       Code, None, headers)
    Response = json.loads(connection.getresponse().read().decode())
    return Response


def teams(Code):
    connection = http.client.HTTPConnection('api.football-data.org')
    headers = {'X-Auth-Token': API}
    connection.request('GET', '/v2/competitions/%s/teams' %
                       Code, None, headers)
    Response = json.loads(connection.getresponse().read().decode())
    return Response


if __name__ == '__main__':
    parser = argparse.ArgumentParser(epilog=__doc__.split('\n')[0])
    # Get the csvs first
    generate_csvs()
    # update database with master csv
    update_db_schedules(unify_matches_csv())
    update_db_teams(unify_teams_csv())
    print("Done with Database Update...")
