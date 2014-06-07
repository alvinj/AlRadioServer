#!/usr/bin/python

import feedparser
import time
from subprocess import check_output

# ------
# uptime
# ------

uptime = check_output(['uptime'])
print "\n"
print '-------------------------------------------------------------'
print uptime.strip()
print '-------------------------------------------------------------'
print "\n"


# -------
# tribune
# -------

d = feedparser.parse('http://chicagotribune.feedsportal.com/c/34253/f/622872/index.rss')

# print all posts 
count = 1
blockcount = 1
for post in d.entries:
    if count % 5 == 1:
        print "\n" + time.strftime("%a, %b %d %I:%M %p") + '  ((( TRIBUNE - ' + str(blockcount) + ' )))'
        print "-----------------------------------------\n"
        blockcount += 1
    print post.title + "\n"
    count += 1


