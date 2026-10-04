
layout: default
title: Project 2

# Project 2: NFL Running Back Rushing Yard Prediction

## Research Question

What variables most accurately predict how many rushing yards an NFL running back will record in an upcoming game?

## Project Overview

This project uses machine learning to predict NFL running back rushing yards based on player performance, recent workload, opponent characteristics, and game context.

## Problem Definition

This project aims to predict how many rushing yards an NFL running back will have in an upcoming NFL game. The model predicts this uses previous game information from the running back and the upcoming teams defense.

## Target Variable

The target variable is rushing_yards, which represents the number of rushing yards a running back records in a game.

## Classification or Regression?

This is a regression problem because the model predictsa continous numerical value rather than a category. The numerical value being rushing yards from a running back.

## Who Benefits?

This model is useful for NFL teams, coaches, and sports analysts who want to better understand what factors associate with running back performance. As well as fantasy football players interested in player performance.

## Why is the problem meaningful?

Predicting running back performance is meaningful because it can be affected by many things such as workload, previous performance, opposing defense, etc. Being able to understand which ones stick out the most for the highest correlation helps with prediciting expected performance.

# Background and Context

## What does the reader need to know?

NFL running back performance can vary from game to game because of all of the different factors that can affect it. Being able to narrow it down to what factors affect it the most takes looking at multiple factors rather than just a player's season average.

## What previous research or domain knowledge informs my approach?

Previous research has examined the relationship between running back workload and future performance. Research on NFL running backs shows that the number of carries a running back receives can be an important factor when examining future workload and performance.

## What do credible sources suggest about relevant, patterns, or concerns?

The research suggests that workload and carries are relevant factors, although just because running back has a higher number of carries, this does not mean a player will always produce more rushing yards.

## Sources

Source 1:

Kraeutler, M. J., Belk, J. W., & McCarty, E. C. (2017). The effect of the number of carries on injury risk and subsequent season's performance among running backs in the National Football League. Orthopaedic Journal of Sports Medicine, 5(3). https://doi.org/10.1177/2325967117691941

Source 2:

Kraeutler, M. J., Belk, J. W., & McCarty, E. C. (2017). The effect of the number of carries among college running backs on future injury risk and performance in the National Football League. Orthopaedic Journal of Sports Medicine, 5(5). https://doi.org/10.1177/2325967117703054 

Source 3:

Salaga, S., Mills, B. M., & Tainsky, S. (2020). Employer-assigned workload and human capital deterioration: Evidence from the National Football League. Journal of Sports Economics, 21(6), 574–599. https://doi.org/10.1177/1527002520930258

# Data Description

## Where did the data come from?

The data used in this project comes from nflverse, a python package avaliable. The data can be accessed through the nflreadpy python package and nflverse data repositories.

Sources:

