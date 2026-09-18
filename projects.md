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

## Visuals 
The visuals below help examine the relationships between pregame performance and NFL point spreads. The observations represent one NFL game, and the perfomance differences are calculated as the home team's value minus the away teams.

### Points Allowed Difference vs NFL Point Spread
<img width="575" height="454" alt="image" src="https://github.com/user-attachments/assets/f9bf9eef-28bd-4f4c-a9f2-621f09c2e2ff" />
This scatter plot shows the relationship between the difference in average points allowed by the home and away teams and the published point spread. This plot has a general downward spread. One thing to note is that if a team has a positive point spread that means they are favored to win by that many points. This is opposite from sportsbook because the point spread for a sportsbook would be negative for the favored team. In our case a positive point spread means the home team is favored to win, this is how the nflverse dataset represents point spreads. The downward trend shows that when the home team has a lower points allowed, they have a higher point spread meaning they are favored to win. When the home team has a more points allowed they are expected to lose.

### Points Scored Difference vs NFL Point Spread
<img width="575" height="454" alt="image" src="https://github.com/user-attachments/assets/64d92618-7b60-4d65-899b-1a4c2c2b74a9" />
This scatter plot shows the relationship between the difference in average points scored by the home and away teams and the published point spread. It has a general upward trend. When the home team has a lower points scored differnce relative to the away team, they are expected to lose. As you move up the graph, when the home team has a higher points scored difference compared to the away teams points scored difference they are favored to win.

## Ethics and Limitations
This project uses publicly avaliable NFL data obtained programmatically from nfl verse. There was no private or sensitive information used in the analysis. The data is describing publicy avaliable game and team performance, so ethical considerations involve responsible interpretation of the results rather than personal privacy.

One of the limitations was the fact that only 2025 NFL regular season data was used. With this being said, this only represents a relatively smaller sample and may not exactly correlate with other seasons. Another limitation is that coaching, injuries, schedules and other in season conditions vary from year to year. Results should not be assumed to apply to every individual season.

Another limitation is that the model used, has 2 factors it was narrowed down to: average point scored and average points allowed. They are other factors that may not be included that could associate with the point spread. For example injuries, roster changes, weather, etc. This means that the model does not explain all of the factors that may influence the dependent varibale (published spread).

Additional context could play a part in this because certain teams may have more defensive advantages meaning points may not all have came from the same thing.

There may be potential bias due to the information that is included or excluded in the dataset. Since the model focuses on regular season performance, factors that are difficult to measure may be unshown. Also since the data is from the game before, early-season games have less historical information than later-season games.

Finally the results describe association rather than causation. Other variables may influence both team performance and the published spread.

## Unanswered Questions
They are several questions that remain outside the scope of this project. Would the same relationships appear accross multiple NFL seasons? Would roster changes, trades, injuries, weather, or other statistics improve the model? Would playoffs have a different model? Future research could be done to address these questions by using multiple seasons and offering additional information.

## Code and AI Transparency
## Code
The python code was used to obtain, clean, prepare, visualize, and analyze the NFL data. 



