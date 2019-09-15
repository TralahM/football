import http.client
from datetime import datetime
import json
import pandas as pd
API = '278236859e9f4dff94372b4af8037d31'


def str2time(strng):
    return datetime.strptime(strng, '%H:%M:%S').time()


def str2date(strng):
    return datetime.strptime(strng, '%Y-%m-%d').date()


def create_db_connection():
    DB_USER = 'root'
    DB_PASS = 'password'
    DB_HOST = 'localhost'
    DB_NAME = 'betmeback'
    try:
        from sqlalchemy import create_engine
        ENGINE = create_engine(
            'mysql+mysqldb://{0}:{1}@{2}/{3}?charset=utf8mb4'.format(
                DB_USER, DB_PASS, DB_HOST, DB_NAME),
            encoding='utf-8',
            convert_unicode=True,
        )
    except Exception as e:
        print(e)
    return ENGINE


def league_json2csv(Response):
    columns = ['league_id', 'caption', 'league', 'start_date', 'end_date',
               'number_of_teams', 'number_of_matches', 'current_matchday']
    league_id = Response['id']
    competition_code = Response['code']
    caption = Response['area']['name']+" "+Response['name']
    league = Response['code']
    start_date = Response['currentSeason']['startDate']
    end_date = Response['currentSeason']['endDate']
    number_of_teams = get_team_number(league)
    number_of_matches = get_match_number(league)
    current_matchday = Response['currentSeason']['currentMatchday']
    with open(competition_code+"_leagues.csv", "w") as cf:
        cf.writelines(','.join(columns)+"\n")
        cf.writelines(','.join(str(k) for k in [
                      league_id, caption, league, start_date, end_date, number_of_teams, number_of_matches, current_matchday])+'\n')
        print(','.join(str(k) for k in [league_id, caption, league, start_date,
                                        end_date, number_of_teams, number_of_matches, current_matchday])+'\n')


def team_json2csv(Response):
    columns = ['betradar_id', 'league_id', 'name',
               'short_name', 'crest_url', 'team_abbreviation']
    league_id = Response['competition']['id']
    competition_code = Response['competition']['code']
    teams = Response['teams']
    with open(competition_code+"_teams.csv", "w") as cf:
        cf.writelines(','.join(columns)+"\n")
        for team in teams:
            ln = list()
            ln.append(team["id"])
            ln.append(league_id)
            ln.append(team["name"])
            ln.append(team["shortName"])
            ln.append(team["crestUrl"])
            ln.append(team["tla"])
            print(','.join(str(i) for i in ln))
            cf.writelines(str(','.join(str(i) for i in ln))+"\n")
        print("\t\tDone!")


def match_json2csv(Response):
    columns = ['match_id', 'match_date', 'match_time', 'home_team_id', 'home_team_name', 'away_team_id',
               'away_team_name', 'league_id', 'match_day', 'home_team_score', 'away_team_score', 'status', 'Winner']

    matches = Response['matches']
    # nmatches = len(matches)
    competition_code = Response['competition']['code']
    league_id = Response['competition']['id'].__str__()
    with open(competition_code+".csv", 'w') as cf:
        cf.writelines(','.join(columns)+"\n")
        for match in matches:
            ln = list()
            ln.append(match['id'])
            ln.append(str2date(match['utcDate'].split('T')[0]))
            ln.append(str2time(match['utcDate'].split('T')[1].split('Z')[0]))
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
    master_teams = pd.concat(dfs, axis=0).reset_index(drop=True)
    master_teams.to_csv("All_Teams.csv", index=False)
    return master_teams


def unify_matches_csv():
    match_csv = ["PL.csv", "BL1.csv", "SA.csv", "PD.csv", "CL.csv"]
    dfs = [pd.read_csv(fl) for fl in match_csv]
    master_fixtures = pd.concat(dfs, axis=0).reset_index(drop=True)
    master_fixtures.to_csv("All_Fixtures.csv", index=False)
    return master_fixtures


def unify_leagues_csv():
    match_csv = ["PL_leagues.csv", "BL1_leagues.csv",
                 "SA_leagues.csv", "PD_leagues.csv", "CL_leagues.csv"]
    dfs = [pd.read_csv(fl) for fl in match_csv]
    master_leagues = pd.concat(dfs, axis=0).reset_index(drop=True)
    master_leagues.to_csv("All_Leagues.csv", index=False)
    return master_leagues


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
