
# use this script to add the AlphaVantage CRT to the Java cacerts file
# they use "Let's Encrypt"
# keystore password is "changeit"
# need to run this command as root/sudo
# see this page for good information on the process:
# https://support.cloudbees.com/hc/en-us/articles/217078498-PKIX-path-building-failed-error-message

keytool \
    -import \
    -alias "alphavantage.co" \
    -keystore /usr/lib/jvm/jdk-8-oracle-arm32-vfp-hflt/jre/lib/security/cacerts \
    -file wwwalphavantageco.crt

