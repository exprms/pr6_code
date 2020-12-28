#
import pandas as pd
import feedparser as fp

url_frame = pd.read_excel('Feeds.xlsx', skiprows=0, header=1)
# feed = url_frame.URL[25]

# df_feeds = pd.DataFrame(data=None, columns=['date', 'title', 'summary', 'author', 'link'])
df_feeds_sm = pd.DataFrame(data=None, columns=['date', 'title', 'summary'])

for i in range(len(url_frame.URL)):
    tempfeed = fp.parse(url_frame.URL[i])
    #print(i)
    for j in range(len(tempfeed.entries)):
        try:
            val = tempfeed.entries[j].summary
        except:
            try:
                val = tempfeed.entries[j].value
            except:
                val = 'None'

        df2 = pd.DataFrame([[tempfeed.entries[j].published, tempfeed.entries[j].title, val]],
                           columns=['date', 'title', 'summary'])
        df_feeds_sm = df_feeds_sm.append(df2, ignore_index=True)

df_feeds_sm.to_csv('feeds.txt', sep='\t', index=False)

