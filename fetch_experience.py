# generate a csv file recording an article's number of revision, number of editor, Gini, conflict
# input file is 'pol_aca_shock_id_and_date.csv'
import csv
from datetime import date, datetime, timedelta
from collections import Counter

def GetGini(s):
	# return normalized Gini coefficient
	if len(s) == 0:
		return -1
	elif len(s) == 1:
		return 1
	else:
		s.sort()
		res = 0
		n = len(s)
		for k in range(1,n):
			res = res + (s[k]-s[k-1])*k*(n-k)*2
		return res / 2.0 / len(s) / sum(s)

def GetNextWeekDayOne(s):
	return s + timedelta(days=7)

def GetLastWeekDayOne(s):
	return s - timedelta(days=7)

def GetFirstWeekDayOne(s, shock_date):
	t = shock_date
	while t > s:
		t = t - timedelta(days=7)
	return t

def TimestampToDatestamp(ts):
	return datetime.strptime(ts, '%Y-%m-%dT%H:%M:%SZ').date()

# read articleid and shock_date
shock_id_reader = csv.reader(open('pol_aca_shock_id_and_date.csv', 'r'))
shock_dict = {}
header = True
for row in shock_id_reader:
	if not header:
		shock_dict[row[0]] = datetime.strptime(row[1], "%Y-%m-%d").date()
	else:
		header = False

# import bot list
bot_reader = csv.reader(open('bot_list.csv', 'r'))
bot_set = set()
for row in bot_reader:
	bot_set.add(row[0])

HistoryAddr = 'pol_aca_history.csv'
HistoryFile = open(HistoryAddr, 'rb')
HistoryReader = csv.DictReader(HistoryReader)

RevisionFile = open('revision_by_week.csv', 'wb')
fieldnames = [
	'ArticleId',
	'Date',
	'NumRev',
	'NumEditor',
	'NumRevNew',
	'NumEditorNew',
	'Gini',
	'NumRevert',
	'NumRevertNew']
RevisionWriter = csv.DictWriter(RevisionFile, fieldnames)
RevisionWriter.writeheader()

ArticleId = ''
NextWeekDayOne = ''
# mapping editor to previous number of revisions
EditorPrevNumRevMap = Counter()
# mapping editor to number of revisions
EditorNumRevMap = Counter()
# mapping editor to previous number of reverts
EditorPrevNumRevertMap = Counter()
# mapping editor to number of reverts
EditorNumRevertMap = Counter()


for idx, line in enumerate(HistoryReader):
	print idx
	if line['ArticleId'] != ArticleId:
		# write records for previous article
		row = {}
		row['ArticleId'] = ArticleId
		row['Date'] = GetLastWeekDayOne(NextWeekDayOne)
		row['NumRev'] = sum(EditorNumRevMap.values())
		row['NumEditor'] = len(EditorNumRevMap)
		row['NumRevNew'] = sum(
			[0 if key in EditorPrevNumRevMap else EditorNumRevMap[key] for key in EditorNumRevMap])
		row['NumEditorNew'] = sum(
			[0 if key in EditorPrevNumRevMap else 1 for key in EditorNumRevMap])
		row['Gini'] = getGini(EditorNumRevMap.values())
		row['NumRevert'] = sum(EditorNumRevertMap.values())
		row['NumRevertNew'] = sum(
			[0 if key in EditorPrevNumRevertMap else EditorNumRevertMap[key] for key in EditorNumRevertMap])
		RevisionWriter.writerow(row)
		# initialize for new article
		ArticleId = line['ArticleId']
		FirstWeekDayOne = GetFirstWeekDayOne(
			s=TimestampToDatestamp(line['Timestamp']),
			shock_date=shock_dict[line['ArticleId']])
		NextWeekDayOne = GetNextWeekDayOne(FirstWeekDayOne)
		EditorPrevNumRevMap = Counter()
		EditorNumRevMap = Counter()
		EditorPrevNumRevertMap = Counter()
		EditorNumRevertMap = Counter()
	else:
		# write records for previous week
		while TimestampToDatestamp(line['Timestamp']) >= NextWeekDayOne:
			row = {}
			row['ArticleId'] = ArticleId
			row['Date'] = GetLastWeekDayOne(NextWeekDayOne)
			row['NumRev'] = sum(EditorNumRevMap.values())
			row['NumEditor'] = len(EditorNumRevMap)
			row['NumRevNew'] = sum(
				[0 if key in EditorPrevNumRevMap else EditorNumRevMap[key] for key in EditorNumRevMap])
			row['NumEditorNew'] = sum(
				[0 if key in EditorPrevNumRevMap else 1 for key in EditorNumRevMap])
			row['Gini'] = getGini(EditorNumRevMap.values())
			row['NumRevert'] = sum(EditorNumRevertMap.values())
			row['NumRevertNew'] = sum(
				[0 if key in EditorPrevNumRevertMap else EditorNumRevertMap[key] for key in EditorNumRevertMap])
			RevisionWriter.writerow(row)
			NextWeekDayOne = GetNextWeekDayOne(NextWeekDayOne)
			EditorPrevNumRevMap.update(EditorNumRevMap)
			EditorNumRevMap = Counter()
			EditorPrevNumRevertMap.update(EditorNumRevertMap)
			EditorNumRevertMap = Counter()

	# process current line of revision
	if line['Contributor'] in EditorNumRevMap:
		if ('bot' not in line['Contributor']
				and 'Bot' not in line['Contributor']
				and 'BOT' not in line['Contributor']
				and line['Contributor'] not in bot_set):
			EditorNumRevMap[line['Contributor']] += 1
			if line['RevertId'] != '-1':
				EditorNumRevertMap[line['Contributor']] += 1
			else:
				EditorNumRevertMap[line['Contributor']] += 0
	else:
		if ('bot' not in line['Contributor']
				and 'Bot' not in line['Contributor']
				and 'BOT' not in line['Contributor']
				and line['Contributor'] not in bot_set):
			EditorNumRevMap[line['Contributor']] = 1
			if line['RevertId'] != '-1':
				EditorNumRevertMap[line['Contributor']] = 1
			else:
				EditorNumRevertMap[line['Contributor']] = 0

HistoryFile.close()
RevisionFile.close()
