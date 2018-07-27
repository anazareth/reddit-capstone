from psaw import PushshiftAPI
import pandas as pd
import datetime as dt
import time


def main():
    start_time = time.time()
    
    for subreddit in ['upliftingnews', 'news', 'worldnews']:
        for year in [2015, 2016, 2017]:
            init(year, subreddit)
            print(time.strftime("%a %b %d %H:%M:%S %Z") + " -- Collecting all " + str(year) + " submissions from /r/" + subreddit + "...")
            get_submissions(subreddit)
    print(time.strftime("%a %b %d %H:%M:%S %Z"),
          " -- Done, elapsed time: ", str(time.time() - start_time))


def init(year, subreddit):
    global SEARCH_LIMIT, MAX_ROWS, MIN_COMMENTS, OUT_CSV_NAME, SUBREDDIT, START_EPOCH, END_EPOCH, RAW_FIELDS
    
    print(time.strftime("%a %b %d %H:%M:%S %Z") + " -- Starting program...")
    
    START_EPOCH = int(dt.datetime(year, 1, 1).timestamp())
    days_delta = 365
    END_EPOCH = START_EPOCH + days_delta*24*60*60  # days in seconds
    SEARCH_LIMIT = 1000  # max number of rows returned per api request (max 1000)
    MIN_COMMENTS = 1  # minimum comments for a submission to be downloaded (in an effort to filter out spam posts)
    
    OUT_CSV_NAME = subreddit + str(year) + "_" + str(days_delta) + "_"+ str(MIN_COMMENTS) +"com0scr.csv"  # name of created CSV file
    
    RAW_FIELDS = ['url','author', 'title', 'subreddit', 'id', 'permalink', 'score', 'num_comments','domain']


def get_submissions(sub_name):

    api = PushshiftAPI()

    submissions = pd.DataFrame()

    search_lim = SEARCH_LIMIT
    fields = RAW_FIELDS
    min_comments = MIN_COMMENTS

    start_search = api.search_submissions(after=START_EPOCH, subreddit=sub_name, filter=fields, limit=search_lim)
    submissions = pd.DataFrame.from_dict(start_search) #.to_frame()
    submissions = submissions["d_"].apply(pd.Series).dropna(subset=["created"])
    start_epoch = int(submissions.loc[len(submissions)-1, "created"] + 1)
    submissions = submissions[submissions["num_comments"]>=min_comments]


    while start_epoch<END_EPOCH:
        search_results = api.search_submissions(after=start_epoch, subreddit=sub_name, filter=fields, limit=search_lim)
        temp_submissions = pd.DataFrame.from_dict(search_results).loc[:,"d_"].to_frame()
        temp_submissions = temp_submissions["d_"].apply(pd.Series)
        start_epoch = int(temp_submissions.loc[len(temp_submissions)-1, "created"] + 1)
        temp_submissions = temp_submissions[temp_submissions["num_comments"]>=min_comments]
        if len(temp_submissions)>0:
            submissions = submissions.append(temp_submissions, ignore_index=True)  # add search results to dataset
    submissions.to_csv("C:\\Users\\zande\\Documents\\Ryerson\\Capstone\\Data\\Raw\\" + OUT_CSV_NAME)
    print(time.strftime("%a %b %d %H:%M:%S %Z") + " -- File " + OUT_CSV_NAME + " saved successfully with " + str(len(submissions)) + " rows.")



if __name__=="__main__":
    main()

