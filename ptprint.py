import os
import argparse
import binascii

data = '\x00'*100
data = data + "\x1B@"
data = data + "\x1BiM\x40"
data = data + "\x1BiK\x09"
data = data + "M\x02"

image = ''

length = 0
width = 0

image = open('output.pbm', 'rb').read()

n = 3
rawwidth = ''
rawlength = ''

while image[n] != ' ':
	rawwidth = rawwidth + image[n]
	n = n+1

width = int(rawwidth)

while image[n] != '\n':
	rawlength = rawlength + image[n]
	n = n+1

length = int(rawlength)

n = n+1
pixeldata = image[n:]

print(str(n))


# read image line by line
line=0  # we start sending the pixel data line by line, starting from top going down 
image_start = 0
width_bytes = 8

while line<length:
	data_od=image_start+line*width_bytes # count the offset of first byte in current line
	data_po=image_start+line*width_bytes+width_bytes-1 # count the offset of last byte in current line

	paddingA=(16-width_bytes)/2  # padding bytes from one side
	paddingB=16-width_bytes-paddingA # padding bytes from other side

	# The printer expects the bits to be from right to left. So we need to reverse the byte order. Also we need to reverse each bit in every byte.
	# We always send 128 bits of image data per line. If there is narrow tape, not all pixels will be printed. Only the pixels in the center will be printed.
	# We try to center the image in the middle of the 128 bit (pixels). 
	# If the image width is less then 128bits we add pudding 00 bytes.
	print('DATA LENTH '+str(len(data)))
	data = data + "G\x11\x00\x0F" + ("\x00"*paddingA)

	for j in pixeldata[data_po:data_od-1:-1]:
		data = data + chr(int(format(int(binascii.hexlify(j), 16), '09b')[8:0:-1], 2))

	data = data + ("\x00"*paddingB)

	# If would go from button of the image to top, we would not need to reverse the bit's order. Then we would use the line below
	#data <<  "G\x11\x00\x0F"+"\x00"*paddingA+obrazek[data_od..data_po]+"\x00"*paddingB

	# sending uncopressed line does not work. I do not know why. My attempt is below
	#data <<  "g\x10\x00"+"\x00"*bytu_na_vycentrovani_L+obrazek[data_od..data_po].chars.map{|s| [s.unpack('b*')[0].reverse].pack('b*')}.join().reverse + "\x00"*bytu_na_vycentrovani_P


	line=line+1  # increase the line counter

data = data + '\x00\x1A'

datafile = open('datafile.prn', 'wb').write(data)