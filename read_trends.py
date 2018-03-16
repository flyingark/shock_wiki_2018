# generate csv file recording trends of each article in each month or each day

import csv
import json
from datetime import datetime, date

if True:
	fin = open('pol_trends_with_wiki_id_and_summary_clean.tsv', 'rb')
	f_reader = csv.reader(fin, delimiter = '\t')

	fout = open('pol_trends_data.csv', 'wb')
	f_writer = csv.writer(fout, delimiter = ',')
	f_writer.writerow(['scholar_name', 'scholar_profession', 'date', 'trends', 'articleid'])

	flog = open('pol_trends_data.log', 'wb')

	for idx, line in enumerate(f_reader):
		print line[0], line[1]
		if line[2] == "<type 'exceptions.KeyError'>":
			flog.write(line[0] + '\t' + line[1] + '\t' + 'KeyError' + '\n')
		elif line[2] == "<type 'exceptions.ValueError'>":
			flog.write(line[0] + '\t' + line[1] + '\t' + 'ValueError' + '\n')
		else:
			try:
				trend_dict = json.loads(line[2])
				for key, value in trend_dict.values()[0].items():
					if datetime.utcfromtimestamp(int(key) / 1000) >= datetime(year = 2008, month = 1, day = 1):
						f_writer.writerow(
							[line[0], line[1], datetime.utcfromtimestamp(int(key) / 1000), value, line[5]]
						)
				flog.write(line[0] + '\t' + line[1] + '\t' + 'successful' + '\n')
			except:
				flog.write(line[0] + '\t' + line[1] + '\t' + 'OtherError' + '\n')

	fin.close()
	fout.close()

else:
	fin = open('trends_shock_daily.tsv', 'rb')
	f_reader = csv.reader(fin, delimiter = '\t')

	fout = open('trends_data_at_shockmonth.csv', 'wb')
	f_writer = csv.writer(fout, delimiter = ',')
	f_writer.writerow(['scholar_name', 'scholar_profession', 'date', 'trends', 'articleid'])

	for idx, line in enumerate(f_reader):
		print line[0], line[1]
		if line[2] == "<type 'exceptions.KeyError'>":
			continue
		elif line[2] == "<type 'exceptions.ValueError'>":
			continue
		else:
			try:
				trend_dict = json.loads(line[3])
				for key, value in trend_dict.values()[0].items():
					if datetime.utcfromtimestamp(int(key) / 1000) >= datetime(year = 2008, month = 1, day = 1):
						f_writer.writerow(
							[line[1], line[2], datetime.utcfromtimestamp(int(key) / 1000), value, line[0]]
						)
			except:
				continue

	fin.close()
	fout.close()
