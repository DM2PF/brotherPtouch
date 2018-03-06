import os
import argparse
import binascii


def mirrorBits(byte):
	return chr(int(format(int(binascii.hexlify(byte), 16), '09b')[8:0:-1], 2))


class Image:
	def __init__(self, imagedata):

		rawwidth = ''
		rawlength = ''

		n = 3	# set start character of bitmap file for parsing

		while imagedata[n] != ' ':
			rawwidth += imagedata[n]
			n += 1
		width = int(rawwidth)

		while imagedata[n] != '\n':
			rawlength += imagedata[n]
			n += 1

		self.length = int(rawlength)
		self.pixeldata = imagedata[n+1:]
		self.width_bytes = width / 8


class PtData:
	def __init__(self, imagedata):
		self.imagedata = imagedata

	def create(self):
		image = Image(self.imagedata)

		self.data = '\x00' * 100
		self.data += '\x1B@'
		self.data += '\x1BiM\x40'
		self.data += '\x1BiK\x09'
		self.data += 'M\x02'

		line = 0
		while line < image.length:
			startByte = line * image.width_bytes  
			endByte = line * image.width_bytes + image.width_bytes - 1

			paddingA = (16 - image.width_bytes) / 2  			# padding bytes from one side
			paddingB = 16 - image.width_bytes - paddingA 		# padding bytes from other side

			self.data += 'G\x11\x00\x0F'			# line initialization
			self.data += ('\x00' * paddingA)		# padding side A

			for j in image.pixeldata[endByte:startByte-1:-1]:		# read bytes for line in reverse order
				self.data += mirrorBits(j)							# add mirrored bits in bytes to print data

			self.data += ('\x00' * paddingB)		# padding side B

			line += 1

		self.data += '\x00\x1A'

	def getData(self):
		return self.data


def main():
	ptData = PtData(open('output.pbm', 'rb').read())
	ptData.create()
	datafile = open('printfile.prn', 'wb').write(ptData.getData())


if __name__ == '__main__':
	main()