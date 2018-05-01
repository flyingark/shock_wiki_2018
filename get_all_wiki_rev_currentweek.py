# generate a csv file recording an article's editors' retention over all
# wikipedianumber of revision,

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
	if Date not in AllWikiRevDict[Editor]:
		AllWikiRevDict[Editor][Date] = 0
	AllWikiRevDict[Editor][Date] += 1
	AllWikiRevDict[Editor]["NumRev"] += 1

def TrimAllWikiDict(CurrRetentionStartDate, AllWikiRevDict):
	"""remove revisions before CurrRetentionStartDate"""
	for Editor, NumRevDict in AllWikiRevDict.iteritems():
		for Date in NumRevDict.keys():
			if Date < CurrRetentionStartDate.toordinal():
				NumRevDict["NumRev"] -= NumRevDict.pop(Date)

def UpdatePrevNumAllWikiDict(AllWikiRevDict):
	"""Update PrevNumRev in the AllWikiRevDict"""
	for Editor, NumRevDict in AllWikiRevDict.iteritems():
		NumRevDict["PrevNumRev"] += NumRevDict["NumRev"]

def GetRetention(AllWikiRevDict, MainMetricList):
	# go through main metric list and calculate retention 
	for item in MainMetricList:
		EditorRetenRevList = []
		for Editor in list(set(item['PreShockEditorSet'] + item['PostShockEditorSet'] + item['NewEditorSet'])):
			if Editor in AllWikiRevDict:
				EditorRetenRevList.append(AllWikiRevDict[Editor]['NumRev'])
			else:
				EditorRetenRevList.append(0)
		item['SumEditorAllWiki'] = np.sum(EditorRetenRevList)
		item['MeanEditorAllWiki'] = np.mean(EditorRetenRevList)
		item['MedEditorAllWiki'] = np.median(EditorRetenRevList)
		item['LogMeanEditorAllWiki'] = np.mean(np.log(np.array(EditorRetenRevList) + 1))
		
		OldEditorRetenRevList = []
		for Editor in list(set(item['PreShockEditorSet'] + item['PostShockEditorSet'])):
			if Editor in AllWikiRevDict:
				OldEditorRetenRevList.append(AllWikiRevDict[Editor]['NumRev'])
			else:
				OldEditorRetenRevList.append(0)
		item['SumOldEditorAllWiki'] = np.sum(OldEditorRetenRevList)
		item['MeanOldEditorAllWiki'] = np.mean(OldEditorRetenRevList)
		item['MedOldEditorAllWiki'] = np.median(OldEditorRetenRevList)
		item['LogMeanOldEditorAllWiki'] = np.mean(np.log(np.array(OldEditorRetenRevList) + 1))
		
		NewEditorRetenRevList = []
		for Editor in item['NewEditorSet']:
			if Editor in AllWikiRevDict:
				NewEditorRetenRevList.append(AllWikiRevDict[Editor]['NumRev'])
			else:
				NewEditorRetenRevList.append(0)
		item['SumNewEditorAllWiki'] = np.sum(NewEditorRetenRevList)
		item['MeanNewEditorAllWiki'] = np.mean(NewEditorRetenRevList)
		item['MedNewEditorAllWiki'] = np.median(NewEditorRetenRevList)
		item['LogMeanNewEditorAllWiki'] = np.mean(np.log(np.array(NewEditorRetenRevList) + 1))
		
		PreShockEditorRetenRevList = []
		for Editor in item['PreShockEditorSet']:
			if Editor in AllWikiRevDict:
				PreShockEditorRetenRevList.append(AllWikiRevDict[Editor]['NumRev'])
			else:
				PreShockEditorRetenRevList.append(0)
		item['SumPreShockAllWiki'] = np.sum(PreShockEditorRetenRevList)
		item['MeanPreShockAllWiki'] = np.mean(PreShockEditorRetenRevList)
		item['MedPreShockAllWiki'] = np.median(PreShockEditorRetenRevList)
		item['LogMeanPreShockAllWiki'] = np.mean(np.log(np.array(PreShockEditorRetenRevList) + 1))
		
		PostShockEditorRetenRevList = []
		for Editor in item['PostShockEditorSet']:
			if Editor in AllWikiRevDict:
				PostShockEditorRetenRevList.append(AllWikiRevDict[Editor]['NumRev'])
			else:
				PostShockEditorRetenRevList.append(0)
		item['SumPostShockAllWiki'] = np.sum(PostShockEditorRetenRevList)
		item['MeanPostShockAllWiki'] = np.mean(PostShockEditorRetenRevList)
		item['MedPostShockAllWiki'] = np.median(PostShockEditorRetenRevList)
		item['LogMeanPostShockAllWiki'] = np.mean(np.log(np.array(PostShockEditorRetenRevList) + 1))
		
		NewWikiRetenRevList = []
		for Editor in item['NewWikiEditorSet']:
			if Editor in AllWikiRevDict:
				NewWikiRetenRevList.append(AllWikiRevDict[Editor]['NumRev'])
			else:
				NewWikiRetenRevList.append(0)
		item['SumNewWikiAllWiki'] = np.sum(NewWikiRetenRevList)
		item['MeanNewWikiAllWiki'] = np.mean(NewWikiRetenRevList)
		item['MedNewWikiAllWiki'] = np.median(NewWikiRetenRevList)
		item['LogMeanNewWikiAllWiki'] = np.mean(np.log(np.array(NewWikiRetenRevList) + 1))
		
		NewNonWikiRetenRevList = []
		for Editor in list(set(item['NewEditorSet']) - set(item['NewWikiEditorSet'])):
			if Editor in AllWikiRevDict:
				NewNonWikiRetenRevList.append(AllWikiRevDict[Editor]['NumRev'])
			else:
				NewNonWikiRetenRevList.append(0)
		item['SumNewNonWikiAllWiki'] = np.sum(NewNonWikiRetenRevList)
		item['MeanNewNonWikiAllWiki'] = np.mean(NewNonWikiRetenRevList)
		item['MedNewNonWikiAllWiki'] = np.median(NewNonWikiRetenRevList)
		item['LogMeanNewNonWikiAllWiki'] = np.mean(np.log(np.array(NewNonWikiRetenRevList) + 1))

		NewEditorPrevList = []
		# a list recording the fraction of editor's revision in the current week relative to previous revisions
		for Editor in item['NewEditorSet']:
			if Editor in AllWikiRevDict:
				NewEditorPrevList.append((1 + AllWikiRevDict[Editor]['NumRev']) / (1 + AllWikiRevDict[Editor]['PrevNumRev']))
			else:
				NewEditorPrevList.append(0)
		item['MeanNewEditorCurrPrevRatio'] = np.mean(NewEditorPrevList)
		item['MedNewEditorCurrPrevRatio'] = np.median(NewEditorPrevList)
		item['LogMeanNewEditorCurrPrevRatio'] = np.mean(np.log(np.array(NewEditorPrevList) + 1))

