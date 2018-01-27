#!/bin/sh

PATH=~/bin/scala-2.12.4/bin:$PATH

cd /var/www/radio/scripts

./GetFeed.sh $1 $2    2> /dev/null


