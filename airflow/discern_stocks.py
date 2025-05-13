import extract_reddit
import spacy
import re

# Load spacy model
nlp = spacy.load('en_core_web_lg')

# Load ticker and company name
pd = extract_reddit.pd
df = pd.read_csv('sp500_companies.csv')
tickers_csv = pd.Series(df['Symbol'].values, index=df['Longname']).to_dict()

# Save stock tickers and company name
stock_names = []
stock_tickers = []
for name, tickers in tickers_csv.items():
    stock_names.append(name.lower())
    stock_tickers.append(tickers.upper())

def does_post_contain_stocktickers(post):
    post_title_text = post.get('title') + '. ' + post.get('selftext')

    ambiguous_tickers = ['V', 'T', 'C', 'O', 'D', 'F', 'A', 'K', 'L', 'J']
    #Using REGEX to find potential stock tickers
    ticker_pattern = r'\b[A-Z]{1,5}\b'
    potential_ticker_matches = set(re.findall(ticker_pattern, post_title_text))
    for potential_ticker in potential_ticker_matches:
        if potential_ticker in stock_tickers and potential_ticker not in ambiguous_tickers: #To reduce false positives
            print(f'Ticker match found: {potential_ticker}')
            return post
    #If no match, check for company names
    return does_post_contain_stocknames(post)
        

def does_post_contain_stocknames(post):
    #Using SpaCy to find potential company names
    post_full_text = post.get('title') + '. ' + post.get('selftext')
    doc = nlp(post_full_text)
    for ent in doc.ents:
        if ent.label_ in ['ORG']:
            ent_text = ent.text.lower()
            for stock_name in stock_names:
                if ent_text in stock_name and len(ent_text)> 3:
                    print(f'Name match found: {ent_text}')
                    return post
    return None #if there is no match

def main():
    df = extract_reddit.main()
    filtered_posts = []
    for index, row in df.iterrows():
        result = does_post_contain_stocktickers(row) # row is panda series
        if result is not None:      #using this syntax due to it being a Series
            filtered_posts.append(result)

    filtered_df = pd.DataFrame(filtered_posts)
    print('filtered_df :',filtered_df[['subreddit','title']])
    return filtered_df

if __name__ == "__main__":
    main()
