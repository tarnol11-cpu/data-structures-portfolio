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
