import os
import sys
from dotenv import load_dotenv
import praw
import pandas as pd

#Load environment variable from .env
dotenv_path =os.path.join(os.path.dirname(__file__),"..",".env")
load_dotenv(dotenv_path)

# Options for extracting data from PRAW
SUBREDDIT = "valueinvesting+stocks"
LIMIT = 15
TIME_FILTER = "day"

def reddit_api ():
    #Connect to Reddit's API through PRAW
    try:
        reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            user_agent=os.getenv("REDDIT_USER_AGENT"),
            username=os.getenv("REDDIT_USERNAME"),
        )
    except Exception as e:
        print(f"Unable to connect to API. Error: {e}")
        sys.exit(1)
    return reddit

def get_subreddit_posts(reddit):
    #Get Subreddit Posts Object (PRAW Submission Class)
    try:
        subreddit_posts = reddit.subreddit(SUBREDDIT).top(time_filter=TIME_FILTER ,limit=LIMIT)
    except Exception as e:
        print(f"Unable to retrieve posts. Error: {e}")
    return subreddit_posts

def posts_to_pandas(subreddit):
    #Extract each subreddit post and turn into Pandas Dataframe
    dict_posts = []
    try:
        for post in subreddit:
            extracted_date = pd.to_datetime(post.created_utc, unit='s') # Convert Unix timestamp to datetime
            posts = {
                "subreddit":post.subreddit.display_name,
                "id":post.id,
                "author":post.author,
                "author_flair_text":post.author_flair_text,
                "title":post.title,
                "num_comments":post.num_comments,
                "score":post.score,
                "selftext":post.selftext,
                "url":post.url,
                "created_utc":extracted_date
            }
            dict_posts.append(posts)
        extracted_post_df = pd.DataFrame(dict_posts)
    except Exception as e:
        print(f"Unable to extract posts. Error: {e}")

    return extracted_post_df

def convert_to_csv(data):
    pass

def main():
    reddit = reddit_api()
    subreddit= get_subreddit_posts(reddit)
    post_df = posts_to_pandas(subreddit)
    #Check rate limit
    print(reddit.auth.limits)
    print(post_df[['subreddit','title']])
    return post_df

if __name__ == "__main__":
    main()


