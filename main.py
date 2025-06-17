from src.utils.config import GCPConfig, RedditConfig
import src.extract.extract_reddit as extract_reddit
import src.filter.discern_stocks as discern_stocks
import src.transform.sentiment_analysis as sentiment_analysis
import src.load.load_to_bigquery as load_to_bigquery

def run_pipeline():
    extracted_reddit_post = extract_reddit.extract_reddit(RedditConfig)
    print(f"Extracted df: \n{extracted_reddit_post[['subreddit','title']]}")

    filtered_reddit_post = discern_stocks.filter_reddit(extracted_reddit_post)
    print(f'Filtered df : \n{filtered_reddit_post[['subreddit','title']]}')

    analyzed_reddit_post = sentiment_analysis.sentiment_analyzed_post(filtered_reddit_post)
    print(analyzed_reddit_post[['subreddit','title','stock','sentiment']])

    load_to_bigquery.upload_dataframe_to_gcs(analyzed_reddit_post,GCPConfig)
    loaded_rows = load_to_bigquery.load_csv_to_bigquery(GCPConfig)
    print(f"Loaded {loaded_rows} rows to BigQuery")
    

if __name__ == "__main__":
    run_pipeline()

    