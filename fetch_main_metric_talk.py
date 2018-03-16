# generate a csv file recording an article's number of revision,
# number of editor, Gini, conflict
from __future__ import division
import csv
from datetime import date, datetime, timedelta
from collections import Counter
import numpy as np

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

def GetEntropy(s):
	"""return information entropy"""
	if len(s) == 0:
		return ''
	else:
		s = [v/sum(s) for v in s]
		s = [v * np.log(v) for v in s]
		return -sum(s)

def GetNextWeekDayOne(s):
	"""return date object of 7 days later s"""
	return s + timedelta(days=7)

def GetLastWeekDayOne(s):
	"""return date object of 7 days before s"""
	return s - timedelta(days=7)

def GetFirstWeekDayOne(s, t):
	"""return the first date object before s that is 7x days before t"""
	while t > s:
		t = t - timedelta(days=7)
	return t

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

# ArticleShockDateMap: a dictionary mapping ArticleId to ShockDate
ArticleShockDateMap = {}
for line in csv.DictReader(open('shockdate_list.csv', 'r')):
	ArticleShockDateMap[line['TalkId']] = DatestampToDate(line['ShockDate'])

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
FileWriter = csv.DictWriter(
	open('main_metric_talk.csv', 'w'),
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
		'GiniNew',
		'GiniOld',
		'GiniAll'])
FileWriter.writeheader()

# initialize for new article
ArticleId = ''
RelWeek = 0
# OldEditorSet: a set recording old editors
OldEditorSet = set()
# NewEditorSet: a set recording new editors
NewEditorSet = set()
# EditorNumRevMap: mapping editor to number of revisions
EditorNumRevMap = Counter()

# traverse revision history and calculate metrics
for idx, line in enumerate(csv.DictReader(open('talk_history.csv', 'r'))):
	print idx
	if line['ArticleId'] != ArticleId:
		if idx != 0:
			# write metrics for previous article
			row = {}
			row['ArticleId'] = ArticleId
			row['RelWeek'] = RelWeek
			row['StartDate'] = (ArticleShockDateMap[ArticleId]
				+ timedelta(days=RelWeek * 7))
			row['NumRevNew'] = sum(
				IntersectDictSet(EditorNumRevMap, NewEditorSet).values())
			row['NumRevOld'] = sum(
				IntersectDictSet(EditorNumRevMap, OldEditorSet).values())
			row['NumRev'] = sum(EditorNumRevMap.values())
			row['NumEditorNew'] = len(
				IntersectDictSet(EditorNumRevMap, NewEditorSet).values())
			row['NumEditorOld'] = len(
				IntersectDictSet(EditorNumRevMap, OldEditorSet).values())
			row['NumEditor'] = len(EditorNumRevMap)
			row['GiniNew'] = GetGini(
				IntersectDictSet(EditorNumRevMap, NewEditorSet).values())
			row['GiniOld'] = GetGini(
				IntersectDictSet(EditorNumRevMap, OldEditorSet).values())
			row['GiniAll'] = GetGini(EditorNumRevMap.values())
			FileWriter.writerow(row)
		# initialize for new article
		ArticleId = line['ArticleId']
		RelWeek = ((TimestampToDate(line['Timestamp']) 
					- ArticleShockDateMap[line['ArticleId']])).days // 7
		OldEditorSet = set()
		NewEditorSet = set()
		EditorNumRevMap = Counter()
	else:
		# write records for previous week
		while (TimestampToDate(line['Timestamp']) 
				>= ArticleShockDateMap[line['ArticleId']]
				+ timedelta(days=RelWeek * 7 + 7)):
			row = {}
			row['ArticleId'] = ArticleId
			row['RelWeek'] = RelWeek
			row['StartDate'] = (ArticleShockDateMap[line['ArticleId']]
				+ timedelta(days=RelWeek * 7))
			row['NumRevNew'] = sum(
				IntersectDictSet(EditorNumRevMap, NewEditorSet).values())
			row['NumRevOld'] = sum(
				IntersectDictSet(EditorNumRevMap, OldEditorSet).values())
			row['NumRev'] = sum(EditorNumRevMap.values())
			row['NumEditorNew'] = len(
				IntersectDictSet(EditorNumRevMap, NewEditorSet).values())
			row['NumEditorOld'] = len(
				IntersectDictSet(EditorNumRevMap, OldEditorSet).values())
			row['NumEditor'] = len(EditorNumRevMap)
			row['GiniNew'] = GetGini(
				IntersectDictSet(EditorNumRevMap, NewEditorSet).values())
			row['GiniOld'] = GetGini(
				IntersectDictSet(EditorNumRevMap, OldEditorSet).values())
			row['GiniAll'] = GetGini(EditorNumRevMap.values())
			FileWriter.writerow(row)
			RelWeek = RelWeek + 1
			OldEditorSet.update(NewEditorSet)
			NewEditorSet.clear()
			EditorNumRevMap = Counter()
	# process current line of revision
	if IsBot(line['Contributor'], BotSet) == False:
		if line['Contributor'] not in OldEditorSet:
			NewEditorSet.add(line['Contributor'])
		if line['Contributor'] in EditorNumRevMap:
			EditorNumRevMap[line['Contributor']] += 1
		else:
			EditorNumRevMap[line['Contributor']] = 1
