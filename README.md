# shock_wiki_2018

_Collaborator: Ruihan Wang, Daniel Romero, Ceren Budak, Lionel Robert_

This project identifies and evaluates the impact of shock on the collaborative dynamics on Wikipedia articles. The shocks are identified using google trennds data. We focus on three sets of articles:
  1. Politican
  2. Academic scholars
  3. Random set from WikiProject Biography

## Identify Shock
The raw data of shock is from Ruihan's code. To identify the shock,
  1. Process the monthly level trends with `read_trends.py`.
  2. Process the output from 1 with `identify_shock_trends.R`.
  3. Step 2 identifies the month in which the shock takes place. Rerun Ruihan's code to fetch the shock data at the daily level.
  4. The day on which the highest shock level is observed is the date of shock.

## Fetch measures
The measures include activity, gini, cumulative retention. They are separately generated from `fetch_main_metric`, `fetch_experience`, `fetch_retention_cumulative`. Each piece will generate a csv file. Each line in that file corresponds to a snapshot of an article.

## Analysis
Run `Analysis.Rmd`.
