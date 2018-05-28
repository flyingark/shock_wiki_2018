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
  * output file: `/data/all_treated_main_metric.csv`

    | Fieldname   | Remark |
    | ----------  |---------- |
    | `ArticleId` | id of article |
    | `RelWeek`   | week relative to the time of shock |
    | `StartDate`, `EndDate` | start and end date of the corresponding week |
    | `RetentionEndDate` | end date of the retention period |
    | `NumRevNew`, `NumRevOld`, `NumRev` | number of revisions by new / incumbent / all editors |
    | `NumEditorNew`, `NumEditorOld`, `NumEditor` | number of new / incumbent / all editors |
    | `Gini` | gini coefficient normalized by theoretical upperbound |
    | `NumRevertedNew`, `NumRevertedOld` | number of revisions reverted by new / incumbent editors |
    | `NumRevertingNew`, `NumRevertingOld` | number of revertings made by new / incumbent editors |
    | `NumTotalRev` | number of cumulative revisions up to the week |

* Get the set of new editors, incumbent editors, incumbent editors who join before the shock, incumbent editors who join after the shock, editors who are new to Wikipedia
  * code: `/code/fetch_editorset.py`
  * require `/data/all_treated_info.csv`, `/data/bot_list.csv` and `/data/treated_history.csv`
  * output file: `/data/all_treated_editor_set.csv`.
  
    | Fieldname | Remark |
    | ---------- |---------- |
    | `ArticleId` | id of article |
    | `RelWeek` | week relative to the time of shock |
    | `StartDate`, `EndDate` | start and end date of the corresponding week |
    | `RetentionEndDate` | end date of the retention period |
    | `NewEditorSet` | set containing new editors in the week |
    | `PreShockEditorSet`, `PostShockEditorSet` | set containing incumbent editors who join before / after the shock |
    | `NewWikiEditorSet` | set containing new editors who are new to Wikipedia as well |

* Get retention.
  * code: `/code/fetch_retention.py`
  * require `/data/all_treated_info.csv`, `/data/bot_list.csv` and `/data/treated_history.csv`
  * output file: `/data/retention.csv`
    
    | Fieldname | Remark |
    | ---------- |---------- |
    | `ArticleId` | id of article |
    | `RelWeek` | week relative to the time of shock |
    | `NumCumulRevNew`, `NumCumulRevOld`, `NumCumulRev` | number of revisions by new / incumbent / all editors to the focal article in the retention period |
    | `NumCumulEditorNew`, `NumCumulEditorOld`, `NumCumulEditor` | number of new / incumbent / all editors who remain active in the focal article in the retention period |

* Spillover over all Wikipedia
  * code: `/code/get_all_wiki_rev_currentweek.py`
  * require `/data/all_treated_info.csv`, `/data/bot_list.csv`, `/data/treated_history.csv` and `/data/all_treated_main_metric_sort_by_date.csv` (**NOT** `/data/all_treated_main_metric.csv`)
  * output file: `/data/all_treated_allwikirev_currentweek.csv`. For  includes four summary statistics for various measures: sum, mean, median and mean of log-transformation. We use _ to denote these summary statistics.
  
    | Fieldname | Remark |
    | ---------- |---------- |
    | `ArticleId` | id of article |
    | `__EditorAllWiki` | number of revisions by all editors over the entire Wikipedia |
    | `__OldEditorAllWiki` | number of revisions by old editors over the entire Wikipedia |
    | `__NewEditorAllWiki` | number of revisions by new editors over the entire Wikipedia |
    | `__PreShockAllWiki` | number of revisions by old editors who join before shock over the entire Wikipedia |
    | `__PostShockAllWiki` | number of revisions by old editors who join after shock over the entire Wikipedia |
    | `__NewWikiAllWiki` | number of revisions by new editors who are also new to Wikipedia over the entire Wikipedia |
    
    Note: For each measure, the output file contains four summary statistics (which is represented by a `__` here): `Sum` for sum, `Mean` for mean, `Med` for median, `LogMean` for mean of log-transformation.
    
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
