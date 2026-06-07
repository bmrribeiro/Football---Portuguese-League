
-- DATA TREATMENT - RELATIONS

USE football_portugal;

-- Primary Keys

ALTER TABLE teams
ADD PRIMARY KEY (team_id);

ALTER TABLE matches
ADD PRIMARY KEY (match_id);

ALTER TABLE standings
ADD PRIMARY KEY (season_id, team_id);

ALTER TABLE players
ADD PRIMARY KEY (player_id, season);

ALTER TABLE scorers
ADD PRIMARY KEY (player_id, season_id);


-- FOREIGN KEYS - RELATIONS

ALTER TABLE matches
ADD FOREIGN KEY (home_team_id) REFERENCES teams(team_id),
ADD FOREIGN KEY (away_team_id) REFERENCES teams(team_id);

ALTER TABLE standings
ADD FOREIGN KEY (team_id) REFERENCES teams(team_id);

ALTER TABLE players
ADD FOREIGN KEY (team_id) REFERENCES teams(team_id);

ALTER TABLE scorers
ADD FOREIGN KEY (team_id) REFERENCES teams(team_id);


