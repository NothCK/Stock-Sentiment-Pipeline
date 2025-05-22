import src.utils.stock_data as stock_data
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
import re, spacy
import pandas as pd

# Load spacy model
nlp = spacy.load('en_core_web_lg')

#Download sentence tokenizer data
nltk.download('punkt_tab')
from nltk.tokenize import sent_tokenize
analyzer = SentimentIntensityAnalyzer()

#Get dict, set of stock names and tickers
name_to_ticker, stock_names, stock_tickers = stock_data.load_stock_data()

#Constants to reduce false positives
ambiguous_tickers = stock_data.false_positive_tickers
ambiguous_stock_names = stock_data.false_positive_names

def stock_ticker_finder(sentence:str) -> str | None:
   #Using REGEX to find potential stock tickers
    ticker_pattern = r'\b[A-Z]{1,5}\b'
    potential_ticker_matches = set(re.findall(ticker_pattern, sentence))
    for ticker_match in potential_ticker_matches:
        if ticker_match in stock_tickers and ticker_match not in ambiguous_tickers:
            #print(f"Ticker match : {ticker_match}")
            return ticker_match
    #If no name check for company/stock name
    return stock_name_finder(sentence)

def stock_name_finder(sentence:str) -> str | None:
    spcy = nlp(sentence)
    for ent in spcy.ents:
        if ent.label_ in ['ORG']:
            ent_text = ent.text.lower()
            if ent_text in name_to_ticker:
                #print(f"Exact match: {ent_text}")
                return name_to_ticker[ent_text]
            #Substring match
            for stock_name in stock_names:
                if ent_text in stock_name and len(ent_text)> 3 and ent_text not in ambiguous_stock_names:
                    #print(f"Name match : {ent_text}")
                    return name_to_ticker.get(stock_name)
    #If no match returns None
    return None

def analyze_sentiment(post:pd.Series) -> tuple[dict,pd.Series]:
    post_text = post.get('title') + '. ' + post.get('selftext')
    sentences = sent_tokenize(post_text)
    current_stock = None
    stock_and_sentiment= {}

    for sentence in sentences:
        stock_match = stock_ticker_finder(sentence)
        sentiment = analyzer.polarity_scores(sentence)
        if stock_match:
            current_stock = stock_match
            if current_stock in stock_and_sentiment:
                stock_and_sentiment[current_stock].append(sentiment)
            else:
                stock_and_sentiment[current_stock] = [sentiment]
        #If stock_match returns None, use the last current stock mentioned
        elif current_stock:
            stock_and_sentiment[current_stock].append(sentiment)


    for stock,sentiments in stock_and_sentiment.items():
        compound_scores = [sentiment['compound'] for sentiment in sentiments]
        avg_sentiment = sum(compound_scores) / len(compound_scores)
        stock_and_sentiment[stock] = round(avg_sentiment,3)
        #This is due to sentiment from VADER is not a direct value
    
    return stock_and_sentiment, post

def restructure_data(sentiment:dict, original_post:pd.Series) -> list[pd.Series]:
    structured_posts = []
    for stock,score in sentiment.items():
        post = {
            "subreddit": original_post.get("subreddit")
            , "id": original_post.get("id")
            , "author": original_post.get("author")
            , "author_flair_text": original_post.get("author_flair_text")
            , "title": original_post.get("title")
            , "num_comments": original_post.get("num_comments")
            , "score": original_post.get("score")
            , "selftext": original_post.get("selftext")
            , "url": original_post.get("url")
            , "created_utc": original_post.get("created_utc")
            , "stock": stock
            , "sentiment": score
            , "num_stocks_mentioned": len(sentiment)
            , "overall_post_sentiment": round(sum(sentiment.values()) / len(sentiment), 3)
        }
        structured_posts.append(pd.Series(post))
    return structured_posts

def sentiment_analyzed_post(df:pd.DataFrame) -> pd.DataFrame:
    series_of_posts = []
    for index,series in df.iterrows():
        sentiment, post = analyze_sentiment(series)
        if sentiment:
            structured_series_list = restructure_data(sentiment,post)
            series_of_posts.extend(structured_series_list)
    
    structured_df = pd.DataFrame(series_of_posts)
    structured_df = structured_df.where(pd.notnull(structured_df), None)
    print(structured_df[['subreddit','title','stock','sentiment']])
    return structured_df
