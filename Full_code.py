import nflreadpy as nfl

# Load 2025 NFL schedule data
schedule = nfl.load_schedules(2025)

# Load 2025 weekly team statistics
team_stats = nfl.load_team_stats(2025, summary_level="week")

print("Schedule rows:", schedule.height)
print("Schedule columns:", schedule.width)

print("Team stats rows:", team_stats.height)
print("Team stats columns:", team_stats.width)

print("\nSchedule columns:")
print(schedule.columns)

print("\nTeam stats columns:")
print(team_stats.columns)

print(schedule.null_count())

# Calculate the difference between home and away team performance

model_data["win_pct_diff"] = (
    model_data["home_win_pct"] - model_data["away_win_pct"]
)

model_data["points_scored_diff"] = (
    model_data["home_avg_points_scored"]
    - model_data["away_avg_points_scored"]
)

model_data["points_allowed_diff"] = (
    model_data["home_avg_points_allowed"]
    - model_data["away_avg_points_allowed"]
)

model_data["point_diff_diff"] = (
    model_data["home_avg_point_diff"]
    - model_data["away_avg_point_diff"]
)

# Check the new variables
print(model_data[
    [
        "game_id",
        "spread_line",
        "win_pct_diff",
        "points_scored_diff",
        "points_allowed_diff",
        "point_diff_diff"
    ]
].head())

# Summary statistics for the variables in our model
print(model_data[
    [
        "spread_line",
        "win_pct_diff",
        "points_scored_diff",
        "points_allowed_diff",
        "point_diff_diff"
    ]
].describe())

import statsmodels.api as sm

# Select our predictor variables
X = model_data[
    [
        "win_pct_diff",
        "points_scored_diff",
        "points_allowed_diff"
    ]
]

# Add an intercept to the model
X = sm.add_constant(X)

# Select our outcome variable
y = model_data["spread_line"]

# Fit the multiple linear regression
model = sm.OLS(y, X).fit()

# Display the results
print(model.summary())

print(team_stats.null_count())

print(schedule.null_count().to_pandas().T)

schedule = schedule.to_pandas()
team_stats = team_stats.to_pandas()

print("Schedule shape:", schedule.shape)
print("Team stats shape:", team_stats.shape)

# Keep only regular-season games
schedule = schedule[schedule["game_type"] == "REG"].copy()

# Keep only regular-season team statistics
team_stats = team_stats[team_stats["season_type"] == "REG"].copy()

# Check the new sizes
print("Schedule shape:", schedule.shape)
print("Team stats shape:", team_stats.shape)

print(schedule[schedule["week"] == 1][
    ["game_id", "away_team", "home_team", "spread_line"]
])

# Remove Week 1 because there are no previous 2025 games
schedule = schedule[schedule["week"] > 1].copy()
team_stats = team_stats[team_stats["week"] > 1].copy()

print("Schedule shape:", schedule.shape)
print("Team stats shape:", team_stats.shape)

# Create the home team's game information
home_games = schedule[
    ["game_id", "season", "week", "home_team", "away_team", "home_score", "away_score"]
].copy()

home_games = home_games.rename(columns={
    "home_team": "team",
    "away_team": "opponent",
    "home_score": "points_for",
    "away_score": "points_against"
})

# Create the away team's game information
away_games = schedule[
    ["game_id", "season", "week", "away_team", "home_team", "away_score", "home_score"]
].copy()

away_games = away_games.rename(columns={
    "away_team": "team",
    "home_team": "opponent",
    "away_score": "points_for",
    "home_score": "points_against"
})

# Put the home and away games together
team_games = pd.concat([home_games, away_games], ignore_index=True)

print("Team-game shape:", team_games.shape)
print(team_games.head())

# Create a win variable
team_games["win"] = (
    team_games["points_for"] > team_games["points_against"]
).astype(int)

# Create point differential
team_games["point_differential"] = (
    team_games["points_for"] - team_games["points_against"]
)

