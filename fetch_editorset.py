# generate a csv file recording an article's new editor set, old editor set
from __future__ import division
import csv
import json
from datetime import date, datetime, timedelta
from collections import Counter
import numpy as np

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
for line in csv.DictReader(open('../data/all_treated_info.csv', 'r')):
	ArticleShockDateMap[line['ArticleId']] = DatestampToDate(line['ShockDate'])

# BotSet: a set recording bot accounts
BotSet = set()
for line in csv.DictReader(open('../data/bot_list.csv', 'r')):
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
	open('../data/all_treated_editor_set.csv', 'w'),
	fieldnames=[
		'ArticleId',
		'RelWeek',
		'StartDate',
		'EndDate',
		'RetentionEndDate',
		'NewEditorSet',
		'PreShockEditorSet',
		'PostShockEditorSet',
		'NewWikiEditorSet'])
Writer.writeheader()

# read information on when an editor joins wikipedia
EditorJoinMap = {}
JoinFile = open('../data/editor_set.csv', 'r')
for idx, line in enumerate(csv.DictReader(JoinFile)):
	print idx
	if line['Editor'] not in EditorJoinMap:
		EditorJoinMap[line['Editor']] = {'JoinDate': DatestampToDate(line['JoinDate'])}

# initialize for new article
ArticleId = ''
RelWeek = 0
# OldEditorSet: a set recording old editors
OldEditorSet = set()
# NewEditorSet: a set recording new editors
NewEditorSet = set()
# PreShockEditorSet: a set recording old editors who contributed befor shock
PreShockEditorSet = set()
# NewWikiEditorSet: a set recording editors who are new to both Wiki and article
NewWikiEditorSet = set()
# EditorNumRevMap: mapping editor to number of revisions
EditorNumRevMap = Counter()

# traverse revision history and calculate set
HistoryFile = open('../data/treated_history.csv', 'r')
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
			row['EndDate'] = (ArticleShockDateMap[ArticleId]
				+ timedelta(days=(RelWeek * 7 + 6)))
			row['RetentionEndDate'] = (ArticleShockDateMap[ArticleId]
				+ timedelta(days=(RelWeek * 7 + 28 + 6)))
			row['NewEditorSet'] = json.dumps(list(NewEditorSet))
			row['PreShockEditorSet'] = json.dumps(list(
				(set(EditorNumRevMap.keys()) - NewEditorSet) & PreShockEditorSet))
			row['PostShockEditorSet'] = json.dumps(list(
				(set(EditorNumRevMap.keys()) - NewEditorSet) - PreShockEditorSet))
			row['NewWikiEditorSet'] = json.dumps(list(NewWikiEditorSet))
			Writer.writerow(row)
		# initialize for new article
		ArticleId = line['ArticleId']
		RelWeek = ((TimestampToDate(line['Timestamp']) 
					- ArticleShockDateMap[line['ArticleId']])).days // 7
		OldEditorSet = set()
		NewEditorSet = set()
		PreShockEditorSet = set()
		NewWikiEditorSet = set()
		EditorNumRevMap = Counter()
	else:
		# write records for previous week
		while (TimestampToDate(line['Timestamp']) 
				>= ArticleShockDateMap[line['ArticleId']]
				+ timedelta(days=RelWeek * 7 + 7)):
			row = {}
			row['ArticleId'] = ArticleId
			row['RelWeek'] = RelWeek
			row['StartDate'] = (ArticleShockDateMap[ArticleId]
				+ timedelta(days=RelWeek * 7))
			row['EndDate'] = (ArticleShockDateMap[ArticleId]
				+ timedelta(days=(RelWeek * 7 + 6)))
			row['RetentionEndDate'] = (ArticleShockDateMap[ArticleId]
				+ timedelta(days=(RelWeek * 7 + 28 + 6)))
			row['NewEditorSet'] = json.dumps(list(NewEditorSet))
			row['PreShockEditorSet'] = json.dumps(list(
				(set(EditorNumRevMap.keys()) - NewEditorSet) & PreShockEditorSet))
			row['PostShockEditorSet'] = json.dumps(list(
				(set(EditorNumRevMap.keys()) - NewEditorSet) - PreShockEditorSet))
			row['NewWikiEditorSet'] = json.dumps(list(NewWikiEditorSet))
			Writer.writerow(row)
			RelWeek = RelWeek + 1
			OldEditorSet.update(NewEditorSet)
			NewEditorSet.clear()
			NewWikiEditorSet.clear()
			if RelWeek <= 0:
				PreShockEditorSet = set(OldEditorSet)
			EditorNumRevMap = Counter()
	# process current line of revision
	if IsBot(line['Contributor'], BotSet) == False:
		if line['Contributor'] not in OldEditorSet:
			NewEditorSet.add(line['Contributor'])
		if (EditorJoinMap[line['Contributor']]['JoinDate'] == TimestampToDate(line['Timestamp'])):
			NewWikiEditorSet.add(line['Contributor'])
		if line['Contributor'] in EditorNumRevMap:
			EditorNumRevMap[line['Contributor']] += 1
		else:
			EditorNumRevMap[line['Contributor']] = 1