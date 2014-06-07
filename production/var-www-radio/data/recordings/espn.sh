#!/bin/sh

date=`date +"%m%d_%a_%H%M%P"`

url=http://173.193.205.96:8158
output_filename=espn.${date}

# seconds
duration=3600

# --------------------------------
# don't change anything below here
# --------------------------------

output_dir=/var/www/radio/data/recordings
cd $output_dir

streamripper $url -d $output_dir -l $duration -a $output_filename -o always


