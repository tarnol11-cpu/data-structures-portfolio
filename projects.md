# Projects
This section documents my data science projects, research questions, and data stories I create throughout the semesters.
---
## Project 1
## Research Question
### Which team performance factors are most strongly associated with NFL point spreads?
## Dataset and Description
### Source: 2025 NFL data obtained through the nflverse (nflreadpy) package avaliable in python which provides schedule and team-level statistics. Two different data sets contained in the nflreadpy package. The first being the schedule dataset for game-level information. The second being the team statistics dataset for team performance-level information.
### Unit of Analysis: One NFL game after aggregating the team-level data.
### Features (Betting-Market, Outcomes, and Statistical Model): Point spread will be my dependent variable. Game total, final score, scoring margin/winner, team performance, and win/loss percentage will all be other variables used to get to the outcome variable. 
### Size: The 2025 schedule dataset has 285 games and 46 features. The 2025 team statistics dataset has 570 team-game observations and 138 features.
### Missing Values: All primary variables used in the analysis contain no missing values, some unused schedule variables contain missing values such as nfl_detail_id and pff, therefore these variables will be excluded rather than imputed into my analysis.

## Conceptualized/operationalized variables and important context
## Variables
## Point Spread - Outcome Variable/ Dependent Variable
## Win Percentage Difference - Home team's pregame win % minus the away teams's pregame win %
## Point Differential Difference - Home team's average pregame point differential minus the away team's average
## Points Scored Difference - Home teams's average points scored minus the away team's average points scored
## Points Allowed Difference - Home team's average points allowed minus the away team's average points allowed
In order to prevent data leakage we are measuring the team perfomance before each game, in order to help predict that factors that go into deciding the point spread for the upcoming game.
Point spreads are designed to be able to represent the expected margin between different teams. The goal of this project is not to determine exactly how sportsbooks decipher the spreads, but rather to determine which variables that we can observe, are most strongly associated with the point spreads that are published for NFL games.
## Data Cleaning and Preparation
The raw NFL data was obtained programmatically by using the nflreadpy package which is avaliable via vscode and was convereted from Polars DataFrames to pandas DataFrames for cleaning and analysis. The initial numbers for the schedule data contained 285 games and 46 variables. The weekly team statistics data contained 570 team-game observations and 138 variables.
To start the data cleaning, I condensed the analysis to just be regular season games in order to focus on team performance during the regular season since playoff games have a different competitive enviornemnt.
I then excluded week 1 games because the data is revolved aroud the 2025 season, and there would be no pre-game data for week 1 since this was the first data of the season. This reduced the schedule data from 272 regular season games to 256 games.
I then reshaped the schedule data so that there was one team observation per game. This made it easier to be able to calculate each team's points scored, point differential, points allowed, and team win's per week. I used pandas groupby() and cumulative calculations in order to use games that team performance statistics from a previous game.
After calculating the pregame statistics, I removed any obersvations that had zero previous games. This opened the opportunity to be able to merge the home-team and away-team statistics into the game-level schedule using game_id. I was then able to calculate home minus away differences for points scored, allowed, differential, and win percentage.
The final dataset that I used had 240 NFL games, 0 missing values, and no duplicate games.

[View the full data cleaning code](https://github.com/tarnol11-cpu/data-structures-portfolio/blob/main/data_cleaning.py)
