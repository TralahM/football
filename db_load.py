from fetch_matches import *
# unify_leagues_csv()
# unify_matches_csv()
teams = unify_teams_csv()
update_db_teams(teams)