main_metric_reader = csv.DictReader(open('../data/all_treated_editor_set_sort_by_date.csv', 'r'))
all_wiki_reader = csv.DictReader(open('../data/history_all_wikipedia_sort_by_date.csv', 'r'))
all_wiki_line = all_wiki_reader.next()
writer = csv.DictWriter(open('../data/main_metric_sort_by_date_rev_currentweek.csv', 'wb'),
	fieldnames=['ArticleId', 'RelWeek',
				'SumEditorAllWiki',
				'SumOldEditorAllWiki',
				'SumNewEditorAllWiki',
				'SumPreShockAllWiki',
				'SumPostShockAllWiki',
				'SumNewWikiAllWiki',
				'SumNewNonWikiAllWiki',
				'MeanEditorAllWiki',
				'MeanOldEditorAllWiki',
				'MeanNewEditorAllWiki',
				'MeanPreShockAllWiki',
				'MeanPostShockAllWiki',
				'MeanNewWikiAllWiki',
				'MeanNewNonWikiAllWiki',
				'MedEditorAllWiki',
				'MedOldEditorAllWiki',
				'MedNewEditorAllWiki',
				'MedPreShockAllWiki',
				'MedPostShockAllWiki',
				'MedNewWikiAllWiki',
				'MedNewNonWikiAllWiki',
				'LogMeanEditorAllWiki',
				'LogMeanOldEditorAllWiki',
				'LogMeanNewEditorAllWiki',
				'LogMeanPreShockAllWiki',
				'LogMeanPostShockAllWiki',
				'LogMeanNewWikiAllWiki',
				'LogMeanNewNonWikiAllWiki',
				'MeanNewEditorCurrPrevRatio',
				'MedNewEditorCurrPrevRatio',
				'LogMeanNewEditorCurrPrevRatio'],
	extrasaction='ignore')
writer.writeheader()

CurrStartDate = date(2000,1,1)
CurrEndDate = CurrStartDate + timedelta(days=6)
CurrRetentionStartDate = CurrStartDate
CurrRetentionEndDate = CurrStartDate + timedelta(days=6)
AllWikiRevDict = {}
MainMetricList = []

for idx, line in enumerate(main_metric_reader):
	print idx
	line['NewEditorSet'] = [str(item.encode('utf-8')) for item in json.loads(line['NewEditorSet'])]
	line['PreShockEditorSet'] = [str(item.encode('utf-8')) for item in json.loads(line['PreShockEditorSet'])]
	line['PostShockEditorSet'] = [str(item.encode('utf-8')) for item in json.loads(line['PostShockEditorSet'])]
	line['NewWikiEditorSet'] = [str(item.encode('utf-8')) for item in json.loads(line['NewWikiEditorSet'])]
	if DatestampToDate(line['StartDate']) > CurrStartDate:
		# read allwikirev into AllWikiRevDict until CurrStartDate + 6 days
		while DatestampToDate(all_wiki_line['Date']) <= CurrRetentionEndDate:
			UpdateAllWikiDict(all_wiki_line, AllWikiRevDict)
			try:
				all_wiki_line = all_wiki_reader.next()
			except:
				break
		TrimAllWikiDict(CurrRetentionStartDate, AllWikiRevDict)
		GetRetention(AllWikiRevDict, MainMetricList)
		UpdatePrevNumAllWikiDict(AllWikiRevDict)
		for _ in range(len(MainMetricList)):
			writer.writerow(MainMetricList.pop(0))
		CurrStartDate = DatestampToDate(line['StartDate'])
		CurrEndDate = CurrStartDate + timedelta(days=6)
		CurrRetentionStartDate = CurrStartDate
		CurrRetentionEndDate = CurrStartDate + timedelta(days=6)
	MainMetricList.append(line)