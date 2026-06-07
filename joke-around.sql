USE football_portugal;

-- TOTAL NUMBER OF MATCHES PLAYED BY EACH TEAM IN THE 2025 SEASON 

SELECT team_name, games_played FROM standings WHERE season_id=2433 ORDER BY games_played ASC;

-- TEAMS THAT SCORED MORE THAN 50 GOALS IN THE 2025 SEASON
SELECT team_name, goals_scored FROM standings WHERE goals_scored > 50 AND YEAR(season_start_date) = 2025 ORDER BY goals_scored DESC; -- or use season_id=2433

-- HOW MANY PLAYERS FROM EACH NATIONALITY ARE IN THE DATABASE? I DID THIS FOR THE 2025 SEASON AND ADDED A PERCENTAGE

SELECT nationality, COUNT(*) AS country_representation, ROUND(100 * COUNT(*) / SUM(COUNT(*)) OVER(), 2) AS percentage FROM players WHERE season=2025 GROUP BY nationality ORDER BY country_representation DESC;

-- WHAT IS THE PERFORMANCE OF FC PORTO (id=503), SPORTING (id=498) AND BENFICA (id=1903) AT HOME VS AWAY IN THE 2025/2026 SEASON (WINS, DRAWS, DEFEATS)? 

SELECT * FROM matches;

SELECT 
    h.team,
    h.wins AS home_wins,
    h.draws AS home_draws,
    h.losses AS home_losses,
    a.wins AS away_wins,
    a.draws AS away_draws,
    a.losses AS away_losses
