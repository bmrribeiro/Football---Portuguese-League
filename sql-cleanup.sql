-- DATA CLEANUP - removal of NULL values

DELETE FROM teams WHERE team_id IS NULL;
ALTER TABLE standings DROP COLUMN season_winner;
ALTER TABLE matches DROP COLUMN season_winner;