# Check the results
print(team_games[
    ["team", "opponent", "points_for", "points_against", "win", "point_differential"]
].head(10))

# Sort by team and then by week
team_games = team_games.sort_values(
    ["team", "week"]
).reset_index(drop=True)

# Check the first few rows
print(team_games.head(10))

# Calculate the number of previous games for each team
team_games["games_before"] = (
    team_games.groupby("team").cumcount()
)

# Calculate cumulative wins from previous games
team_games["wins_before"] = (
    team_games.groupby("team")["win"].cumsum() - team_games["win"]
)

# Calculate cumulative points scored before the current game
team_games["points_scored_before"] = (
    team_games.groupby("team")["points_for"].cumsum() 
    - team_games["points_for"]
)

# Calculate cumulative points allowed before the current game
team_games["points_allowed_before"] = (
    team_games.groupby("team")["points_against"].cumsum()
    - team_games["points_against"]
)

# Calculate cumulative point differential before the current game
team_games["point_diff_before"] = (
    team_games.groupby("team")["point_differential"].cumsum()
    - team_games["point_differential"]
)

# Convert the totals into averages
team_games["win_pct_before"] = (
    team_games["wins_before"] / team_games["games_before"]
)

team_games["avg_points_scored_before"] = (
    team_games["points_scored_before"] / team_games["games_before"]
)

team_games["avg_points_allowed_before"] = (
    team_games["points_allowed_before"] / team_games["games_before"]
)

team_games["avg_point_diff_before"] = (
    team_games["point_diff_before"] / team_games["games_before"]
)

print(team_games.head(10))

# Remove games where a team has no previous-game statistics
team_games = team_games[team_games["games_before"] > 0].copy()

print("Team-game shape:", team_games.shape)
print(team_games.head())

# Select the pregame statistics we need
pregame_stats = team_games[
    [
        "game_id",
        "team",
        "win_pct_before",
        "avg_points_scored_before",
        "avg_points_allowed_before",
        "avg_point_diff_before"
    ]
].copy()

# Create the home-team statistics
home_stats = pregame_stats.rename(columns={
    "team": "home_team",
    "win_pct_before": "home_win_pct",
    "avg_points_scored_before": "home_avg_points_scored",
    "avg_points_allowed_before": "home_avg_points_allowed",
    "avg_point_diff_before": "home_avg_point_diff"
})

# Create the away-team statistics
away_stats = pregame_stats.rename(columns={
    "team": "away_team",
    "win_pct_before": "away_win_pct",
    "avg_points_scored_before": "away_avg_points_scored",
    "avg_points_allowed_before": "away_avg_points_allowed",
    "avg_point_diff_before": "away_avg_point_diff"
})

print("Home stats shape:", home_stats.shape)
print("Away stats shape:", away_stats.shape)

# Select the pregame statistics we need
pregame_stats = team_games[
    [
        "game_id",
        "team",
        "win_pct_before",
        "avg_points_scored_before",
        "avg_points_allowed_before",
        "avg_point_diff_before"
    ]
].copy()

# Get the home and away teams from the schedule
game_teams = schedule[
    ["game_id", "home_team", "away_team"]
].copy()

# Create home-team statistics
home_stats = game_teams.merge(
    pregame_stats,
    left_on=["game_id", "home_team"],
    right_on=["game_id", "team"],
    how="inner"
)

home_stats = home_stats.rename(columns={
    "win_pct_before": "home_win_pct",
    "avg_points_scored_before": "home_avg_points_scored",
    "avg_points_allowed_before": "home_avg_points_allowed",
    "avg_point_diff_before": "home_avg_point_diff"
})

# Create away-team statistics
away_stats = game_teams.merge(
    pregame_stats,
    left_on=["game_id", "away_team"],
    right_on=["game_id", "team"],
    how="inner"
)

away_stats = away_stats.rename(columns={
    "win_pct_before": "away_win_pct",
    "avg_points_scored_before": "away_avg_points_scored",
    "avg_points_allowed_before": "away_avg_points_allowed",
    "avg_point_diff_before": "away_avg_point_diff"
})

