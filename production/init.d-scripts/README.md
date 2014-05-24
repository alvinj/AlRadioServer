init.d startup scripts
======================

This directory contains the startup scripts that should be copied
to the _/etc/init.d_ directory, and further be configured so they
will starup at boot time.

Installing the scripts
----------------------

The configuration process to use these scripts is this:

* Copy these scripts to the _/etc/init.d_ directory on the RPI (=sudo cp fmradio.sh /etc/init.d=)
* Test the scripts like this:

    sudo /etc/init.d/fmradio.sh start
    sudo /etc/init.d/fmradio.sh status
    sudo /etc/init.d/fmradio.sh stop

* To be sure, check that the process is running after issuing the `start` command by checking it with `ps`
  (=ps auxw | grep python= in this case)
* Install the script so it will be run at Linux boot time:

    sudo update-rc.d fmradio.sh defaults

* Check that the files/links are in the right places with this command:

    ls -l /etc/rc?.d/*fmradio.sh


Documentation
-------------

See this link for more documentation: http://blog.scphillips.com/2013/07/getting-a-python-script-to-run-in-the-background-as-a-service-on-boot/

That's where I got everything, including the source code for the startup scripts.


