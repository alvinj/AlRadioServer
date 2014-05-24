Stream Recording Scripts
========================

These are the scripts I used to record online radio streams on
the Raspberry Pi with the `streamripper` utility.

The scripts are run through crontab entries like these:

    #--------------------------------------------------
    # min,hour,dayOfMonth,month,dayOfWeek command
    #
    # field          allowed values
    # -----          --------------
    # minute         0-59
    # hour           0-23
    # day of month   1-31
    # month          1-12 (or names, see below)
    # day of week    0-7 (0 or 7 is Sun, or use names)
    #--------------------------------------------------
    
    # espn (mike+mike at 6am and 7am)
    0 6 * * * /var/www/radio/data/recordings/espn.sh  > /var/www/radio/logs/espn.log 2>&1
    0 7 * * * /var/www/radio/data/recordings/espn.sh  > /var/www/radio/logs/espn.log 2>&1
    
    # 104.3 (drew, sandy, and scott)
    0 12 * * * /var/www/radio/data/recordings/104_3.sh  > /var/www/radio/logs/104_3.log 2>&1
    0 13 * * * /var/www/radio/data/recordings/104_3.sh  > /var/www/radio/logs/104_3.log 2>&1

(I only record the first two hours of each show, but could record all three hours.)


To-Do
-----

1 The scripts can be refactored a little bit to put the date, directory, and command
  in one "common.sh" file.

