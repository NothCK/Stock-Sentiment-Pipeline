import src.utils.stock_data as stock_data
import spacy
import re
import pandas as pd

# Load spacy model
nlp = spacy.load('en_core_web_lg')

#Constants to reduce false positives
ambiguous_tickers = stock_data.false_positive_tickers
ambiguous_stock_names = stock_data.false_positive_names

def does_post_contain_stocktickers(post:pd.Series, stock_names:set, stock_tickers:set) -> bool:
    title = post.get('title') or ''
    selftext = post.get('selftext') or ''
    post_title_text = title + '. ' + selftext
    
    #Using REGEX to find potential stock tickers
    ticker_pattern = r'\b[A-Z]{1,5}\b'
    potential_ticker_matches = set(re.findall(ticker_pattern, post_title_text))
    for potential_ticker in potential_ticker_matches:
        if potential_ticker in stock_tickers and potential_ticker not in ambiguous_tickers: 
            return True

    #If no match, check for company names
    return does_post_contain_stocknames(post_title_text, stock_names)
        

def does_post_contain_stocknames(post_title_text, stock_names) -> bool:
    #Using SpaCy to find potential company names
    doc = nlp(post_title_text)
    for ent in doc.ents:
        if ent.label_ in ['ORG']:
            ent_text = ent.text.lower()
            for stock_name in stock_names:
                if ent_text in stock_name and len(ent_text)> 3 and ent_text not in ambiguous_stock_names:
                    return True     
    return False 

def filter_reddit(df:pd.DataFrame) -> pd.DataFrame:
    name_to_ticker, stock_names, stock_tickers = stock_data.load_stock_data()

    boolean_post_contain_stock = df.apply(
        lambda row:
        does_post_contain_stocktickers(row, stock_names, stock_tickers ), axis=1 #axis 1 is for rows
    )

    filtered_df = df[boolean_post_contain_stock].copy()
    print('filtered_df :',filtered_df[['subreddit','title']])
    return filtered_df
    
    """
    filtered_posts = []

    for index, row in df.iterrows():
        result = does_post_contain_stocktickers(row, stock_names, stock_tickers ) # row is panda series
        if result:      #if True add row/Series/post
            filtered_posts.append(row)

    filtered_df = pd.DataFrame(filtered_posts)
    print('filtered_df :',filtered_df[['subreddit','title']])
    return filtered_df
    """

