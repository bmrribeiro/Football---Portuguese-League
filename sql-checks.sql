-- Verifying season_winner in 'standings' and 'matches' tables

SELECT DISTINCT season_winner FROM standings;
SELECT DISTINCT season_winner FROM matches;

-- Verifying rows with NULL values in the 'teams' table
SELECT * FROM teams WHERE team_id IS NULL OR team_name IS NULL;