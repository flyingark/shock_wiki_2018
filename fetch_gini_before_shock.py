# This code fetch the gini coefficient for articles in 1-8 weeks before the shock
# input file is 'pol_aca_shock_id_and_date.csv'

from __future__ import division
import csv
from datetime import datetime, date, timedelta
from collections import Counter
import numpy as np

# BotSet: a set recording bot accounts
BotSet = set()
for line in csv.DictReader(open('bot_list.csv', 'r')):
	BotSet.add(line['ArticleId'])

def IsBot(Editor, BotSet):
	# return whether an editor is a bot
	if ('bot' in Editor
			or 'Bot' in Editor
			or 'BOT' in Editor
			or Editor in BotSet):
		return True
	else:
		return False

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

def TimestampToDate(ts):
	"""convert timestamp to date object"""
	return datetime.strptime(ts, '%Y-%m-%dT%H:%M:%SZ').date()

def DatestampToDate(ds):
	"""convert datestamp to date object"""
	return datetime.strptime(ds, '%Y-%m-%d').date()

# ArticleShockDateMap: a dictionary mapping ArticleId to ShockDate
ArticleShockDateMap = {}
for line in csv.DictReader(open('shockdate_list.csv', 'r')):
	ArticleShockDateMap[line['ArticleId']] = DatestampToDate(line['ShockDate'])

# open output file
WinSize = 8
FileWriter = csv.DictWriter(
	open('gini_before.csv', 'w'),
	fieldnames=['ArticleId'] 
		+ [('Gini' + str(w+1) + 'WeekBefore') for w in range(WinSize)]
		+ [('Entropy' + str(w+1) + 'WeekBefore') for w in range(WinSize)])
FileWriter.writeheader()

# initialize for new article
ArticleId = ''
# EditorNumRevMapList: mapping editor to number of revisions
# e.g. EditorNumRevMapList[0] is 1 week before shock
# e.g. EditorNumRevMapList[WinSize-1] is WinSize weeks before shock
EditorNumRevMapList = [Counter() for _ in range(WinSize)]

# traverse revision history and calculate gini before
for idx, line in enumerate(csv.DictReader(open('revision_history.csv', 'r'))):
	print idx
	if line['ArticleId'] != ArticleId:
		if idx != 0:
			# write metrics for previous article
			row = {}
			row['ArticleId'] = ArticleId
			for w in range(WinSize):
				EditorNumCumulRevMap = reduce(
					lambda x,y: x+y, EditorNumRevMapList[:w+1])
				row[('Gini' + str(w+1) + 'WeekBefore')] = GetGini(
					EditorNumCumulRevMap.values())
				row[('Entropy' + str(w+1) + 'WeekBefore')] = GetEntropy(
					EditorNumCumulRevMap.values())
			FileWriter.writerow(row)
			# initialize for new article
		ArticleId = line['ArticleId']
		EditorNumRevMapList = [Counter() for _ in range(WinSize)]
	# process current line of revision
	RelWeek = ((TimestampToDate(line['Timestamp'])
		- ArticleShockDateMap[line['ArticleId']])).days // 7
	if RelWeek < 0 and RelWeek >= -WinSize:
		if IsBot(line['Contributor'], BotSet) == False:
			if line['Contributor'] in EditorNumRevMapList[-RelWeek-1]:
				EditorNumRevMapList[-RelWeek-1][line['Contributor']] += 1
			else:
				EditorNumRevMapList[-RelWeek-1][line['Contributor']] = 1
