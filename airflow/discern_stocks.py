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
    stock_names.append(name)
    stock_tickers.append(tickers)

def does_post_contain_stocks(post):
    # Combine post title and text
    post_title_text = post.get('title') + '. ' + post.get('selftext')

    filtered_post = []

    # Using REGEX to find potential stock tickers
    ticker_pattern = r'\b[A-Z]{1,5}\b'
    potential_ticker_matches = set(re.findall(ticker_pattern, post_title_text))
    for potential_ticker in potential_ticker_matches:
        if potential_ticker in stock_tickers:
            print(f'Ticker match found: {potential_ticker}')
            filtered_post.append(post)
            
    # Using SpaCy & REGEX to find potential company names
    doc = nlp(post_title_text)
    for ent in doc.ents:
        if ent.label_ in ['ORG','GPE']:
            for stock_name in stock_names:
                regex_pattern = rf"\b{re.escape(ent.text)}\b"
                name_match = re.search(regex_pattern, stock_name, re.IGNORECASE)
                if name_match and len(name_match.group(0))> 3 and post not in filtered_post:
                    print(f'Name match found: {name_match}')
                    filtered_post.append(post)
                        
    if filtered_post:
        #print("Filtered post func:", filtered_post)
        return filtered_post 
    else:
        return None


df = extract_reddit.main()
filtered_posts = []

for index, row in df.iterrows():
    result = does_post_contain_stocks(row)
    if result:
        filtered_posts.extend(result)

filtered_df = pd.DataFrame(filtered_posts)
print('filtered_df :',filtered_df[['subreddit','title']])

