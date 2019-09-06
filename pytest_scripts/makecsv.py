#!/usr/bin/env python3.7

from get import Response

columns = ['Date','Time','HTID','HomeTeam','ATID','AwayTeam','HTHG','HTAG','FTHG','FTAG','Goals','Winner']

matches=Response['matches']
nmatches=len(matches)
competition_code=Response['competition']['code']

with open(competition_code+".csv",'w') as cf:
    cf.writelines('\t'.join(columns)+"\n")
    for match in matches:
        ln=[]
        ln.append(match['utcDate'].split('T')[0])
        ln.append(match['utcDate'].split('T')[1].split('Z')[0])
        ln.append(match['homeTeam']['id'].__str__())
        ln.append(match['homeTeam']['name'])
        ln.append(match['awayTeam']['id'].__str__())
        ln.append(match['awayTeam']['name'])
        ln.append(match['score']['halfTime']['homeTeam'].__str__())
        ln.append(match['score']['halfTime']['awayTeam'].__str__())
        ln.append(match['score']['fullTime']['homeTeam'].__str__())
        ln.append(match['score']['fullTime']['awayTeam'].__str__())
        if not isinstance(match['score']['fullTime']['homeTeam'],int):
            ln.append('')
        else:
            ln.append(str(match['score']['fullTime']['awayTeam']+match['score']['fullTime']['homeTeam']))
        ln.append(match['score']['winner'].__str__())
        print('\t'.join(ln))
        cf.writelines(str('\t'.join(ln))+"\n")
    print("\t\tDone!")
cf.close()



