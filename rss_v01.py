#
# example for using rss feed from cbnc
#

import feedparser as fp

# as an example RSS feeds from www.cnbc.com were used:
cnbc_rss_feeds = dict([('earnings', 'https://www.cnbc.com/id/15839135/device/rss/rss.html'),
                       ('finance', 'https://www.cnbc.com/id/10000664/device/rss/rss.html'),
                       ('politics', 'https://www.cnbc.com/id/10000113/device/rss/rss.html')])

for feed in cnbc_rss_feeds.values():
    tempfeed = fp.parse(feed)

    # get all titles and summaries:
    print('FROM FEED: ' + feed)
    for i in range(len(tempfeed)):
        print('*********************************************** \n' + tempfeed.entries[i].title)
        print('SUMMARY: \n' + tempfeed.entries[i].summary)
