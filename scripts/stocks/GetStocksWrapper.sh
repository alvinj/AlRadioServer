#!/bin/sh

PATH=~/bin/scala-2.12.4/bin:$PATH

cd /var/www/radio/scripts/stocks

/var/www/radio/scripts/stocks/GetStocks.sh > /var/www/radio/data/stocks.out


