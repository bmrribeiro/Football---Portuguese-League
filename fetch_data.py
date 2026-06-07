import requests
import pandas as pd
import json
from dotenv import load_dotenv
import os
import time

load_dotenv()
API_KEY = os.getenv("API_KEY")


def fetch_data(url):
    headers = {"X-Auth-Token": API_KEY}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

'''
data_teams = fetch_data("https://api.football-data.org/v4/competitions/PPL/teams")
data_teams_2024 = fetch_data("https://api.football-data.org/v4/competitions/PPL/teams?season=2024")
data_teams_2023 = fetch_data("https://api.football-data.org/v4/competitions/PPL/teams?season=2023")
#print(data_teams)
#print(data_teams_2023)
#print(data_teams_2024)'''


'''data_matches = fetch_data("https://api.football-data.org/v4/competitions/PPL/matches")
data_matches_2024 = fetch_data("https://api.football-data.org/v4/competitions/PPL/matches?season=2024")
data_matches_2023 = fetch_data("https://api.football-data.org/v4/competitions/PPL/matches?season=2023")
#print(data_matches)
#print(data_matches_2023)
#print(data_matches_2024)'''


'''data_standings = fetch_data("https://api.football-data.org/v4/competitions/PPL/standings")
data_standings_2024 = fetch_data("https://api.football-data.org/v4/competitions/PPL/standings?season=2024")
data_standings_2023 = fetch_data("https://api.football-data.org/v4/competitions/PPL/standings?season=2023")'''

#SCORERS
'''
data_scorers = fetch_data("https://api.football-data.org/v4/competitions/PPL/scorers") #ONLY SHOWS TOP10
data_scorers_2024 = fetch_data("https://api.football-data.org/v4/competitions/PPL/scorers?season=2024")
data_scorers_2023 = fetch_data("https://api.football-data.org/v4/competitions/PPL/scorers?season=2023")
#print(data_scorers_2024)
    
season_year = data_scorers['filters']['season']
season_id = data_scorers['season']["id"]
season_start = data_scorers['season']["startDate"]
season_end = data_scorers['season']["endDate"]


df_scorers = pd.json_normalize(data_scorers['scorers'])

df_scorers = df_scorers.rename(columns={
    'id': 'season_id',
    
    'player.id': 'player_id',
    'player.name': 'player_name',
    'player.dateOfBirth': 'date_of_birth',
    'player.nationality': 'nationality',
    'player.section': 'position',
    'team.id': 'team_id',
    'team.name': 'team_name',
    'playedMatches': 'matches_played',
})

df_scorers["season_year"] = season_year
df_scorers['season_id'] = season_id
df_scorers['season_start'] = season_start
df_scorers['season_end'] = season_end

df_scorers = df_scorers.drop(columns=[col for col in df_scorers.columns if col.startswith("team.") or col.startswith("player.")], errors="ignore")

df_scorers = df_scorers[['season_id', 'season_year', 'season_start', 'season_end', 'player_id', 'player_name', 'nationality', 'date_of_birth', 'team_id', 'team_name', 'position', 'matches_played', 'goals', 'assists', 'penalties']]

print(df_scorers.head(10).T)
'''


'''
#data_teams treatment

#print(json.dumps(data_teams, indent=2)) #See the info I have access to - data from teams (players, coaches, etc)

#This is no longer necessary with what we did next, but I'll leave it for reference, in case you want to see what data_teams["teams"] consists of

df_teams = pd.json_normalize(data_teams["teams"])
df_teams = df_teams.drop(columns=[col for col in df_teams.columns if col.endswith("msg")], errors="ignore") #drop columns that end with "msg"
df_teams = df_teams[['id', 'name', 'squad']]
df_teams = pd.json_normalize(data_teams["teams"])[['id', 'name']]
'''

'''df_players = pd.json_normalize(
    data_teams["teams"],
    record_path="squad",
    meta=["id", "name"],
    meta_prefix="team_"
)
df_players = df_players.rename(columns={
    'id': 'player_id',
    'name': 'player_name',
    'dateOfBirth': 'date_of_birth',
})
#Put team_id and team_name at the beginning to facilitate reading
df_players = df_players[['team_id', 'team_name', 'player_id', 'player_name', 'position', 'date_of_birth', 'nationality']]
print(df_players.head())'''


