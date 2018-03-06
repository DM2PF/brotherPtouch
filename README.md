## brotherPtouch
Software that creates labels, especially for Warmbier ESD Boxes, and prints them on a Brother P-Touch label printer.
 
![ESD Boxes](https://github.com/DM2PF/brotherPtouch/raw/master/esdboxen-.jpg)

## Usage
It consists of two parts:

**batchlabel.py** creates a bitmap of labels from a CSV file

**ptprint.py** creates the print data file from a bitmap, which then can be sent to the printer via CUPS.

The actual print is started with `lp -d <Printer> printfile.prn`, where `<Printer>` is the printer's CUPS name.