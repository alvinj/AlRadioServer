
# this is the script i use to run the play server on the rpi.
# this script is located in /var/www/radio/server.
#
# this script assumes there is a subdirectory named `current` that contains the
# current play application. in practice i have `current` set up as a
# symbolic link to the current play folder, which is currently named
# something like `alradio-1.0-SNAPSHOT`.

# use the `rpi.conf` file that's packaged with the zip file
./current/bin/alradio -Dconfig.resource=rpi.conf -J-Xms64M -J-Xmx128M

