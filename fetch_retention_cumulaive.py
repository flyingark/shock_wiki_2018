# generate a csv file recording retention with date identified at day level
# the analysis is performed at week level

import csv
from datetime import date, datetime, timedelta
import numpy as np

# import bot list
bot_reader = csv.reader(open('bot_list.csv', 'r'))
bot_set = set()
for row in bot_reader:
	bot_set.add(row[0])

# read articleid and shock_date
shock_id_reader = csv.reader(open('pol_aca_shock_id_and_date.csv', 'r'))
shock_dict = {}
header = True
for row in shock_id_reader:
	if not header:
		shock_dict[row[0]] = datetime.strptime(row[1], "%Y-%m-%d").date()
	else:
		header = False

# read wikipedia data
history_file = open("pol_aca_history.csv", 'rb')
history_reader = csv.DictReader(history_file)

# write retention file. lapse = week * 2. For example, look at cumulative retention in 5 weeks, lapse=10
lapse = 4
retention_file = open( "pol_aca_cumulative_retention" + str(lapse/2) + "weeks.csv", 'wb' )
retention_writer = csv.writer( retention_file, delimiter = '\t' )
firstrow = ["join_week_rel_to_shock",
			"articleid",
			"shock_date",
			"num_revision_by_newcomer",
			"num_revision_by_oldcomer",
			"num_revision_norm_by_total",
			"num_editor_newcomer",
			"num_editor_oldcomer",
			"num_editor_norm_by_total",
			"num_revision_by_newcomer_noweek0",
			"num_revision_by_oldcomer_noweek0"
			"num_revision_norm_by_total_noweek0",
			"num_editor_newcomer_noweek0",
			"num_editor_oldcomer_noweek0",
			"num_editor_norm_by_total_noweek0",
			"avg_num_bytes_by_newcomer",
			"avg_num_bytes_by_oldcomer",
			"avg_num_bytes_norm_by_total",
			"avg_num_bytes_by_newcomer_noweek0",
			"avg_num_bytes_by_oldcomer_noweek0",
			"avg_num_bytes_norm_by_total_noweek0"]
retention_writer.writerow(firstrow)

curr_id = ""
curr_is_shock = False
curr_shock_date = ""
# main a list of dictionary recording the revisions of newcomers in 4 weeks
preveditors = set()
newcomers = [{} for _ in range(2*lapse+1)]
alleditor_list = [set() for _ in range(4*lapse+1)]
totaledits = [0 for _ in range(4*lapse+1)]
bytes_by_newcomers = [{} for _ in range(2*lapse+1)]
bytes_by_all = [0 for _ in range(4*lapse+1)]