#data_matches treatment
'''
print(json.dumps(data_matches, indent=2)) #see what info I have access to - data from matches (date, teams, score, etc)

df_matches = pd.json_normalize(data_matches["matches"])
   
df_matches = df_matches.drop(columns=[col for col in df_matches.columns if col.endswith("msg")], errors="ignore") #drop columns that end with "msg"
df_matches = df_matches[['id', 'utcDate', 'status', 'season.id', 'season.winner', 'homeTeam.id', 'homeTeam.name', 'awayTeam.id', 'awayTeam.name', 'score.winner', 'score.fullTime.home', 'score.fullTime.away']]
df_matches = df_matches.rename(columns={
    'id': 'match_id',
    'utcDate': 'date_match',
    'season.id': 'season_id',
    'season.winner': 'season_winner',
    'homeTeam.id': 'home_team_id',
    'homeTeam.name': 'home_team',
    'awayTeam.id': 'away_team_id',
    'awayTeam.name': 'away_team',
    'score.winner': 'winner',
    'score.fullTime.home': 'home_goals',
    'score.fullTime.away': 'away_goals'
})
print(df_matches.head())'''



'''#I don't know this API, so I want to confirm if the team IDs are correct. From what I see, they are, nothing to worry about.
players_teams = set(df_players["team_id"].unique()) #set is a collection of unique values, without repetitions (automatically removes duplicates)
matches_home = set(df_matches["home_team_id"].unique())
matches_away = set(df_matches["away_team_id"].unique())
matches_teams = matches_home.union(matches_away) #Put toghether home with away, removing duplicates
print(matches_teams.issubset(players_teams)) #Verifies if all elements of matches_teams are in players_teams (True if so, False otherwise)
print(players_teams.issubset(matches_teams))

#Do the same for the names, this serves for later to perform a merge
players_teams = set(df_players["team_name"].unique())
matches_home = set(df_matches["home_team"].unique())
matches_away = set(df_matches["away_team"].unique())
matches_teams = matches_home.union(matches_away)
print(matches_teams.issubset(players_teams))
print(players_teams.issubset(matches_teams))'''


#Optimization of what I did previously, keep what is behind in comments to see learning and also to have an idea of how to analyze this API

#Matches final - The same as behind, but optimized and for the available seasons (2025, 2024 and 2023)

def process_matches(data):
    df = pd.json_normalize(data["matches"])
    
    # Remove unneecessary columns 
    df = df.drop(columns=[col for col in df.columns if col.endswith("msg")], errors="ignore")
    
    # Select relevant columns
    df = df[['id', 'utcDate', 'status', 'season.id', 'season.winner',
             'homeTeam.id', 'homeTeam.name', 'awayTeam.id', 'awayTeam.name',
             'score.winner', 'score.fullTime.home', 'score.fullTime.away']]
    
    # Rename columns
    df = df.rename(columns={
        'id': 'match_id',
        'utcDate': 'date_match',
        'season.id': 'season_id',
        'season.winner': 'season_winner',
        'homeTeam.id': 'home_team_id',
        'homeTeam.name': 'home_team',
        'awayTeam.id': 'away_team_id',
        'awayTeam.name': 'away_team',
        'score.winner': 'winner',
        'score.fullTime.home': 'home_goals',
        'score.fullTime.away': 'away_goals'
    })
    
    return df

# Seasons to fetch
seasons = [2023, 2024, 2025]

dfs = []

for season in seasons:
    url = f"https://api.football-data.org/v4/competitions/PPL/matches?season={season}"
    data = fetch_data(url)
    df = process_matches(data)
    dfs.append(df)
    time.sleep(6)

# Put all DataFrames together into a single DataFrame
df_matches = pd.concat(dfs, ignore_index=True)

# Transform the winner column to show the name of the winning team instead of HOME_TEAM, AWAY_TEAM (Done after constructing the Database)
# Uncomment when you have the update script ready, to avoid having to do updates later)
df_matches['winner'] = df_matches.apply(lambda row: row['home_team'] if row['winner'] == 'HOME_TEAM'
                                        else row['away_team'] if row['winner'] == 'AWAY_TEAM'
                                        else 'Draw', axis=1)

print("\nMatches")
print(df_matches.head())


#Teams final - The same as behind, but optimized and for the available seasons (2025, 2024 and 2023)

def process_teams(data, season=None):
    df = pd.json_normalize(data["teams"])
    
    df = df.drop(columns=[col for col in df.columns if col.endswith("msg")], errors="ignore")
    df = df[['id', 'name']]
    
    df = df.rename(columns={
        'id': 'team_id',
        'name': 'team_name'
    })
    
    if season:
        df["season"] = season
        
    return df


def process_players(data, season=None):
    df = pd.json_normalize(
        data["teams"],
        record_path="squad",
        meta=["id", "name"],
        meta_prefix="team_"
    )
    
    df = df.rename(columns={
        'id': 'player_id',
        'name': 'player_name',
        'dateOfBirth': 'date_of_birth',
    })
    
    df = df[['team_id', 'team_name', 'player_id', 'player_name',
             'position', 'date_of_birth', 'nationality']]
    
    if season:
        df["season"] = season
        
    return df
    
