import os
import argparse
import csv

trenner64 = 'inline:data:image/pbm;base64,UDQKNjQgMQqAAAAAAAAAAQo='


parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input-csv', action='store', default='input.csv',
	help='File name of the .csv file with the label data. Needs to have 3 columns. Default: input.csv')
parser.add_argument('-s', '--size', action='store', default='3',
	help='Length of the label. 1 fits for ESD boxes No. 1. 2 and 3 for Boxes No. 2 and 3. Default: 3')

args = parser.parse_args()

# Label creation from csv
with open(args.input_csv, 'rb') as csvfile:
	csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')

	i=1
	for row in csvreader:
		os.system('sh esdbox3.sh "' + row[0] + '" "' + row[1] + '" "' + row[2] + '" ' + str(i) + '.pbm')
		i = i+1

# Merge the labels
os.system('mv 1.pbm output.pbm')
if i > 1:
	for j in xrange(2, i):
		os.system('convert output.pbm "' + trenner64 + '" ' + str(j) + '.pbm -append output.pbm')
		os.system('rm ' + str(j) + '.pbm')		# aufraeumen