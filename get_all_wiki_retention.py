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

def GetRetention(AllWikiRevDict, MainMetricList):
	# go through main metric list and calculate retention 
	for item in MainMetricList:
		OldEditorRetenRevList = []
		for Editor in list(set(item['PreShockEditorSet'] + item['PostShockEditorSet'])):
			if Editor in AllWikiRevDict:
				OldEditorRetenRevList.append(AllWikiRevDict[Editor]['NumRev'])
			else:
				OldEditorRetenRevList.append(0)
		item['SumOldEditorRetenAllWiki'] = np.sum(OldEditorRetenRevList)
		item['MeanOldEditorRetenAllWiki'] = np.mean(OldEditorRetenRevList)
		item['MedOldEditorRetenAllWiki'] = np.median(OldEditorRetenRevList)
		item['LogMeanOldEditorRetenAllWiki'] = np.mean(np.log(np.array(OldEditorRetenRevList) + 1))
		
		NewEditorRetenRevList = []
		for Editor in item['NewEditorSet']:
			if Editor in AllWikiRevDict:
				NewEditorRetenRevList.append(AllWikiRevDict[Editor]['NumRev'])
			else:
				NewEditorRetenRevList.append(0)
		item['SumNewEditorRetenAllWiki'] = np.sum(NewEditorRetenRevList)
		item['MeanNewEditorRetenAllWiki'] = np.mean(NewEditorRetenRevList)
		item['MedNewEditorRetenAllWiki'] = np.median(NewEditorRetenRevList)
		item['LogMeanNewEditorRetenAllWiki'] = np.mean(np.log(np.array(NewEditorRetenRevList) + 1))

		PreShockEditorRetenRevList = []
		for Editor in item['PreShockEditorSet']:
			if Editor in AllWikiRevDict:
				PreShockEditorRetenRevList.append(AllWikiRevDict[Editor]['NumRev'])
			else:
				PreShockEditorRetenRevList.append(0)
		item['SumPreShockRetenAllWiki'] = np.sum(PreShockEditorRetenRevList)
		item['MeanPreShockRetenAllWiki'] = np.mean(PreShockEditorRetenRevList)
		item['MedPreShockRetenAllWiki'] = np.median(PreShockEditorRetenRevList)
		item['LogMeanPreShockRetenAllWiki'] = np.mean(np.log(np.array(PreShockEditorRetenRevList) + 1))

		PostShockEditorRetenRevList = []
		for Editor in item['PostShockEditorSet']:
			if Editor in AllWikiRevDict:
				PostShockEditorRetenRevList.append(AllWikiRevDict[Editor]['NumRev'])
			else:
				PostShockEditorRetenRevList.append(0)
		item['SumPostShockRetenAllWiki'] = np.sum(PostShockEditorRetenRevList)
		item['MeanPostShockRetenAllWiki'] = np.mean(PostShockEditorRetenRevList)
		item['MedPostShockRetenAllWiki'] = np.median(PostShockEditorRetenRevList)
		item['LogMeanPostShockRetenAllWiki'] = np.mean(np.log(np.array(PostShockEditorRetenRevList) + 1))
		
		NewWikiRetenRevList = []
		for Editor in item['NewWikiEditorSet']:
			if Editor in AllWikiRevDict:
				NewWikiRetenRevList.append(AllWikiRevDict[Editor]['NumRev'])
			else:
				NewWikiRetenRevList.append(0)
		item['SumNewWikiRetenAllWiki'] = np.sum(NewWikiRetenRevList)
		item['MeanNewWikiRetenAllWiki'] = np.mean(NewWikiRetenRevList)
		item['MedNewWikiRetenAllWiki'] = np.median(NewWikiRetenRevList)
		item['LogMeanNewWikiRetenAllWiki'] = np.mean(np.log(np.array(NewWikiRetenRevList) + 1))
		
		NewNonWikiRetenRevList = []
		for Editor in list(set(item['NewEditorSet']) - set(item['NewWikiEditorSet'])):
			if Editor in AllWikiRevDict:
				NewNonWikiRetenRevList.append(AllWikiRevDict[Editor]['NumRev'])
			else:
				NewNonWikiRetenRevList.append(0)
		item['SumNewNonWikiRetenAllWiki'] = np.sum(NewNonWikiRetenRevList)
		item['MeanNewNonWikiRetenAllWiki'] = np.mean(NewNonWikiRetenRevList)
		item['MedNewNonWikiRetenAllWiki'] = np.median(NewNonWikiRetenRevList)
		item['LogMeanNewNonWikiRetenAllWiki'] = np.mean(np.log(np.array(NewNonWikiRetenRevList) + 1))