#Loop for all seasons

seasons = [2025, 2024, 2023]

teams_list = []
players_list = []

for season in seasons:
    url = f"https://api.football-data.org/v4/competitions/PPL/teams?season={season}"
    data = fetch_data(url)
    
    df_teams = process_teams(data, season)
    df_players = process_players(data, season)
    
    teams_list.append(df_teams)
    players_list.append(df_players)
    time.sleep(6)
# Concatenate eveything
df_teams = pd.concat(teams_list, ignore_index=True)
df_players = pd.concat(players_list, ignore_index=True)

#Remove duplicates and keep the teams that are repeated by the most recent season (to create Primary Key)
df_teams = df_teams.sort_values('season', ascending=False).drop_duplicates(subset=['team_id'], keep='first')

print("\nTeams")
print(df_teams.head())
print("\nPlayers")
print(df_players.tail())

#Standings works differently:
#The data for the table is nested within standings[0]["table"] because the API returns a list with three types of standings (TOTAL, HOME, AWAY). 
#The TOTAL is at index 0. 


def process_standings(data):
    season_info = data["season"]
    season_id = season_info["id"]
    season_start_date = season_info["startDate"]
    season_end_date = season_info["endDate"]
    season_winner = season_info["winner"]
    
    df_standings = pd.json_normalize(data['standings'][0]['table'])
 
    df_standings = df_standings.rename(columns={
        'team.id': 'team_id',
        'team.name': 'team_name',
        'playedGames': 'games_played',
   		'goalsFor': 'goals_scored',
   		'goalsAgainst': 'goals_suffered',
    	'goalDifference': 'goal_difference'
    })

    df_standings['season_id'] = season_id
    df_standings['season_start_date']= season_start_date
    df_standings['season_end_date'] = season_end_date
    df_standings['season_winner'] = season_winner

    df_standings = df_standings.drop(columns= [col for col in df_standings.columns if col.startswith("team.") or col == "form"], errors="ignore")
    #Put in desired order
    df_standings = df_standings[['season_id', 'season_start_date', 'season_end_date', 'season_winner', 'position', 'team_id', 'team_name', 'points', 'games_played', 'won', 'draw', 'lost', 'goals_scored', 'goals_suffered', 'goal_difference']]
    return df_standings


seasons=[2023, 2024, 2025]
dfs=[]

for season in seasons:
    url = f"https://api.football-data.org/v4/competitions/PPL/standings?season={season}"
    data = fetch_data(url)
    df = process_standings(data)
    dfs.append(df)
    time.sleep(6)

df_standings = pd.concat(dfs, ignore_index=True)

print("\nStandings")
print(df_standings.head())


#Optimization of scorers


def process_scorers(data):
    season_year = data['filters']['season']
    season_id = data['season']["id"]
    season_start = data['season']["startDate"]
    season_end = data['season']["endDate"]


    df_scorers = pd.json_normalize(data['scorers'])

    df_scorers = df_scorers.rename(columns={
        'id': 'season_id',
        'player.id': 'player_id',
        'player.name': 'player_name',
        'player.dateOfBirth': 'date_of_birth',
        'player.nationality': 'nationality',
        'player.section': 'position',
        'team.id': 'team_id',
        'team.name': 'team_name',
        'playedMatches': 'matches_played',
    })

    df_scorers["season_year"] = season_year
    df_scorers['season_id'] = season_id
    df_scorers['season_start'] = season_start
    df_scorers['season_end'] = season_end

    df_scorers = df_scorers.drop(columns=[col for col in df_scorers.columns if col.startswith("team.") or col.startswith("player.")], errors="ignore")

    df_scorers = df_scorers[['season_id', 'season_year', 'season_start', 'season_end', 'player_id', 'player_name', 'nationality', 'date_of_birth', 'team_id', 'team_name', 'position', 'matches_played', 'goals', 'assists', 'penalties']]
    return df_scorers

seasons=[2023, 2024, 2025]
dfs=[]

for season in seasons:
    url = f"https://api.football-data.org/v4/competitions/PPL/scorers?season={season}"
    data = fetch_data(url)
    df = process_scorers(data)
    dfs.append(df)
    time.sleep(7)
    
df_scorers = pd.concat(dfs, ignore_index=True)

df_scorers = df_scorers.sort_values(
    by=['season_year', 'goals'],
    ascending=[True, False]
).reset_index(drop=True)

print("\nTop 10 scorers:")
print(df_scorers.head())

df_matches.to_csv("data/matches.csv", index=False)
df_standings.to_csv("data/standings.csv", index=False)
df_scorers.to_csv("data/scorers.csv", index=False)
df_teams.to_csv("data/teams.csv", index=False)
df_players.to_csv("data/players.csv", index=False)