FROM (
    SELECT 
        home_team AS team,
        SUM(CASE WHEN winner = home_team THEN 1 ELSE 0 END) AS wins,
        SUM(CASE WHEN winner = 'Draw' THEN 1 ELSE 0 END) AS draws,
        SUM(CASE WHEN winner != home_team AND winner != 'Draw' THEN 1 ELSE 0 END) AS losses
    FROM matches
    WHERE status = 'FINISHED'
    -- AND home_team IN ('FC Porto', 'Sporting Clube de Portugal', 'Sport Lisboa e Benfica')
    AND season_id = 2433
    GROUP BY home_team
) h
JOIN (
    SELECT 
        away_team AS team,
        SUM(CASE WHEN winner = away_team THEN 1 ELSE 0 END) AS wins,
        SUM(CASE WHEN winner = 'Draw' THEN 1 ELSE 0 END) AS draws,
        SUM(CASE WHEN winner != away_team AND winner != 'Draw' THEN 1 ELSE 0 END) AS losses
    FROM matches
    WHERE status = 'FINISHED'
    -- AND away_team IN ('FC Porto', 'Sporting Clube de Portugal', 'Sport Lisboa e Benfica'
    AND season_id = 2433
    GROUP BY away_team
) a ON h.team = a.team
ORDER BY h.wins DESC;

-- WHAT ARE THE TEAMS THAT IMPROVED THEIR POSITION IN THE LEAGUE BETWEEN 2023 AND 2025 (2023=1603; 2024=2312; 2025=2433)?

-- SELECT DISTINCT season_id, season_start_date FROM standings; 
-- This shows only the teams that were present in all three seasons:
SELECT * FROM standings; 

SELECT
    s2023.team_name,
    s2023.position AS position_2023,
    s2024.position AS position_2024,
    s2025.position AS position_2025,
    s2023.position - s2024.position AS improvement_2023_2024,
    s2024.position - s2025.position AS improvement_2024_2025
FROM standings s2023
JOIN standings s2024 ON s2023.team_id = s2024.team_id
JOIN standings s2025 ON s2024.team_id = s2025.team_id
WHERE s2023.season_id = 1603
AND s2024.season_id = 2312
AND s2025.season_id = 2433
ORDER BY improvement_2024_2025 DESC;

/* This shows the teams that were present in all three seasons, it is necessary to do a union for each season

SELECT
    COALESCE(s2023.team_name, s2024.team_name, s2025.team_name) AS team_name,
    s2023.position AS position_2023,
    s2024.position AS position_2024,
    s2025.position AS position_2025,
    s2023.position - s2024.position AS improvement_2023_2024,
    s2024.position - s2025.position AS improvement_2024_2025
FROM (SELECT * FROM standings WHERE season_id = 1603) s2023
LEFT JOIN (SELECT * FROM standings WHERE season_id = 2312) s2024 ON s2023.team_id = s2024.team_id
LEFT JOIN (SELECT * FROM standings WHERE season_id = 2433) s2025 ON s2024.team_id = s2025.team_id

UNION

SELECT
    COALESCE(s2023.team_name, s2024.team_name, s2025.team_name) AS team_name,
    s2023.position AS position_2023,
    s2024.position AS position_2024,
    s2025.position AS position_2025,
    s2023.position - s2024.position AS improvement_2023_2024,
    s2024.position - s2025.position AS improvement_2024_2025
FROM (SELECT * FROM standings WHERE season_id = 2312) s2024
LEFT JOIN (SELECT * FROM standings WHERE season_id = 1603) s2023 ON s2024.team_id = s2023.team_id
LEFT JOIN (SELECT * FROM standings WHERE season_id = 2433) s2025 ON s2024.team_id = s2025.team_id

UNION

SELECT
    COALESCE(s2023.team_name, s2024.team_name, s2025.team_name) AS team_name,
    s2023.position AS position_2023,
    s2024.position AS position_2024,
    s2025.position AS position_2025,
    s2023.position - s2024.position AS improvement_2023_2024,
    s2024.position - s2025.position AS improvement_2024_2025
FROM (SELECT * FROM standings WHERE season_id = 2433) s2025
LEFT JOIN (SELECT * FROM standings WHERE season_id = 2312) s2024 ON s2025.team_id = s2024.team_id
LEFT JOIN (SELECT * FROM standings WHERE season_id = 1603) s2023 ON s2024.team_id = s2023.team_id

ORDER BY improvement_2023_2024 DESC; */ 

-- WHAT IS THE MEAN OF GOALS PER MATCH IN EACH SEASON?

-- SELECT * FROM matches;

SELECT 
    season_id,
    ROUND(AVG(home_goals + away_goals), 2) AS avg_goals_per_match
FROM matches
WHERE status = 'FINISHED'
GROUP BY season_id
ORDER BY season_id;


-- WHAT ARE THE PLAYERS THAT SCORED IN MORE THAN ONE SEASON?

SELECT * FROM scorers;

SELECT player_name, COUNT(DISTINCT season_id) AS seasons_scored, SUM(goals) AS golos_total
FROM scorers
GROUP BY player_name
HAVING seasons_scored > 1
ORDER BY golos_total DESC; 

-- WHICH TEAM HAS THE BEST DEFENSE (FEWEST GOALS ALLOWED) IN EACH SEASON? 

SELECT * FROM standings;

SELECT s.season_id, s.team_name, s.goals_suffered
FROM standings s
JOIN (
    SELECT season_id, MIN(goals_suffered) AS min_goals
    FROM standings
    GROUP BY season_id
) min_per_season ON s.season_id = min_per_season.season_id 
AND s.goals_suffered = min_per_season.min_goals
ORDER BY s.season_id;

-- WHAT IS THE TOP 5 OF GAMES WITH THE MOST GOALS SCORED IN TOTAL? 

SELECT match_id, date_match, season_id, home_team, away_team, home_goals + away_goals AS total_goals
FROM matches
WHERE status = 'FINISHED'
ORDER BY total_goals DESC, date_match ASC
LIMIT 5; 

-- RANKING OF TEAMS BY POINTS PER GAME (POINTS / GAMES PLAYED).
SELECT * FROM standings;

SELECT team_name, ROUND(SUM(points) / SUM(games_played), 2) AS ratio_points_games
FROM standings
GROUP BY team_name
ORDER BY ratio_points_games DESC;
