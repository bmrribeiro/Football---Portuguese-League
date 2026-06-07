import mysql.connector
from dotenv import load_dotenv
from pathlib import Path
import os
import pandas as pd
from sqlalchemy import create_engine

load_dotenv(dotenv_path=Path(__file__).parent / ".env")

DB_HOST = os.getenv("DB_HOST")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# DELETE AND CREATE DATABASE
conn = mysql.connector.connect(
    host=DB_HOST,
    user="root",
    password=DB_PASSWORD
)
cursor = conn.cursor()
cursor.execute("DROP DATABASE IF EXISTS football_portugal")
cursor.execute("CREATE DATABASE football_portugal")
cursor.close()
conn.close()

# Engine
engine = create_engine(
    f"mysql+mysqlconnector://root:{DB_PASSWORD}@{DB_HOST}/football_portugal"
)

# READ CSVs
df_teams = pd.read_csv("data/teams.csv")
df_players = pd.read_csv("data/players.csv")
df_matches = pd.read_csv("data/matches.csv")
df_standings = pd.read_csv("data/standings.csv")
df_scorers = pd.read_csv("data/scorers.csv")

# LOAD DATA TO DATABASE
df_teams.to_sql("teams", con=engine, if_exists="replace", index=False)
df_players.to_sql("players", con=engine, if_exists="replace", index=False)
df_matches.to_sql("matches", con=engine, if_exists="replace", index=False)
df_standings.to_sql("standings", con=engine, if_exists="replace", index=False)
df_scorers.to_sql("scorers", con=engine, if_exists="replace", index=False)

print("Data loaded successfully!")