#!/usr/bin/python

import feedparser
import time
import ystockquote
from subprocess import check_output

# ------
# uptime
# ------

uptime = check_output(['uptime'])
print "\n"
print '-------------------------------------------------------------'
print uptime.strip()
print '-------------------------------------------------------------'
print "\n\n"


# ---
# npr
# ---

d = feedparser.parse('http://www.npr.org/rss/rss.php?id=100')

count = 0
blockcount = 1
for post in d.entries:
    if count % 5 == 1:
        print "\n" + time.strftime("%a, %b %d %I:%M %p") + '  ((( NPR - ' + str(blockcount) + ' )))'
        print "-------------------------------------\n\n"
        blockcount += 1
    print post.title + "\n\n"
    count += 1
    if count > 15:
        break

# ---
# cnn
# ---

# 'most popular' rss feed
d = feedparser.parse('http://rss.cnn.com/rss/cnn_mostpopular.rss')

count = 0
blockcount = 1
for post in d.entries:
    if count % 5 == 1:
        print "\n" + time.strftime("%a, %b %d %I:%M %p") + '  ((( CNN - ' + str(blockcount) + ' )))'
        print "-------------------------------------\n"
        blockcount += 1
    print post.title + "\n\n"
    count += 1
    if count > 15:
        break


# ------------
# stock quotes
# ------------

#print "\n\n___ STOCK QUOTES ___\n"

#appl = ystockquote.get_price('AAPL')
#print 'Apple: ' + appl + "\n"

#att = ystockquote.get_price('T')
#print 'AT&T: ' + att + "\n"

#gtat = ystockquote.get_price('GTAT')
#print 'GTAT: ' + gtat + "\n"

#jcp = ystockquote.get_price('JCP')
#print 'JCP: ' + jcp + "\n"

#tsla = ystockquote.get_price('TSLA')
#print 'TSLA: ' + tsla + "\n\n"



