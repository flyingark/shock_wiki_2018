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
* Run script `arkzhang@epico.si.umich.edu:~/shock_wiki_2018/code/fetch_main_metric.py`. This generates `/data/main_metric.csv` and `/data/main_metric_sort_by_date.csv`. These two files contain essentially the same information. The measures includes:
  1. activity (number of revisions, editors, reverted, reverting)
  2. gini
  3. the set of new editors, incumbent editors, incumbent editors who join before the shock, incumbent editors who join after the shock, editors who are new to wikipedia
  4. size of article
* Run script `arkzhang@epico.si.umich.edu:~/shock_wiki_2018/code/fetch_retention.py`. This generates `/data/retention.csv`.
* Run script `arkzhang@epico.si.umich.edu:~/shock_wiki_2018/code/get_all_wiki_rev_currentweek.py`. This generates `/data/main_metric_sort_by_date_rev_currentweek.csv` that records the spillover over all wikipedia
* Run script `arkzhang@epico.si.umich.edu:~/shock_wiki_2018/code/get_all_wiki_retention.py`. This generates `/data/all_treated_allwikireten_currentweek.csv`that records retention over all wikipedia, but without normalization. Run script `arkzhang@epico.si.umich.edu:~/shock_wiki_2018/code/get_spillover_nonzero.py`. This generates `/data/main_metric_sort_by_date_spillover_nonzero.csv` that records spillover normalized by maximum number of revisions over an editor's lifetime.

## Analysis
Run `Analysis.Rmd`.
