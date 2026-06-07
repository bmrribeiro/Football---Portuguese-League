# Data Analysis - An overview of the Portuguese Football League

A complete Data Analysis project covering all phases of a hybrid ELT pipeline, built from scratch using Python, MySQL, and Power BI.

**Data source:** [football-data.org](https://www.football-data.org/) API  
**Season coverage:** 2023/24, 2024/25, 2025/26

---

## What is this project?

This project analyses three seasons of the Portuguese League data, covering match results, standings, top scorers, and squad composition across 18 clubs per season.

This was primarily a learning project — built to develop and consolidate skills across the full data analyst stack. As a result, `fetch_data.py` contains extensive comments documenting the exploratory process: understanding the API structure, inspecting raw JSON responses, and iterating on data processing logic. These comments were left intentionally to show the learning process and the reasoning behind each decision.

---

## Dashboard Preview

<table>
  <tr>
    <td align="center"><b>📊 League Overview</b></td>
  </tr>
  <tr>
    <td><a href="https://github.com/bmrribeiro/Football---Portuguese-League/blob/main/PB1.png" target="_blank"><img width="100%" src="https://raw.githubusercontent.com/bmrribeiro/Football---Portuguese-League/main/PB1.png" alt="League Overview" /></a></td>
  </tr>
  <tr>
    <td>Season-level KPIs: standings, top scorers, home/away/draw percentages, biggest wins and highest scoring games.</td>
  </tr>
</table>

<table>
  <tr>
    <td align="center"><b>🏟️ Team Overview</b></td>
  </tr>
  <tr>
    <td><a href="https://github.com/bmrribeiro/Football---Portuguese-League/blob/main/PB2.png" target="_blank"><img width="100%" src="https://raw.githubusercontent.com/bmrribeiro/Football---Portuguese-League/main/PB2.png" alt="Team Overview" /></a></td>
  </tr>
  <tr>
    <td>Per-team analysis: home/away performance, recent form with visual indicators, attack and defense ratings, and an overall team rating.</td>
  </tr>
</table>

<table>
  <tr>
    <td align="center"><b>🌍 Players</b></td>
  </tr>
  <tr>
    <td><a href="https://github.com/bmrribeiro/Football---Portuguese-League/blob/main/PB3.png" target="_blank"><img width="100%" src="https://raw.githubusercontent.com/bmrribeiro/Football---Portuguese-League/main/PB3.png" alt="Players" /></a></td>
  </tr>
  <tr>
    <td>Squad nationality analysis: player count and percentage representation by nationality, filterable by season and team.</td>
  </tr>
</table>

---

## Why this project?

I enjoy football and I support Sporting Clube de Portugal, and that was the main the reason to engage on this project, something I can relate. 

The data comes from the free tier of the [football-data.org](https://www.football-data.org/) API, which imposes limitations worth noting:

- **Rate limit:** 10 requests per minute — handled with `time.sleep(6)` between calls
- **Historical access:** limited to the last 3 seasons - not enough data for accurate prediction models
- **No match-level statistics:** possession, shots, passes — unavailable at the free tier
- **Incomplete fields:** some fields (e.g. `season_winner`) return null and were removed during data cleaning

These constraints shaped the scope of the project and are reflected in the pipeline design.

---

## Pipeline Overview — Hybrid ELT

The pipeline follows a hybrid ELT approach — *Extract, Load, Transform* — where transformation happens at multiple stages rather than all at once before loading:

| Stage | Tool | Description |
|---|---|---|
| **Extract** | Python + Requests | Fetch data from REST API |
| **Load** | Python + SQLAlchemy | Load raw data into MySQL |
| **Transform (SQL)** | MySQL | Schema design, PKs, FKs, data cleaning |
| **Transform (DAX)** | Power BI | Measures, calculated columns, KPIs |

This is called *hybrid* because transformation happens both in Python (column selection, renaming, type casting) and after loading (SQL and DAX).

On each pipeline run, the database is dropped and recreated from scratch to avoid duplicate data. Primary and foreign keys are automatically reapplied after loading via `sql-schema.sql`, followed by data cleanup via `sql-cleanup.sql`. The entire pipeline is orchestrated by `run_pipeline.py` and runs automatically via Windows Task Scheduler (weekly).

---

## Database Design — Star Schema

The database follows a star schema design:

- **Fact tables** (large, transactional): `matches`, `standings`, `scorers`
- **Dimension tables** (descriptive): `teams`, `players`, `seasons`

The `seasons` table was created manually in Power BI.

Relationships were defined in MySQL using primary keys and foreign keys, then re-established in Power BI's model view. The relationship between `teams` and `matches` is split into two:

- `teams[team_id] → matches[home_team_id]` (active)
- `teams[team_id] → matches[away_team_id]` (inactive, activated via DAX where needed)

---

## Credentials & Security

API keys and database credentials are stored in a local `.env` file and read via `python-dotenv`. This file is not included in the repository — credentials never appear in the source code. 

A free API key can be obtained at [football-data.org](https://www.football-data.org/).

---

## File Structure

| File | Description |
|---|---|
| `fetch_data.py` | Connects to the API, processes and exports data to CSV. Contains extensive comments documenting the exploratory process of understanding the API structure |
| `database.py` | Drops and recreates the database, reads CSVs, and loads data into MySQL via SQLAlchemy |
| `run_pipeline.py` | Orchestrates the full pipeline: reset DB, fetch data, load data, apply SQL schema and cleanup |
| `sql-schema.sql` | Defines primary keys and foreign keys — reapplied automatically on each pipeline run |
| `sql-cleanup.sql` | Removes null rows and drops unused columns |
| `sql-checks.sql` | Verification queries — run manually in Workbench when needed, not part of the automated pipeline |
| `joke-around.sql` | SQL analysis queries written for portfolio demonstration |
| `LigaPortugalBetclic.pbix` | Power BI report file |
| `data/` | CSV exports from the API (one file per table) |

---

## Python — Data Extraction & Loading

Data is fetched from five API endpoints per season (`/matches`, `/standings`, `/teams`, `/scorers`, `/players`), resulting in 11 API calls per pipeline run. The free tier only allows me 10 requests per minute, that is why I use "time.sleep(6)" in each call.

Data is loaded into MySQL using `SQLAlchemy`. The database is dropped and recreated on each run, so there are no conflicts with existing foreign key constraints during loading. PKs and FKs are reapplied afterwards by `run_pipeline.py`.

---

## SQL — Schema & Analysis

Primary and foreign keys were defined after loading to enforce referential integrity across the schema:

```sql
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
```

The joke-around.sql file consists of some exercises that I made to myself to practice SQL queries and to be more familiar with the Database.


---

## Power BI — Dashboard

The report has three pages, all filterable by season:

**Page 1 — League Overview:** Season-level KPIs: total games, total goals, goals per game, home/away/draw percentages, best and worst attack/defense teams, biggest wins, highest scoring games, top scorers with assists, and the full league standings table.

**Page 2 — Team Overview:** Per-team analysis filtered by season and team: games played, home/away wins, losses and draws, goals scored and conceded, recent form (last 5 results with visual indicators 🟢⚪🔴), biggest win, attack and defense ratings.

**Page 3 — Players:** League and squad nationality analysis: player count and percentage representation by nationality, filterable by season and team.

---

## What I learned

This was primarily a learning project, built to develop and consolidate skills across the full data analyst stack — not just follow a course exercise.

**Python:** Working with a REST API taught me to handle rate limits, normalise nested JSON, and build reusable processing functions. The exploratory phase — understanding the API structure, inspecting raw responses, iterating on processing logic — is documented in the comments throughout `fetch_data.py`. The automated pipeline means this project could be maintained in a professional context with minimal effort.

**SQL:** Designing a relational schema from scratch — deciding on primary keys, foreign keys, and table granularity — taught me to think about data structure before writing queries. I have learnt about JOINS and UNION in the exploratory analysis queries which was challenging.

**Power BI / DAX:** This was the most challenging seeing that I self-taught myself on PowerBI. But I feel confident that I can now make better reports than before :D


---

## Tech Stack

![Python](https://img.shields.io/badge/Python-3.14-blue)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange)
![Power BI](https://img.shields.io/badge/Power%20BI-Desktop-yellow)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.x-red)
![pandas](https://img.shields.io/badge/pandas-2.x-lightblue)
