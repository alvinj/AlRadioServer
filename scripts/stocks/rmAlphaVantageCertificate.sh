
# use this script to delete the AlphaVantage CRT from the Java cacerts file
# they use "Let's Encrypt"
# keystore password is "changeit"
# need to run this command as root/sudo

keytool \
    -delete -alias "alphavantage.co" \
    -keystore /usr/lib/jvm/jdk-8-oracle-arm32-vfp-hflt/jre/lib/security/cacerts



