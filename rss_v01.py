#
# example for using rss feed from cbnc
#
import feedparser as fp
import pandas as pd

# read URLs from excel file:
url_frame = pd.read_excel('Feeds.xlsx', skiprows=0, header=1)

# as an example RSS feeds from www.cnbc.com were used:
# cnbc_rss_feeds = dict([('earnings', 'https://www.cnbc.com/id/15839135/device/rss/rss.html'),
#                       ('finance', 'https://www.cnbc.com/id/10000664/device/rss/rss.html'),
#                       ('politics', 'https://www.cnbc.com/id/10000113/device/rss/rss.html')])
with open('cnbc_news.txt', 'a') as filehandle:
    for feed in cnbc_rss_feeds.values():
        tempfeed = fp.parse(feed)
        # get all titles and summaries:

        filehandle.write('FROM FEED: ' + feed + '\n')
        for i in range(len(tempfeed)):
            filehandle.write('*********************************************** \n' + tempfeed.entries[i].title + '\n')
            filehandle.write('SUMMARY: \n' + tempfeed.entries[i].summary + '\n')
            filehandle.write('published: ' + tempfeed.entries[i].published + '\n')


