import os
from dotenv import load_dotenv

#Load environment variable from .env
dotenv_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
load_dotenv(dotenv_path)


class RedditConfig:
    REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
    REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
    REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")
    REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")

    #Options for extracting data from PRAW
    SUBREDDIT = "valueinvesting+stocks"
    LIMIT = 45
    TIME_FILTER = "day"
