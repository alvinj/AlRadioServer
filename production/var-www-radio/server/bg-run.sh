#./current/bin/alradio -J-Xms64M -J-Xmx128M

# use the `rpi.conf` file that's packaged with the zip file

nohup ./current/bin/alradio -Dconfig.resource=rpi.conf -J-Xms64M -J-Xmx128M & > /var/www/radio/logs/play.log 2>&1

