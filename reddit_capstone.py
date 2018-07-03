from psaw import PushshiftAPI
import pandas as pd
import datetime as dt
import time

start_time = time.time()

api = PushshiftAPI()

SEARCH_LIMIT = 1000
MAX_ROWS = 1048000  # approx excel lim (for convenience)
MIN_COMMENTS = 1
start_epoch = int(dt.datetime(2016, 8, 2).timestamp())
END_EPOCH = int(dt.datetime(2017, 8, 2).timestamp())
print(time.strftime("%a %b %d %H:%M:%S %Z") + " -- Starting program...")

raw_fields = ['url','author', 'title', 'subreddit', 'created_utc', 'permalink', 'score', 'id', 'num_comments',
              'is_self', 'is_video', 'num_crossposts', 'over_18', 'whitelist_status', 'domain',
              'author_flair_text', 'author_flair_type', 'locked', 'media_only', 'pinned','body']

submissions = pd.DataFrame()

start_search = api.search_submissions(after=start_epoch, subreddit='news', filter=raw_fields, limit=SEARCH_LIMIT)
submissions = pd.DataFrame.from_dict(start_search) #.to_frame()
submissions = submissions["d_"].apply(pd.Series).dropna(subset=["created"])
start_epoch = int(submissions.loc[len(submissions)-1, "created"] + 1)
submissions = submissions[submissions["num_comments"]>=MIN_COMMENTS]

#116023
#missing:
#1488334783
#1488347494


while(True):
    search_results = api.search_submissions(after=start_epoch, subreddit='news', filter=raw_fields, limit=SEARCH_LIMIT)
    temp_submissions = pd.DataFrame.from_dict(search_results).loc[:,"d_"].to_frame()
    temp_submissions = temp_submissions["d_"].apply(pd.Series)
    start_epoch = int(temp_submissions.loc[len(temp_submissions)-1, "created"] + 1)
    temp_submissions = temp_submissions[temp_submissions["num_comments"]>=MIN_COMMENTS]
    if len(temp_submissions)>0:
        submissions = submissions.append(temp_submissions, ignore_index=True)  # add search results to dataset
    if len(submissions)>MAX_ROWS or start_epoch>=END_EPOCH:  # stopping condition?
        break
    print(start_epoch)
    print(len(submissions))  # to see progress

submissions.to_csv("reddit_news_20160802_1year_comments_utf8.csv", encoding = "utf-8")
submissions.to_csv("reddit_news_20160802_1year_comments.csv")

print(time.strftime("%a %b %d %H:%M:%S %Z"),
      " -- Done, elapsed time: ", str(time.time() - start_time))