[nflverse](https://github.com/nflverse)
[nflverse Data Repository](https://github.com/nflverse/nflreadpy)

## What does each observation or row represent?

Each observation represents one NFL running back's performance in one game.

For example, one row could represent Derrick Henry's performance in week 4 of the 2025 season. The row could contain information about his performance and workload, also information about the opposing team's defense.

## How large is the dataset?

The orginial dataset had 7,687 observations and 156 columns.
After doing some cleaning and figuring out the most important variables, my final dataset contained:

- 5,983 observations
- 11 columns
- 4 predictor variables
- 1 target variable
- The rest of the columns are the player, team, opponent, season, week, and game.

## What potential features are avaliable

1. previous_game_carries - number of carries the running back had in their last game
2. average_carries_last_3 - average number of carries over their last 3 games
3. average_rushing_yards_allowed_last_3 - average rushing yards the opposing defense allowed over the past 3 games
4. home_game - whether or not the running back is at home

These were selected because they are avliable before the upcoming game.

## Assumptions and Limitations

The analysis is limited to information that is included in the nflverse dataset. Observations that did not have previous game history were removed to prevent data leakage. The data aslo does not include every factor like injuries, offensive-line performance, or other factors that were not avaliable on nfl verse that may affect a running back's performance. A time-based train/test aplit was used to simulate future games.

# Data Understanding and Exploration

## Summary Statistics and Target Variable Distribution

The summary statistics showed substanial variation in running back workload and rushing production. The previous-game carries ranged from 0 to 36, over the last three it ranged from 0 to 32, with a mean of 34.38 yards and a median of 23 yards. The difference between the mean and median suggests that high-yardage performance creates upper tail in the distribution.

There is an uneven distribution, not a class-imbalance problem because this is a regression problem rather than a classification project.

## Patterns, Relationships, Unusual Values, or Outliers?

| Feature                                       | Correlation with rushing yards |
| --------------------------------------------- | -----------------------------: |
| **Average carries last 3**                    |                      **0.604** |
| **Previous game carries**                     |                      **0.551** |
| Average opponent rushing yards allowed last 3 |                          0.052 |
| Home game                                     |                          0.012 |

This shows that recent workload variables like (average carries last 3), (previous game carries). 

There were some unusual values. Rushing yards ranged from -8 to 225, showing that the dataset had negative and extremely high rushing performances. These yardage-high games help explain why the mean is considerably higher than what the median was.

## Visualizations

The most useful visualization created was the: Actual vs. Predicted Rushing Yards scatterplot.

It compares the actual rushing yards vs the predicted rushing yards and looked like this: <img width="696" height="546" alt="image" src="https://github.com/user-attachments/assets/578e601f-3bd9-433c-ac53-61af8d1f659e" />

The plot shows the predictions generally following the pattern of the actual rushing yards, although there is some variation around the perfect one. The model struggles with high rushing-yard performances, it tended to predict lower than what really happened.

## Exploration informing selection/preprocessing

The exploration showed us why it was important to create rolling features based on previous games. Current-game statistics like current rushing yards would not work and would cause data-leakage.

The uneven distribution of rushing yards also influenced the decision to evaluate the models using MAE, RMSE, and R-sqaured.

# Data Preparation and Feature Selection

## Missing Values, duplicate observations, outliers, or inconsistent data

Since multiple of the variables had to do with previous game information or past 3 games, any row that didn't have that information was removed.

## Included and excluded features

Included: 
- Previous game carries
- Average carries over last 3 games
- Opponents average rushing yards allowed over last 3 games
- Home game

These were chosen beacuse they provide information that can be known before the upcoming game.

Current-game statistics like rushing yards, touchdowns, rushing epa, etc. were excluded beacuse they would cause data leakage.

## Categorical variables encoded, numerical variables scaled, or features transformed?

The home_game variable was converted to 0 or 1 in order to help with the smoothness and all being numerical variables. No scaling was required because Random Forest and Linear Regression just use numerical.

## How was the data seperated for training and evaluation

A time-based split was used:

- Training: 2021-2024 seasons had 4,725 observations
- Testing: 2025 season had 1,258 observations

## Steps taken to prevent data leakage

Workload and defensive rolling features were calculated using previous games only. Current-game statistics were excluded to prevent data leakage and 2025 season data was used. This makes sure the model uses relevant data to prevent leakage as well.

# Baseline and Model Development 

## Baseline established and why its appropriate.

The baseline established predicted average rushing yards from training data. It is appropriate because it is a simple holder that machine learning model should outperform.

## Machine-Learning models trained

I trained two model:
- Linear Regression
- Random Forest Regression

## Why were these models appropriate

These models were appropriate because the target variable (rushing_yards), is a continuous numerical value, hence why this is a regression problem. Linear Regression is able to do linear relationships and Random Forest is able to do a little bit more complex, nonlinear relationships.

## Model settings or hyperparameters tuned?

No hyperparameter tuning took place. Random forest used 100 trees with a random state of 42 to make the results.

## How were models compared fairly?

Both models were trained using the same training data and four features on the exact same 2025 test data. They were both compared using similar metrics like R-sqaured, MAE, and RMSE.

# Model Evaluation and Selection

## Which evaluation metrics were used and why are they appropriate

MAE: Shows the average number of rushing yards the prediction is off by. Easy to interpret.
RMSE: Penalizes larger prediction errors more heavily, which is useful because some RB games have very large errors.
R²: Shows how much of the variation in rushing yards the model explains.

## How did each model perform compared with the baseline and the other models?

| Model                 |       MAE |      RMSE |        R² |
| --------------------- | --------: | --------: | --------: |
| Baseline              |     29.80 |     37.76 |   -0.0002 |
| **Linear Regression** | **21.19** | **30.85** | **0.333** |
| Random Forest         |     23.18 |     33.04 |     0.234 |

The models beat the baseline, Linear Regression performed the best according to the metrics.

## Final Model

I selected Linear Regression as the final model, simply due to the fact we are working with all numerical values and linear regression performed the best according to the metrics.

## Evidence

Linear Regression had the lowest MAE and RMSE, while having the highest R-sqaured. It was able to predict the rushing yards a bit more accurately than baseline and Random Forest.

## Meaningful tradeoffs?

Yes, Random forest captured more complex, nonlinear relationships, but it did not perform as well on the dataset. Linear Regression was more accurate and was easier to interpret, hence why I chose this as my final model.

# Model Interpretation and Insights

## What did the model learn about the relationship between the features and the target?

The model found that the variable strongest related to rushing yards was recent workload. Running backs with more carries lead to more rushing yards. 

## Which features appear most influential?

- Average carries last 3 games: +2.90 yards per additional average carry
- Previous game carries: +0.74 yards per additional carry
- Home game: +0.19 yards
- Opponent average rushing yards allowed last 3: +0.06 yards

Average carries over last 3 games appeared to be the modt influential.

## Where does the model perform well or poorly?

The model performed well for rushing yard performances but has difficulty predicting high yardage games. The actual vs predicted plot showed that the model tends to underpredict big performances.

## What can be learned from the coefficients and example predictions?

The coefficients showed that recent workload was the strongest predictor. Example predictions also show the general trend of a player's performance but can't predict individual performances.

## Conclusions

We can conclude that recent workload is associated with rushing yards production and the model is able to predict better than the baseline. We can't conclude that more carries causes more rushing yards. We also couldn't account for injuries, O-line performance, weather, or other factors that may affect running back performance so these could help.

# Limitations, Ethics, and Reflection

## What biases may exist in the dataset

The dataset does not include all factors that may affect a running backs rushing yards such as injuries, offensive-line production, weather, coaching etc. Also it only focuses on avaliable seasons so results may not apply equally to every player or situation.

## Who might be affected by incorrect predictions

Incorrect predictions may affect NFL teams, coaches, or sports analysts of any sort. Anybody who uses statistics to make decisions.

## What are the consequences of prediction errors?

The consequences of prediction errors could be someone having unrealistic expectations whether it's over or underpredicting. Large errors are especially important for high or low rushing performances.

## Would this model be appropriate for real-world decision-making? Why or why not?

It could be used as a source of information but not purely relied on for real-world decisions.

## What additional data, features, or modeling approaches would you explore next?

I would explore different things like finding a way to include injuries, offesnive line grades, or defensive tendencies to help support the model.

## What should users understand before relying on the model?

Users should understand that the model provides an estimate, not a guarantee. It performs better than the baseline but still has prediction error, especially for high-yardage games.

# Code and Transparency

## Full Jupyter Notebook

[View the full Jupyter Notebook](NFL_RB_Rushing_Yard_Prediction.ipynb.ipynb)
















