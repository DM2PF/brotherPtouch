import os
import argparse
import csv
import ptprint

trenner64 = 'inline:data:image/pbm;base64,UDQKNjQgMQqAAAAAAAAAAQo='

def createLabel(row1, row2, row3, length, name):
	if length == 1:
		lengthPx = 120
	elif length == 2 | length == 3:
		lengthPx = 235
	else:
		print('Invalid label size')
		sys.exit()	

	# Einzelne Schriftzuege erstellen
	os.system('convert +antialias -background white -fill black -size x24 -gravity center -bordercolor black -border 1 -font /usr/share/fonts/truetype/msttcorefonts/arialbd.ttf -pointsize 22 label:"' + row1 + '" top.pbm')
	if row2 != '':
		os.system('convert +antialias -background white -fill black -size x20 -gravity center -bordercolor black -border 0 -trim -font /usr/share/fonts/truetype/msttcorefonts/arialbd.ttf -pointsize 20 label:"' + row2 + '" mid.pbm')
	if row3 != '':
		os.system('convert +antialias -background white -fill black -size x20 -gravity center -bordercolor black -border 0 -trim -font /usr/share/fonts/truetype/msttcorefonts/arialbd.ttf -pointsize 20 label:"' + row3 + '" bot.pbm')


	os.system('convert -size ' +str(lengthPx)+ 'x64 canvas:white canvas.pbm')				# Canvas erstellen

	if os.path.exists('mid.pbm'):
		os.system('composite -gravity center -geometry +0+7 mid.pbm canvas.pbm canvas.pbm')	# Mittelteil drauf
	if os.path.exists('bot.pbm'):
		os.system('composite -gravity south bot.pbm canvas.pbm canvas.pbm')					# Unterer Teil drauf
	os.system('composite -gravity north top.pbm canvas.pbm canvas.pbm')						# Oberer Teil drauf
	
	os.system('convert -rotate 90 canvas.pbm "'+name+'"')									# drehen und umbenennen

	# aufraeumen
	os.system('rm top.pbm')
	if os.path.exists('bot.pbm'):
		os.system('rm bot.pbm')
	if os.path.exists('mid.pbm'):
		os.system('rm mid.pbm')
	os.system('rm canvas.pbm')



parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input-csv', action='store', default='input.csv',
	help='File name of the .csv file with the label data. Needs to have 3 columns. Default: input.csv')
parser.add_argument('-s', '--size', action='store', default='3',
	help='Length of the label. 1 fits for ESD boxes No. 1. 2 and 3 for Boxes No. 2 and 3. Default: 3')
parser.add_argument('-p', '--printfile', action='store_true',
	help='Generates a .prn file for brother prtiners from the generated bitmap')

args = parser.parse_args()

# Label creation from csv
with open(args.input_csv, 'rb') as csvfile:
	csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')

	i=1
	for row in csvreader:
		createLabel(row[0], row[1], row[2], int(args.size), str(i)+'.pbm')
		i = i+1

# Merge the labels
os.system('mv 1.pbm output.pbm')
if i > 1:
	for j in xrange(2, i):
		os.system('convert output.pbm "' + trenner64 + '" ' + str(j) + '.pbm -append output.pbm')
		os.system('rm ' + str(j) + '.pbm')		# aufraeumen

# Generate printfile
if args.printfile:
	ptData = ptprint.PtData(open('output.pbm', 'rb').read())
	ptData.create()
	open('printfile.prn', 'wb').write(ptData.getData())
