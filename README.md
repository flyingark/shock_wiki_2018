# shock_wiki_2018

_Collaborator: Ruihan Wang, Eric Blohm, Daniel Romero, Ceren Budak, Lionel Robert_

This project identifies and evaluates the impact of shock on the collaborative dynamics on Wikipedia articles. The shocks are identified using google trennds data. We focus on three sets of articles:
  1. Politican
  2. Academic scholars
  3. Random set from WikiProject Biography

The project path is `arkzhang@epico.si.umich.edu:~/shock_wiki_2018`. Unless otherwise specified, the files are under this directory.

## Identify Shock
The raw data of shock is from Ruihan's code. Ruihan has provided [a fairly detailed explanation](https://github.com/dlwrh/wiki-shock-analysis), so I just briefly summarize what to do for replication. To identify the shock,
  1. run [suggest.py](https://github.com/dlwrh/wiki-shock-analysis/blob/master/code/suggest.py), [suggestions_analysis.py](https://github.com/dlwrh/wiki-shock-analysis/blob/master/code/suggestions_analysis.py) and [get_trends.py](https://github.com/dlwrh/wiki-shock-analysis/blob/master/code/get_trends.py). The output is a tsv file that records the trends
  2. Process the monthly level trends with [read_trends.py](https://github.com/flyingark/shock_wiki_2018/blob/master/read_trends.py) and [identify_shock_trends.R](https://github.com/flyingark/shock_wiki_2018/blob/master/identify_shock_trends.R). This will generate a new `trends_data.csv`
  3. run [get_daily_trends.py](https://github.com/dlwrh/wiki-shock-analysis/blob/master/code/get_daily_trends.py). This script requires `trends_data.csv` and retrieves daily-level trends.
  4. Step 2 identifies the month in which the shock takes place. Rerun Ruihan's code to fetch the shock data at the daily level.
  4. The day on which the highest shock level is observed is the date of shock.

## Article history file
* csv file recording the entire history for focal articles (sorted by article name): `/data/treated_history.csv`
* csv file recording the revision history of the editors who revised any focal article: `/data/history_all_wikipedia_sort_by_date.csv`
* csv file recording the article id, shockdate, category (academia, political, sample) of each focal article: `/data/all_treated_info.csv`
* list of bot accounts: `/data/bot_list.csv`

## Fetch measures
Follow the steps below to generate the measures to be analyzed.
* Level of activity, gini and reverts
  * code [fetch_main_measure.py](https://github.com/flyingark/shock_wiki_2018/blob/master/fetch_main_measure.py)
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

  * execute bash command `(head -n 1 main_metric.csv && tail -n +2 all_treated_main_metric.csv | sort -t',' -k3,3) > all_treated_main_metric_sort_by_date.csv"`. This generates a new csv file that contains exactly the same information but is sorted chronologically. This file will be used later to calculater measures all over Wikipedia.
  
* Talk page activity
  * code [talk_stats_analysis.py](https://github.com/dlwrh/wiki-shock-analysis/blob/master/code/talk_stats_analysis.py)
  * require `/data/all_treated_main_metric.csv`
  * output file: `/data/wiki_talk_stats_XX_final.csv`. _Note: The talk page measure consists of three output files (academics, politicians, and biosample). The reason is that when we generate the data, I fetch the main measure separately for the three groups and so Ruihan ran the code separately for the three groups too. Now, since the information for all three groups are condensed into one file, running the code once will suffice._
  
    | Fieldname   | Remark |
    | ----------  |---------- |
    | `ArticleId` | id of article |
    | `RelWeek`   | week relative to the time of shock |
    | `#total_comment` | total number of revisions to talk pages |
    | `#editis_per_neweditor` | average number of revisions to talk page by new editors |
    | `#neweditors` | number of new editors |
    | `#neweditors_comment` | number of revisions to talk pages by new editors |
    | `#reply_neweditors` | number of replies to new editors on talk page |
    | `fraction_talk_reply_neweditors` | ratio of reply to revisions by new editors at talk page |

* Get the set of new editors, incumbent editors, incumbent editors who join before the shock, incumbent editors who join after the shock, editors who are new to Wikipedia
  * code: [fetch_editorset.py](https://github.com/dlwrh/wiki-shock-analysis/blob/master/code/fetch_editorset.py)
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
  * code: [fetch_retention.py](https://github.com/dlwrh/wiki-shock-analysis/blob/master/code/fetch_retention.py)
  * require `/data/all_treated_info.csv`, `/data/bot_list.csv` and `/data/treated_history.csv`
  * output file: `/data/retention.csv`
    
    | Fieldname | Remark |
    | ---------- |---------- |
    | `ArticleId` | id of article |
    | `RelWeek` | week relative to the time of shock |
    | `NumCumulRevNew`, `NumCumulRevOld`, `NumCumulRev` | number of revisions by new / incumbent / all editors to the focal article in the retention period |
    | `NumCumulEditorNew`, `NumCumulEditorOld`, `NumCumulEditor` | number of new / incumbent / all editors who remain active in the focal article in the retention period |

* Spillover over all Wikipedia
  * code: [get_all_wiki_rev_currentweek.py](https://github.com/dlwrh/wiki-shock-analysis/blob/master/code/get_all_wiki_rev_currentweek.py)
  * require `/data/all_treated_info.csv`, `/data/bot_list.csv`, `/data/treated_history.csv` and `/data/all_treated_main_metric_sort_by_date.csv` (**NOT** `/data/all_treated_main_metric.csv`)
  * output file: `/data/all_treated_allwikirev_currentweek.csv`. For  includes four summary statistics for various measures: sum, mean, median and mean of log-transformation. We use _ to denote these summary statistics.
  
    | Fieldname | Remark |
    | ---------- |---------- |
    | `ArticleId` | id of article |
    | `RelWeek` | week relative to the time of shock |
    | `__EditorAllWiki` | number of revisions by all editors over the entire Wikipedia |
    | `__OldEditorAllWiki` | number of revisions by old editors over the entire Wikipedia |
    | `__NewEditorAllWiki` | number of revisions by new editors over the entire Wikipedia |
    | `__PreShockAllWiki` | number of revisions by old editors who join before shock over the entire Wikipedia |
    | `__PostShockAllWiki` | number of revisions by old editors who join after shock over the entire Wikipedia |
    | `__NewWikiAllWiki` | number of revisions by new editors who are also new to Wikipedia over the entire Wikipedia |
    
     _Note: For each measure, the output file contains four summary statistics (represented by `__` here):_ `Sum` _for sum,_ `Mean` _for mean,_ `Med` _for median,_ `LogMean` _for mean of log-transformation._
    
* Retention over all Wikipedia
  * code: [get_all_wiki_retention.py](https://github.com/dlwrh/wiki-shock-analysis/blob/master/code/get_all_wiki_retention.py)
  * require `/data/all_treated_info.csv`, `/data/bot_list.csv`, `/data/treated_history.csv` and `/data/all_treated_main_metric_sort_by_date.csv` (**NOT** `/data/all_treated_main_metric.csv`)
  * output file: `/data/all_treated_allwikireten_currentweek.csv`

    | Fieldname | Remark |
    | ---------- |---------- |
    | `ArticleId` | id of article |
    | `RelWeek` | week relative to the time of shock |
    | `__OldEditorRetenAllWiki` | number of revisions by old editors over the entire Wikipedia during the retention period |
    | `__NewEditorRetenAllWiki` | number of revisions by new editors over the entire Wikipedia during the retention period|
    | `__PreShockRetenAllWiki` | number of revisions by old editors who join before shock over the entire Wikipedia during the retention period |
    | `__PostShockRetenAllWiki` | number of revisions by old editors who join after shock over the entire Wikipedia during the retention period|
    | `__NewWikiRetenAllWiki` | number of revisions by new editors who are also new to Wikipedia over the entire Wikipedia during the retention period |
    | `__NewNonWikiRetenAllWiki` | number of revisions by new editors who are not new to Wikipedia over the entire Wikipedia during the retention period |

    _Note: For each measure, the output file contains four summary statistics (represented by `__` here):_ `Sum` _for sum,_ `Mean` _for mean,_ `Med` _for median,_ `LogMean` _for mean of log-transformation._

* Non-zero spillover over all Wikipedia
  * code: [get_spillover_nonzero.py](https://github.com/dlwrh/wiki-shock-analysis/blob/master/code/get_spillover_nonzero.py)
  * require `/data/main_metric_sort_by_date.csv`, `/data/history_all_wiki_sort_by_date.csv` and `/data/bot_list.csv`
  * output file: `/data/main_metric_sort_by_date_spillover_nonzero.csv`
  
    | Fieldname | Remark |
    | ---------- |---------- |
    | `ArticleId` | id of article |
    | `RelWeek` | week relative to the time of shock |
    | `MeanSpillover` | mean of spillover over all Wikipedia |
    | `LogMeanSpillover` | mean of log-transformation spillover over all Wikipedia |
    
    _Note: For each editor, the spillover measure in a week is the ratio of the number of revisions over all Wikipedia to the average number of revisions (excluding weeks with no revisions)._
  

## Analysis
Run `Analysis.Rmd`. The [markdown file with output](https://github.com/flyingark/shock_wiki_2018/blob/master/Analysis_with_output.pdf) is also attached.
