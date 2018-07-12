from psaw import PushshiftAPI
import pandas as pd
import datetime as dt
import time

start_time = time.time()

api = PushshiftAPI()

SEARCH_LIMIT = 1000
MAX_ROWS = 1048000  # approx excel lim (for convenience)
MIN_COMMENTS = 1
OUT_CSV_NAME = "reddit_upliftingnews_2016_all.csv"
SUBREDDIT = "upliftingnews"
start_epoch = int(dt.datetime(2016, 1, 1).timestamp())
END_EPOCH = int(dt.datetime(2016, 12, 31).timestamp())
print(time.strftime("%a %b %d %H:%M:%S %Z") + " -- Starting program...")

raw_fields = ['url','author', 'title', 'subreddit', 'created_utc', 'permalink', 'score', 'id', 'num_comments','domain', 'locked']

submissions = pd.DataFrame()

start_search = api.search_submissions(after=start_epoch, subreddit=SUBREDDIT, filter=raw_fields, limit=SEARCH_LIMIT)
submissions = pd.DataFrame.from_dict(start_search) #.to_frame()
submissions = submissions["d_"].apply(pd.Series).dropna(subset=["created"])
start_epoch = int(submissions.loc[len(submissions)-1, "created"] + 1)
submissions = submissions[submissions["num_comments"]>=MIN_COMMENTS]

# TODO: create functions with date range as input (maybe try to fill missing data)

while(True):
    search_results = api.search_submissions(after=start_epoch, subreddit=SUBREDDIT, filter=raw_fields, limit=SEARCH_LIMIT)
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

submissions.to_csv(OUT_CSV_NAME)

print(time.strftime("%a %b %d %H:%M:%S %Z"),
      " -- Done, elapsed time: ", str(time.time() - start_time))
