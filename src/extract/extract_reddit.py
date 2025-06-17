from src.utils.config import RedditConfig
import praw
import pandas as pd

def reddit_api(config:RedditConfig) ->praw.Reddit:
    #Connect to Reddit's API through PRAW
    try:
        reddit = praw.Reddit(
            client_id=config.REDDIT_CLIENT_ID,
            client_secret=config.REDDIT_CLIENT_SECRET,
            user_agent=config.REDDIT_USER_AGENT,
            username=config.REDDIT_USERNAME,
        )
    except Exception as e:
        raise RuntimeError(f"Unable to connect to API. Error: {e}")
    return reddit

def get_subreddit_posts(reddit:praw.Reddit, SUBREDDIT_NAME, TIME_FILTER, LIMIT,) -> praw.models.ListingGenerator:
    #Get Subreddit Posts Object (PRAW Submission Class)
    try:
        subreddit_posts = reddit.subreddit(SUBREDDIT_NAME).top(time_filter=TIME_FILTER ,limit=LIMIT)
    except Exception as e:
        raise RuntimeError(f"Unable to retrieve posts. Error: {e}")
    return subreddit_posts

def posts_to_pandas(subreddit:praw.models.ListingGenerator) ->pd.DataFrame:
    dict_posts = []
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

    return extracted_post_df


def extract_reddit(config:RedditConfig) -> pd.DataFrame:
    reddit = reddit_api(config)
    subreddit= get_subreddit_posts(
        reddit = reddit,
        SUBREDDIT_NAME = config.SUBREDDIT,
        TIME_FILTER = config.TIME_FILTER,
        LIMIT = config.LIMIT  
        )
    post_df = posts_to_pandas(subreddit)

    #Check rate limit
    print(reddit.auth.limits)
    return post_df