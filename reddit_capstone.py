
import praw

reddit = praw.Reddit(client_id='g5qzmJVgbIiCuQ', client_secret='Ec3E8iQ0yTbZ_GAuZO0g_Z4exyo',
                     password='PasswordPrivacy101', user_agent='testscript by /u/alex_nazareth',
                     username='alex_nazareth')

news = reddit.subreddit('news')

print(news.display_name)
