# shock_wiki_2018

_Collaborator: Ruihan Wang, Daniel Romero, Ceren Budak, Lionel Robert_

This project identifies and evaluates the impact of shock on the collaborative dynamics on Wikipedia articles. The shocks are identified using google trennds data. We focus on three sets of articles:
  1. Politican
  2. Academic scholars
  3. Random set from WikiProject Biography

The project path is `arkzhang@epico.si.umich.edu:~/shock_wiki_2018`. Unless otherwise specified, the files are under this directory.

## Identify Shock
The raw data of shock is from Ruihan's code. To identify the shock,
  1. Process the monthly level trends with `read_trends.py`.
  2. Process the output from 1 with `identify_shock_trends.R`.
  3. Step 2 identifies the month in which the shock takes place. Rerun Ruihan's code to fetch the shock data at the daily level.
  4. The day on which the highest shock level is observed is the date of shock.

## Article history file
* csv file recording the entire history for focal articles (sorted by article name): `/data/treated_history.csv`
* csv file recording the revision history of the editors who revised any focal article: `/data/history_all_wikipedia_sort_by_date.csv`
* csv file recording the article id, shockdate, category (academia, political, sample) of each focal article: `/data/all_treated_info.csv`
* list of bot accounts: `/data/bot_list.csv`

## Fetch measures
* Fetch activity (number of revisions, editors, reverted, reverting) by all editors and separately by new and incumbent editors), the set of new editors, the set of incumbent editors, the set of new editors who are new to Wikipedia as well with `arkzhang@epico.si.umich.edu:~/shock_wiki_2018/code/fetch_main_metric.py`. Generates `/data/main_metric.csv` and `/data/main_metric_sort_by_date.csv` 
The measures include activity, gini, cumulative retention. They are separately generated from `fetch_main_metric`, `fetch_experience`, `fetch_retention_cumulative`. Each piece will generate a csv file. Each line in that file corresponds to a snapshot of an article.

## Analysis
Run `Analysis.Rmd`.
