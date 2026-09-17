# Keep only regular-season games
schedule = schedule[schedule["game_type"] == "REG"].copy()
team_stats = team_stats[team_stats["season_type"] == "REG"].copy()

print("Schedule shape:", schedule.shape)
print("Team stats shape:", team_stats.shape)

# Remove Week 1 because there are no previous 2025 games
schedule = schedule[schedule["week"] > 1].copy()
team_stats = team_stats[team_stats["week"] > 1].copy()

print("Schedule shape:", schedule.shape)
print("Team stats shape:", team_stats.shape)

# Create one row for each team in each game

home_games = schedule[
    ["game_id", "season", "week", "home_team", "away_team",
     "home_score", "away_score"]
].copy()

home_games = home_games.rename(columns={
    "home_team": "team",
    "away_team": "opponent",
    "home_score": "points_for",
    "away_score": "points_against"
})

away_games = schedule[
    ["game_id", "season", "week", "away_team", "home_team",
     "away_score", "home_score"]
].copy()

away_games = away_games.rename(columns={
    "away_team": "team",
    "home_team": "opponent",
    "away_score": "points_for",
    "home_score": "points_against"
})

team_games = pd.concat(
    [home_games, away_games],
    ignore_index=True
)

# Calculate game-level performance

team_games["win"] = (
    team_games["points_for"] > team_games["points_against"]
).astype(int)

team_games["point_differential"] = (
    team_games["points_for"]
    - team_games["points_against"]
)

team_games = team_games.sort_values(
    ["team", "week"]
).reset_index(drop=True)

# Calculate the number of games played before each game
team_games["games_before"] = (
    team_games.groupby("team").cumcount()
)

# Calculate cumulative performance before the current game
team_games["wins_before"] = (
    team_games.groupby("team")["win"].cumsum()
    - team_games["win"]
)

team_games["points_scored_before"] = (
    team_games.groupby("team")["points_for"].cumsum()
    - team_games["points_for"]
)

team_games["points_allowed_before"] = (
    team_games.groupby("team")["points_against"].cumsum()
    - team_games["points_against"]
)

team_games["point_diff_before"] = (
    team_games.groupby("team")["point_differential"].cumsum()
    - team_games["point_differential"]
)

# Convert cumulative totals into pregame averages

team_games["win_pct_before"] = (
    team_games["wins_before"]
    / team_games["games_before"]
)

team_games["avg_points_scored_before"] = (
    team_games["points_scored_before"]
    / team_games["games_before"]
)

team_games["avg_points_allowed_before"] = (
    team_games["points_allowed_before"]
    / team_games["games_before"]
)

team_games["avg_point_diff_before"] = (
    team_games["point_diff_before"]
    / team_games["games_before"]
)

# Remove games where the team had no previous games
team_games = team_games[
    team_games["games_before"] > 0
].copy()

# Check for missing values
print(model_data[
    [
        "spread_line",
        "win_pct_diff",
        "points_scored_diff",
        "points_allowed_diff",
        "point_diff_diff"
    ]
].isna().sum())

spread_line             0
win_pct_diff            0
points_scored_diff      0
points_allowed_diff     0
point_diff_diff         0

# Check for duplicate games
print("Number of rows:", len(model_data))
print("Number of unique games:", model_data["game_id"].nunique())
print("Number of duplicate rows:", model_data.duplicated().sum())

Number of rows: 240
Number of unique games: 240
Number of duplicate rows: 0
