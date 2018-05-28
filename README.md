# shock_wiki_2018

_Collaborator: Ruihan Wang, Eric Blohm, Daniel Romero, Ceren Budak, Lionel Robert_

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
Follow the steps below to generate the measures to be analyzed.
* Level of activity, gini and reverts
  * code `/code/fetch_main_measure.py`
  * require `/data/all_treated_info.csv`, `/data/bot_list.csv` and `/data/treated_history.csv`
  * output file: `/data/all_treated_main_metric.csv`. fields: `ArticleId`, `RelWeek`, `StartDate`, `EndDate`, `RetentionEndDate`,	`NumRevNew`, `NumRevOld`, `NumRev`,	`NumEditorNew`,	`NumEditorOld`,	`NumEditor`, `Gini`, `NumRevertedNew`, `NumRevertedOld`, `NumRevertingNew`, `NumRevertingOld`, `NumTotalRev`.
| Fieldname | Remark |
| ---------- |---------- |
| `ArticleId` | id of article |
| `RelWeek` | week relative to the time of shock |

* Get the set of new editors, incumbent editors, incumbent editors who join before the shock, incumbent editors who join after the shock, editors who are new to Wikipedia
  * code: `/code/fetch_editorset.py`
  * require `/data/all_treated_info.csv`, `/data/bot_list.csv` and `/data/treated_history.csv`
  * output file: `/data/all_treated_editor_set.csv`. fields: `ArticleId`, `RelWeek`, `StartDate`, `EndDate`, `RetentionEndDate`,	`NewEditorSet`, `PreShockEditorSet`, `PostShockEditorSet`,	`NewWikiEditorSet`.

* Get retention.
  * code: `/code/fetch_retention.py`
  * require `/data/all_treated_info.csv`, `/data/bot_list.csv` and `/data/treated_history.csv`
  * output file: `/data/retention.csv`. fields `ArticleId`, `RelWeek`, `StartDate`, `NumCumulRevNew`, `NumCumulRevOld`, `NumCumulRev`, `NumCumulEditorNew`, `NumCumulEditorOld`, `NumCumulEditor`.

* Spillover over all Wikipedia
  * code: `/code/get_all_wiki_rev_currentweek.py`
  * require `/data/all_treated_info.csv`, `/data/bot_list.csv`, `/data/treated_history.csv` and `/data/all_treated_main_metric_sort_by_date.csv` (**NOT** `/data/all_treated_main_metric.csv`)
  * output file: `/data/all_treated_allwikirev_currentweek.csv`.

* Retention over all Wikipedia
  * code: `/code/get_all_wiki_retention.py`
  * require `/data/all_treated_info.csv`, `/data/bot_list.csv`, `/data/treated_history.csv` and `/data/all_treated_main_metric_sort_by_date.csv` (**NOT** `/data/all_treated_main_metric.csv`)
  * output file: `/data/all_treated_allwikireten_currentweek.csv`

* Non-zero spillover over all Wikipedia
  * code: `/code/get_spillover_nonzero.py`
  * require `/data/main_metric_sort_by_date.csv`, `/data/history_all_wiki_sort_by_date.csv` and `/data/bot_list.csv`
  * output file: `/data/main_metric_sort_by_date_spillover_nonzero.csv`

## Analysis
Run `Analysis.Rmd`.