main_metric_reader = csv.DictReader(open('../data/all_treated_editor_set_sort_by_date.csv', 'r'))
all_wiki_reader = csv.DictReader(open('../data/history_all_wikipedia_sort_by_date.csv', 'r'))
all_wiki_line = all_wiki_reader.next()
writer = csv.DictWriter(open('../data/all_treated_allwikireten_currentweek.csv', 'wb'),
						fieldnames=['ArticleId', 'RelWeek',
									'SumOldEditorRetenAllWiki',
									'SumNewEditorRetenAllWiki',
									'SumPreShockRetenAllWiki',
									'SumPostShockRetenAllWiki',
									'SumNewWikiRetenAllWiki',
									'SumNewNonWikiRetenAllWiki',
									'MeanOldEditorRetenAllWiki',
									'MeanNewEditorRetenAllWiki',
									'MeanPreShockRetenAllWiki',
									'MeanPostShockRetenAllWiki',
									'MeanNewWikiRetenAllWiki',
									'MeanNewNonWikiRetenAllWiki',
									'MedOldEditorRetenAllWiki',
									'MedNewEditorRetenAllWiki',
									'MedPreShockRetenAllWiki',
									'MedPostShockRetenAllWiki',
									'MedNewWikiRetenAllWiki',
									'MedNewNonWikiRetenAllWiki',
									'LogMeanOldEditorRetenAllWiki',
									'LogMeanNewEditorRetenAllWiki',
									'LogMeanPreShockRetenAllWiki',
									'LogMeanPostShockRetenAllWiki',
									'LogMeanNewWikiRetenAllWiki',
									'LogMeanNewNonWikiRetenAllWiki'],
						extrasaction='ignore')
writer.writeheader()

CurrStartDate = date(2000,1,1)
CurrEndDate = CurrStartDate + timedelta(days=6)
CurrRetentionStartDate = CurrStartDate + timedelta(days=7)
CurrRetentionEndDate = CurrStartDate + timedelta(days=34)
AllWikiRevDict = {}
MainMetricList = []

for idx, line in enumerate(main_metric_reader):
	print idx
	line['NewEditorSet'] = [str(item.encode('utf-8')) for item in json.loads(line['NewEditorSet'])]
	line['PreShockEditorSet'] = [str(item.encode('utf-8')) for item in json.loads(line['PreShockEditorSet'])]
	line['PostShockEditorSet'] = [str(item.encode('utf-8')) for item in json.loads(line['PostShockEditorSet'])]
	line['NewWikiEditorSet'] = [str(item.encode('utf-8')) for item in json.loads(line['NewWikiEditorSet'])]
	if DatestampToDate(line['StartDate']) > CurrStartDate:
		# read allwikirev into AllWikiRevDict until CurrStartDate + 34 days
		while DatestampToDate(all_wiki_line['Date']) <= CurrRetentionEndDate:
			UpdateAllWikiDict(all_wiki_line, AllWikiRevDict)
			try:
				all_wiki_line = all_wiki_reader.next()
			except:
				break
		TrimAllWikiDict(CurrRetentionStartDate, AllWikiRevDict)
		GetRetention(AllWikiRevDict, MainMetricList)
		for _ in range(len(MainMetricList)):
			writer.writerow(MainMetricList.pop(0))
		CurrStartDate = DatestampToDate(line['StartDate'])
		CurrEndDate = CurrStartDate + timedelta(days=6)
		CurrRetentionStartDate = CurrStartDate + timedelta(days=7)
		CurrRetentionEndDate = CurrStartDate + timedelta(days=34)
	MainMetricList.append(line)