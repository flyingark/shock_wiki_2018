# generate a csv file recording an article's number of revision,
# number of editor, Gini, conflict
# input file is 'pol_aca_shock_id_and_date.csv'
from __future__ import division
import csv
from datetime import date, datetime, timedelta
from collections import Counter
import numpy as np

# define whether TreatType is treated or control
TreatType = 'treated'

def GetGini(s):
	"""return normalized Gini coefficient"""
	if len(s) == 0:
		return ''
	elif len(s) == 1:
		return 1
	else:
		s.sort()
		res = 0
		n = len(s)
		for k in range(1,n):
			res = res + (s[k]-s[k-1])*k*(n-k)*2
		return res / len(s) / sum(s)

def TimestampToDate(ts):
	"""convert timestamp to date object"""
	return datetime.strptime(ts, '%Y-%m-%dT%H:%M:%SZ').date()

def DatestampToDate(ds):
	"""convert datestamp to date object"""
	return datetime.strptime(ds, '%Y-%m-%d').date()

def IntersectDictSet(d, s):
	"""return intersection between dictionary d and set s"""
	r = {}
	for k, v in d.iteritems():
		if k in s:
			r[k] = v
	return r

def SumValue(d):
	"""return sum of values in dictinary"""
	return sum(d.values())

# ArticleShockDateMap: a dictionary mapping ArticleId to ShockDate
ArticleShockDateMap = {}
for line in csv.DictReader(open(TreatType + '_info.csv', 'r')):
	ArticleShockDateMap[line['ArticleId']] = DatestampToDate(line['ShockDate'])

# BotSet: a set recording bot accounts
BotSet = set()
for line in csv.DictReader(open('bot_list.csv', 'r')):
	BotSet.add(line['Contributor'])

def IsBot(Editor, BotSet):
	# return whether an editor is a bot
	if ('bot' in Editor
			or 'Bot' in Editor
			or 'BOT' in Editor
			or Editor in BotSet):
		return True
	else:
		return False

# open output file
Writer = csv.DictWriter(
	open(TreatType + '_main_metric.csv', 'w'),
	fieldnames=[
		'ArticleId',
		'RelWeek',
		'StartDate',
		'NumRevNew',
		'NumRevOld',
		'NumRev',
		'NumEditorNew',
		'NumEditorOld',
		'NumEditor',
		'Gini',
		'NumRevertedNew',
		'NumRevertedOld',
		'NumRevertingNew',
		'NumRevertingOld'])
Writer.writeheader()

# initialize for new article
ArticleId = ''
RelWeek = 0
# OldEditorSet: a set recording old editors
OldEditorSet = set()
# NewEditorSet: a set recording new editors
NewEditorSet = set()
# EditorNumRevMap: mapping editor to number of revisions
EditorNumRevMap = Counter()
# EditorNumRevertedMap: mapping editor to number of reverteds
EditorNumRevertedMap = Counter()
# EditorNumRevertingMap: mapping editor to number of revertings
EditorNumRevertingMap = Counter()

