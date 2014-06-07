#!/bin/sh

#
# this script copies the input file it's given, along with the latest
# stock data, to the text file that's read by the screensaver.
# this script is intended to be called by crontab.
#
# $1 should be an input filename, like "/var/www/radio/data/tribune.out"
#

SCREENSAVER=/var/www/radio/data/screensaver.txt

cp $1 $SCREENSAVER

echo ""                     >> $SCREENSAVER
date +"%a, %b %d %I:%M %p"  >> $SCREENSAVER
echo "--------------------" >> $SCREENSAVER
echo ""                     >> $SCREENSAVER

cat /var/www/radio/data/stocks.out >> $SCREENSAVER

echo ""                     >> $SCREENSAVER
date +"%a, %b %d %I:%M %p"  >> $SCREENSAVER
echo "--------------------" >> $SCREENSAVER
echo ""                     >> $SCREENSAVER

