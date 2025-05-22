from src.utils.config import RedditConfig
import src.extract.extract_reddit as extract_reddit
import src.filter.discern_stocks as discern_stocks
import src.transform.sentiment_analysis as sentiment_analysis

def main():
    extracted_reddit_post = extract_reddit.extract_reddit(RedditConfig)

    filtered_reddit_post = discern_stocks.filter_reddit(extracted_reddit_post)

    analyzed_reddit_post = sentiment_analysis.sentiment_analyzed_post(filtered_reddit_post)

    return analyzed_reddit_post

if __name__ == "__main__":
    main()

    