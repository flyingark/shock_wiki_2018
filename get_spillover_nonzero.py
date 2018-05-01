# generate a csv file recording an article's editors' retention over all
# wikipedianumber of revision

from __future__ import division
import csv
import json
from datetime import date, datetime, timedelta
from collections import Counter
import numpy as np

def DatestampToDate(ds):
	"""convert datestamp to date object"""
	return datetime.strptime(ds, '%Y-%m-%d').date()

def MapSetDict(set_, dict_, default_val=0):
	"""return a list mapping set s to dictionary d"""
	list_ = []
	for item in set_:
		if item in dict_:
			list_.append(dict_[item])
		else:
			list_.append(default_val)
	return list_

def UpdateAllWikiDict(all_wiki_line, AllWikiRevDict):
	Editor = all_wiki_line['Editor']
	Date = DatestampToDate(all_wiki_line['Date']).toordinal()
	if Editor not in AllWikiRevDict:
		AllWikiRevDict[Editor] = {}
		AllWikiRevDict[Editor]["NumRev"] = 0
		AllWikiRevDict[Editor]["PrevNumRev"] = 0
		AllWikiRevDict[Editor]["StartDate"] = Date
		AllWikiRevDict[Editor]["NumPosWeek"] = 1
		AllWikiRevDict[Editor]["MaxPosWeek"] = 0
	if Date not in AllWikiRevDict[Editor]:
		AllWikiRevDict[Editor][Date] = 0
	AllWikiRevDict[Editor][Date] += 1
	AllWikiRevDict[Editor]["NumRev"] += 1

def TrimAllWikiDict(CurrStartDate, AllWikiRevDict):
	"""remove revisions before CurrRetentionStartDate"""
	for Editor, NumRevDict in AllWikiRevDict.iteritems():
		for Date in NumRevDict.keys():
			if Date not in ["NumRev", "PrevNumRev", "StartDate", "NumPosWeek", "MaxPosWeek"]:
				if Date < CurrStartDate.toordinal():
					n = NumRevDict.pop(Date)
					NumRevDict["PrevNumRev"] += n
					NumRevDict["NumRev"] -= n
				Week = (Date - AllWikiRevDict[Editor]["StartDate"]) // 7
				if Week > AllWikiRevDict[Editor]["MaxPosWeek"]:
					AllWikiRevDict[Editor]["MaxPosWeek"] = Week
					AllWikiRevDict[Editor]["NumPosWeek"] += 1 

def GetSpillover(AllWikiRevDict, MainMetricList):
	# go through main metric list and calculate spillover 
	for item in MainMetricList:
		SpilloverList = []
		# a list recording the fraction of editor's revision in the current week relative to previous revisions
		for Editor in item['NewEditorSet']:
			if Editor in AllWikiRevDict:
				NumWeeks = AllWikiRevDict[Editor]["NumPosWeek"]
				if AllWikiRevDict[Editor]['PrevNumRev'] != 0:
					SpilloverList.append((AllWikiRevDict[Editor]['NumRev']) / (AllWikiRevDict[Editor]['PrevNumRev'] / NumWeeks))
#			else:
#				NewEditorPrevList.append(0)
		item['MeanSpillover'] = np.mean(SpilloverList)
		item['LogMeanSpillover'] = np.mean(np.log(np.array(SpilloverList)))

main_metric_reader = csv.DictReader(open('../data/main_metric_sort_by_date.csv', 'r'))
all_wiki_reader = csv.DictReader(open('../data/history_all_wiki_sort_by_date.csv', 'r'))
all_wiki_line = all_wiki_reader.next()
writer = csv.DictWriter(open('../data/main_metric_sort_by_date_spillover_nonzero.csv', 'wb'),
	fieldnames=['ArticleId', 'RelWeek', 'MeanSpillover', 'LogMeanSpillover'],
	extrasaction='ignore')
writer.writeheader()

CurrStartDate = date(2000,1,1)
CurrEndDate = CurrStartDate + timedelta(days=6)
AllWikiRevDict = {}
MainMetricList = []

for idx, line in enumerate(main_metric_reader):
	print idx
	line['NewEditorSet'] = [str(item.encode('utf-8')) for item in json.loads(line['NewEditorSet'])]
	if DatestampToDate(line['StartDate']) > CurrStartDate:
		# read allwikirev into AllWikiRevDict until CurrStartDate + 6 days
		while DatestampToDate(all_wiki_line['Date']) <= CurrEndDate:
			UpdateAllWikiDict(all_wiki_line, AllWikiRevDict)
			try:
				all_wiki_line = all_wiki_reader.next()
			except:
				break
		TrimAllWikiDict(CurrStartDate, AllWikiRevDict)
		GetSpillover(AllWikiRevDict, MainMetricList)
		for _ in range(len(MainMetricList)):
			writer.writerow(MainMetricList.pop(0))
		CurrStartDate = DatestampToDate(line['StartDate'])
		CurrEndDate = CurrStartDate + timedelta(days=6)
	MainMetricList.append(line)