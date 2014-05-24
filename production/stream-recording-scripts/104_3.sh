#!/bin/sh

date=`date +"%Y_%a_%b_%d_%H%M%P"`

url=http://4533.live.streamtheworld.com:80/KKFNFMAAC_SC
output_filename=104_3.${date}

duration=3600

# -----------------------
# don't change below here
# -----------------------

output_dir=/var/www/radio/data/recordings
cd $output_dir

streamripper $url -d $output_dir -l $duration -a $output_filename -o always