# traverse revision history and calculate metrics
HistoryFile = open('../data/' + TreatType + '_history.csv', 'r')
for idx, line in enumerate(csv.DictReader(HistoryFile)):
	print idx
	if line['ArticleId'] != ArticleId:
		if idx != 0:
			# write metrics for previous article
			row = {}
			row['ArticleId'] = ArticleId
			row['RelWeek'] = RelWeek
			row['StartDate'] = (ArticleShockDateMap[ArticleId]
				+ timedelta(days=RelWeek * 7))
			row['NumRevNew'] = SumValue(
				IntersectDictSet(EditorNumRevMap, NewEditorSet))
			row['NumRevOld'] = SumValue(
				IntersectDictSet(EditorNumRevMap, OldEditorSet))
			row['NumRev'] = SumValue(EditorNumRevMap)
			row['NumEditorNew'] = len(
				IntersectDictSet(EditorNumRevMap, NewEditorSet))
			row['NumEditorOld'] = len(
				IntersectDictSet(EditorNumRevMap, OldEditorSet))
			row['NumEditor'] = len(EditorNumRevMap)
			row['Gini'] = GetGini(EditorNumRevMap.values())
			row['NumRevertedNew'] = SumValue(
				IntersectDictSet(EditorNumRevertedMap, NewEditorSet))
			row['NumRevertedOld'] = SumValue(
				IntersectDictSet(EditorNumRevertedMap, OldEditorSet))
			row['NumRevertingNew'] = SumValue(
				IntersectDictSet(EditorNumRevertingMap, NewEditorSet))
			row['NumRevertingOld'] = SumValue(
				IntersectDictSet(EditorNumRevertingMap, OldEditorSet))
			Writer.writerow(row)
		# initialize for new article
		ArticleId = line['ArticleId']
		RelWeek = ((TimestampToDate(line['Timestamp']) 
					- ArticleShockDateMap[line['ArticleId']])).days // 7
		OldEditorSet = set()
		NewEditorSet = set()
		EditorNumRevMap = Counter()
		EditorNumRevertedMap = Counter()
		EditorNumRevertingMap = Counter()
	else:
		# write records for previous week
		while (TimestampToDate(line['Timestamp']) 
				>= ArticleShockDateMap[line['ArticleId']]
				+ timedelta(days=RelWeek * 7 + 7)):
			rrow = {}
			row['ArticleId'] = ArticleId
			row['RelWeek'] = RelWeek
			row['StartDate'] = (ArticleShockDateMap[ArticleId]
				+ timedelta(days=RelWeek * 7))
			row['NumRevNew'] = SumValue(
				IntersectDictSet(EditorNumRevMap, NewEditorSet))
			row['NumRevOld'] = SumValue(
				IntersectDictSet(EditorNumRevMap, OldEditorSet))
			row['NumRev'] = SumValue(EditorNumRevMap)
			row['NumEditorNew'] = len(
				IntersectDictSet(EditorNumRevMap, NewEditorSet))
			row['NumEditorOld'] = len(
				IntersectDictSet(EditorNumRevMap, OldEditorSet))
			row['NumEditor'] = len(EditorNumRevMap)
			row['Gini'] = GetGini(EditorNumRevMap.values())
			row['NumRevertedNew'] = SumValue(
				IntersectDictSet(EditorNumRevertedMap, NewEditorSet))
			row['NumRevertedOld'] = SumValue(
				IntersectDictSet(EditorNumRevertedMap, OldEditorSet))
			row['NumRevertingNew'] = SumValue(
				IntersectDictSet(EditorNumRevertingMap, NewEditorSet))
			row['NumRevertingOld'] = SumValue(
				IntersectDictSet(EditorNumRevertingMap, OldEditorSet))
			Writer.writerow(row)
			RelWeek = RelWeek + 1
			OldEditorSet.update(NewEditorSet)
			NewEditorSet.clear()
			EditorNumRevMap = Counter()
			EditorNumRevertedMap = Counter()
			EditorNumRevertingMap = Counter()
	# process current line of revision
	if IsBot(line['Contributor'], BotSet) == False:
		if line['Contributor'] not in OldEditorSet:
			NewEditorSet.add(line['Contributor'])
		if line['Contributor'] in EditorNumRevMap:
			EditorNumRevMap[line['Contributor']] += 1
			if line['RevertedId'] != '-1':
				EditorNumRevertedMap[line['Contributor']] += 1
			else:
				EditorNumRevertedMap[line['Contributor']] += 0
			if line['RevertingId'] != '-1':
				EditorNumRevertingMap[line['Contributor']] += 1
			else:
				EditorNumRevertingMap[line['Contributor']] += 0
		else:
			EditorNumRevMap[line['Contributor']] = 1
			if line['RevertedId'] != '-1':
				EditorNumRevertedMap[line['Contributor']] = 1
			else:
				EditorNumRevertedMap[line['Contributor']] = 0
			if line['RevertingId'] != '-1':
				EditorNumRevertingMap[line['Contributor']] = 1
			else:
				EditorNumRevertingMap[line['Contributor']] = 0
