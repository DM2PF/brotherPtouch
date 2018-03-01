
# 4 Argumente: 3 Zeilen + 1 ausgabe
convert  +antialias  -background white -fill black  -size x24 -gravity center -bordercolor black -border 1 -font /usr/share/fonts/truetype/msttcorefonts/arialbd.ttf -pointsize 22 label:"$1" top.pbm
convert  +antialias  -background white -fill black  -size x20 -gravity center -bordercolor black -border 0 -trim -font /usr/share/fonts/truetype/msttcorefonts/arialbd.ttf -pointsize 20 label:"$2" mid.pbm
convert  +antialias  -background white -fill black  -size x20 -gravity center -bordercolor black -border 0 -trim -font /usr/share/fonts/truetype/msttcorefonts/arialbd.ttf -pointsize 20 label:"$3" bot.pbm

# Assemble the shit
convert -size 235x64 canvas:white canvas.pbm
composite -gravity center -geometry +0+7 mid.pbm canvas.pbm canvas.pbm
composite -gravity south bot.pbm canvas.pbm canvas.pbm
composite -gravity north top.pbm canvas.pbm canvas.pbm
convert -rotate 90 canvas.pbm "$4"

# clean up	
rm top.pbm
rm bot.pbm
rm mid.pbm
rm canvas.pbm