print("Home stats shape:", home_stats.shape)
print("Away stats shape:", away_stats.shape)

# Start with the schedule information we need
model_data = schedule[
    ["game_id", "season", "week", "away_team", "home_team", "spread_line"]
].copy()

# Add the home team's pregame statistics
model_data = model_data.merge(
    home_stats[
        [
            "game_id",
            "home_win_pct",
            "home_avg_points_scored",
            "home_avg_points_allowed",
            "home_avg_point_diff"
        ]
    ],
    on="game_id",
    how="inner"
)

# Add the away team's pregame statistics
model_data = model_data.merge(
    away_stats[
        [
            "game_id",
            "away_win_pct",
            "away_avg_points_scored",
            "away_avg_points_allowed",
            "away_avg_point_diff"
        ]
    ],
    on="game_id",
    how="inner"
)

print("Model data shape:", model_data.shape)
print(model_data.head())

OLS Regression Results                            
==============================================================================
Dep. Variable:            spread_line   R-squared:                       0.584
Model:                            OLS   Adj. R-squared:                  0.579
Method:                 Least Squares   F-statistic:                     110.7
Date:                Thu, 17 Sep 2026   Prob (F-statistic):           9.27e-45
Time:                        17:03:23   Log-Likelihood:                -681.06
No. Observations:                 240   AIC:                             1370.
Df Residuals:                     236   BIC:                             1384.
Df Model:                           3                                         
Covariance Type:            nonrobust                                         
=======================================================================================
                          coef    std err          t      P>|t|      [0.025      0.975]
---------------------------------------------------------------------------------------
const                   1.7801      0.270      6.600      0.000       1.249       2.311
win_pct_diff            3.2328      1.229      2.629      0.009       0.811       5.655
points_scored_diff      0.3180      0.049      6.518      0.000       0.222       0.414
points_allowed_diff    -0.3497      0.051     -6.889      0.000      -0.450      -0.250
==============================================================================
Omnibus:                        2.654   Durbin-Watson:                   1.922
Prob(Omnibus):                  0.265   Jarque-Bera (JB):                2.681
Skew:                          -0.071   Prob(JB):                        0.262
Kurtosis:                       3.498   Cond. No.                         37.3
==============================================================================

Notes:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.

import matplotlib.pyplot as plt

plt.scatter(model_data["predicted_spread"], model_data["residuals"])

plt.axhline(y=0, linestyle="--")

plt.xlabel("Predicted point spread")
plt.ylabel("Residual")
plt.title("Residuals vs. Predicted Point Spread")

plt.show()

import statsmodels.api as sm
import matplotlib.pyplot as plt

sm.qqplot(model_data["residuals"], line="45")

plt.title("Q-Q Plot of Regression Residuals")
plt.show()

plt.scatter(
    model_data["points_allowed_diff"],
    model_data["spread_line"]
)

plt.xlabel("Points Allowed Difference (Home − Away)")
plt.ylabel("Point Spread")
plt.title("Points Allowed Difference vs. NFL Point Spread")

plt.axhline(y=0, linestyle="--")

plt.show()

plt.scatter(
    model_data["points_scored_diff"],
    model_data["spread_line"]
)

plt.axhline(y=0, linestyle="--")

plt.xlabel("Points Scored Difference (Home − Away)")
plt.ylabel("Point Spread")
plt.title("Points Scored Difference vs. NFL Point Spread")

plt.show()

print("R-squared:", model.rsquared)
print("Adjusted R-squared:", model.rsquared_adj)
print("F-statistic:", model.fvalue)
print("F-test p-value:", model.f_pvalue)
print("Number of observations:", int(model.nobs))

R-squared: 0.5844885404963711
Adjusted R-squared: 0.5792066151636979
F-statistic: 110.65823609448002
F-test p-value: 9.273560863474204e-45
Number of observations: 240