for idx, line in enumerate(history_reader):
	print idx
	if line['ArticleId'] != curr_id:
		if curr_is_shock:
			for i in range(0,lapse/2+1)+range(lapse,lapse+lapse/2+1):
				row = [i-lapse, curr_id, curr_shock_date]
				
				# week [i,i+lapse/2-1] revision normalized by entire week revision for editors who join in week i
				lst = [sum(newcomers[i][key][0:(lapse/2)]) for key in newcomers[i]]
				row.append(sum(lst))
				row.append(sum(totaledits[i:(i+lapse/2)]) - sum(lst))
				if sum(totaledits[i:(i+lapse/2)]) == 0:
					row.append(-1)
				else:
					row.append(sum(lst)*1.0 / sum(totaledits[i:(i+lapse/2)]))
				
				# among all editors in week [i,i+lapse/2-1], what is the fraction of those who join in week i
				lst = [max(newcomers[i][key][0:(lapse/2)]) / max(max(newcomers[i][key][0:(lapse/2)]), 1) for key in newcomers[i]]
				alleditor_set = set()
				for k in range(0,lapse/2):
					alleditor_set = set(list(alleditor_set) + list(alleditor_list[i+k]))
				row.append(sum(lst))
				row.append(len(alleditor_set))
				if len(alleditor_set) == 0:
					row.append(-1)
				else:
					row.append(sum(lst)*1.0 / len(alleditor_set))

				# week (i,i+lapse/2-1] revision normalized by entire week revision for editors who join in week i
				lst = [sum(newcomers[i][key][1:(lapse/2)]) for key in newcomers[i]]
				row.append(sum(lst))
				row.append(sum(totaledits[(i+1):(i+lapse/2)]) - sum(lst))
				if sum(totaledits[(i+1):(i+lapse/2)]) == 0:
					row.append(-1)
				else:
					row.append(sum(lst)*1.0 / sum(totaledits[(i+1):(i+lapse/2)]))
				
				# among all editors in week (i,i+lapse/2-1], what is the fraction of those who join in week i
				lst = [max(newcomers[i][key][1:(lapse/2)]) / max(max(newcomers[i][key][1:(lapse/2)]), 1) for key in newcomers[i]]
				alleditor_set = set()
				for k in range(1,lapse/2):
					alleditor_set = set(list(alleditor_set) + list(alleditor_list[i+k]))
				row.append(sum(lst))
				row.append(len(alleditor_set))
				if len(alleditor_set) == 0:
					row.append(-1)
				else:
					row.append(sum(lst)*1.0 / len(alleditor_set))

				# week [i,i+lapse/2-1] bytes normalized by entire week bytes for editors who join in week i
				lst = [sum(bytes_by_newcomers[i][key][0:(lapse/2)]) for key in bytes_by_newcomers[i]]
				row.append(sum(lst))
				row.append(sum(bytes_by_all[i:(i+lapse/2)]) - sum(lst))
				if sum(bytes_by_all[i:(i+lapse/2)]) == 0:
					row.append(-1)
				else:
					row.append(sum(lst)*1.0 / sum(bytes_by_all[i:(i+lapse/2)]))
				
				# week (i,i+lapse/2-1] bytes normalized by entire week bytes for editors who join in week i
				lst = [sum(bytes_by_newcomers[i][key][1:(lapse/2)]) for key in bytes_by_newcomers[i]]
				row.append(sum(lst))
				row.append(sum(bytes_by_all[(i+1):(i+lapse/2)]) - sum(lst))
				if sum(bytes_by_all[(i+1):(i+lapse/2)]) == 0:
					row.append(-1)
				else:
					row.append(sum(lst)*1.0 / sum(bytes_by_all[(i+1):(i+lapse/2)]))

				retention_writer.writerow(row)

		curr_id = line['ArticleId']
		if curr_id in shock_dict:
			curr_is_shock = True
			curr_shock_date = shock_dict[curr_id]
		else:
			curr_is_shock = False
			curr_shock_date = ""
		preveditors = set()
		newcomers = [{} for _ in range(2*lapse+1)]
		alleditor_list = [set() for _ in range(4*lapse+1)]
		totaledits = [0 for _ in range(4*lapse+1)]
		bytes_by_newcomers = [{} for _ in range(2*lapse+1)]
		bytes_by_all = [0 for _ in range(4*lapse+1)]

	if (curr_is_shock
			and (
				(("bot" not in line['Contributor'])
					and ("Bot" not in line['Contributor'])
					and ("BOT" not in line['Contributor']))
				and (line['Contributor'] not in bot_set))):
		d = datetime.strptime(line['Timestamp'], "%Y-%m-%dT%H:%M:%SZ").date()
		gap = d - shock_dict[curr_id]
		gap = gap.days / 7
		if gap < -lapse:
			preveditors.add(line['Contributor'])
		elif gap >= -lapse and gap <= 0:
			if line['Contributor'] not in preveditors:
				newcomers[gap+lapse][line['Contributor']] = [1] + [0] * lapse * 2
				if line['BytesDiff'] != '':
					bytes_by_newcomers[gap+lapse][line['Contributor']] = [abs(int(line['BytesDiff']))] + [0] * lapse * 2
				else:
					bytes_by_newcomers[gap+lapse][line['Contributor']] = [0] + [0] * lapse * 2
				preveditors.add(line['Contributor'])
			else:
				# find whether the editor's first revision occurs in [shock_date-lapse,shock_date+gap]
				k = -lapse
				while k <= gap:
					if line['Contributor'] in newcomers[k+lapse]:
						newcomers[k+lapse][line['Contributor']][gap-k] += 1
						if line['BytesDiff'] != '':
							bytes_by_newcomers[k+lapse][line['Contributor']][gap-k] += abs(int(line['BytesDiff']))
						else:
							bytes_by_newcomers[k+lapse][line['Contributor']][gap-k] += 0
						break
					k = k + 1
			alleditor_list[gap+lapse].add(line['Contributor'])
			totaledits[gap+lapse] = totaledits[gap+lapse] + 1
			if line['BytesDiff'] != '':
				bytes_by_all[gap+lapse] += abs(int(line['BytesDiff']))
		elif gap > 0 and gap <= lapse:
			if line['Contributor'] not in preveditors:
				newcomers[gap+lapse][line['Contributor']] = [1] + [0] * lapse * 2
				if line['BytesDiff'] != '':
					bytes_by_newcomers[gap+lapse][line['Contributor']] = [abs(int(line['BytesDiff']))] + [0] * lapse * 2
				else:
					bytes_by_newcomers[gap+lapse][line['Contributor']] = [0] + [0] * lapse * 2
				preveditors.add(line['Contributor'])
			else:
				k = -lapse
				while k <= gap:
					if line['Contributor'] in newcomers[k+lapse]:
						newcomers[k+lapse][line['Contributor']][gap-k] += 1
						if line['BytesDiff'] != '':
							bytes_by_newcomers[k+lapse][line['Contributor']][gap-k] += abs(int(line['BytesDiff']))
						else:
							bytes_by_newcomers[k+lapse][line['Contributor']][gap-k] += 0
						break
					k = k + 1
			alleditor_list[gap+lapse].add(line['Contributor'])
			totaledits[gap+lapse] = totaledits[gap+lapse] + 1
			if line['BytesDiff'] != '':
				bytes_by_all[gap+lapse] += abs(int(line['BytesDiff']))
		elif gap > lapse and gap <= 3*lapse:
			if line['Contributor'] not in preveditors:
				preveditors.add(line['Contributor'])
			else:
				k = -lapse
				while k <= lapse:
					if line['Contributor'] in newcomers[k+lapse]:
						if gap-k <= 2*lapse:
							newcomers[k+lapse][line['Contributor']][gap-k] += 1
							if line['BytesDiff'] != '':
								bytes_by_newcomers[k+lapse][line['Contributor']][gap-k] += abs(int(line['BytesDiff']))
							else:
								bytes_by_newcomers[k+lapse][line['Contributor']][gap-k] += 0
						break
					k = k + 1
			alleditor_list[gap+lapse].add(line['Contributor'])
			totaledits[gap+lapse] = totaledits[gap+lapse] + 1
			if line['BytesDiff'] != '':
				bytes_by_all[gap+lapse] += abs(int(line['BytesDiff']))

history_file.close()
retention_file.close()
