#!/bin/sh

# now running this as a daemon
cd /var/www/radio/server

# use the `rpi.conf` file that's packaged with the zip file
./current/bin/alradio -Dconfig.resource=rpi.conf -J-Xms64M -J-Xmx128M

