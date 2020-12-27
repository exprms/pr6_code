#
# example for using rss feed from cbnc
#

import feedparser as fp

newsfeed = fp.parse('https://www.cnbc.com/id/15839135/device/rss/rss.html')

# get all titles and sumarys:
for i in range(len(newsfeed)):
    print('TITLE: \n' + newsfeed.entries[i].title)
    print('SUMMARY: \n' + newsfeed.entries[i].summary)
