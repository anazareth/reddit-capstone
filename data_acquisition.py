from psaw import PushshiftAPI
import pandas as pd
import datetime as dt
import time


def main():
    start_time = time.time()
    init()
    get_submissions()
    print(time.strftime("%a %b %d %H:%M:%S %Z"),
          " -- Done, elapsed time: ", str(time.time() - start_time))


def init():
    global SEARCH_LIMIT, MAX_ROWS, MIN_COMMENTS, OUT_CSV_NAME, SUBREDDIT, START_EPOCH, END_EPOCH, RAW_FIELDS
    
    print(time.strftime("%a %b %d %H:%M:%S %Z") + " -- Starting program...")
    
    year = 2016
    days_delta = 365
    SUBREDDIT = "upliftingnews"
    
    SEARCH_LIMIT = 1000  # max number of rows returned per api request (max 1000)
    MAX_ROWS = 1048000  # approx excel lim (for convenience)
    MIN_COMMENTS = 1  # minimum comments for a submission to be downloaded (in an effort to filter out spam posts)
    START_EPOCH = int(dt.datetime(year, 1, 1).timestamp())
    END_EPOCH = START_EPOCH + days_delta*24*60*60  # days in seconds

    OUT_CSV_NAME = "reddit_" + SUBREDDIT + str(year) + "_" + str(days_delta) + ".csv"  # name of created CSV file
    
    RAW_FIELDS = ['url','author', 'title', 'subreddit', 'created_utc', 'permalink', 'score', 'id', 'num_comments','domain', 'locked']


def get_submissions():

    api = PushshiftAPI()

    submissions = pd.DataFrame()

    sub_name=SUBREDDIT
    search_lim = SEARCH_LIMIT
    fields = RAW_FIELDS
    min_comments = MIN_COMMENTS

    start_search = api.search_submissions(after=START_EPOCH, subreddit=sub_name, filter=fields, limit=search_lim)
    submissions = pd.DataFrame.from_dict(start_search) #.to_frame()
    submissions = submissions["d_"].apply(pd.Series).dropna(subset=["created"])
    start_epoch = int(submissions.loc[len(submissions)-1, "created"] + 1)
    submissions = submissions[submissions["num_comments"]>=min_comments]


    while len(submissions)<MAX_ROWS and start_epoch<END_EPOCH:
        search_results = api.search_submissions(after=start_epoch, subreddit=sub_name, filter=fields, limit=search_lim)
        temp_submissions = pd.DataFrame.from_dict(search_results).loc[:,"d_"].to_frame()
        temp_submissions = temp_submissions["d_"].apply(pd.Series)
        start_epoch = int(temp_submissions.loc[len(temp_submissions)-1, "created"] + 1)
        temp_submissions = temp_submissions[temp_submissions["num_comments"]>=min_comments]
        if len(temp_submissions)>0:
            submissions = submissions.append(temp_submissions, ignore_index=True)  # add search results to dataset
        print(start_epoch)
        print(len(submissions))  # to see progress

    #submissions.to_csv(OUT_CSV_NAME)


if __name__=="__main__":
    main()

