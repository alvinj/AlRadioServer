#!/usr/bin/python

import feedparser
import time
from subprocess import check_output
import sys

#feed_name = 'TRIBUNE'
#url = 'http://chicagotribune.feedsportal.com/c/34253/f/622872/index.rss'

feed_name = sys.argv[1]
url = sys.argv[2]

db = '/var/www/radio/data/screensaver/feeds.db'
limit = 12 * 3600 * 1000

#
# function to get the current time
#
current_time_millis = lambda: int(round(time.time() * 1000))
current_timestamp = current_time_millis()

def post_is_in_db(title):
    with open(db, 'r') as database:
        for line in database:
            if title in line:
                return True
    return False

# return true if the title is in the database with a timestamp > limit
def post_is_in_db_with_old_timestamp(title):
    with open(db, 'r') as database:
        for line in database:
            if title in line:
                ts_as_string = line.split('|', 1)[1]
                ts = long(ts_as_string)
                if current_timestamp - ts > limit:
                    return True
    return False

# see https://docs.python.org/2/howto/unicode.html
def clean_string(string):
    return string.encode('ascii', 'ignore').strip()
    #return string.encode('utf-8').strip()  #old

#
# get the feed data from the url
#
feed = feedparser.parse(url)

#
# figure out which posts to print
#
posts_to_print = []
posts_to_skip = []

for post in feed.entries:
    # if post is already in the database, skip it
    # TODO check the time
    title = clean_string(post.title)
    if post_is_in_db_with_old_timestamp(title):
        posts_to_skip.append(title)
    else:
        posts_to_print.append(title)
    
#
# add all the posts we're going to print to the database with the current timestamp
# (but only if they're not already in there)
#
f = open(db, 'a')
for title in posts_to_print:
    title_cleaned = clean_string(title)
    if not post_is_in_db(title_cleaned):
        f.write(title_cleaned + "|" + str(current_timestamp) + "\n")
f.close
    
#
# output all of the new posts
#
count = 1
blockcount = 1
for title in posts_to_print:
    if count % 5 == 1:
        print("\n" + '((( ' + feed_name + ' - ' + str(blockcount) + ' )))')
        print("-------------------\n")
        blockcount += 1
    title_cleaned = clean_string(title)
    print(title_cleaned + "\n")
    count += 1

ipAddr = check_output(["hostname", "-I"])
print "\n"
print '---------------------------------'
print 'IP Address: ' + ipAddr.strip()
print '---------------------------------'
print "\n"


