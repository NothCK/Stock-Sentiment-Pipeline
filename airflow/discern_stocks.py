import extract_reddit
import spacy
from rapidfuzz import fuzz
# Load spacy model
nlp = spacy.load('en_core_web_lg')

# Load ticker and company name
pd = extract_reddit.pd
df = pd.read_csv('sp500_companies.csv')
tickers_csv = pd.Series(df['Symbol'].values, index=df['Longname']).to_dict()
print(list(tickers_csv.items())[:5])

def does_post_contain_stocks(posts):
    filtered_post = []
    for post in posts:
        doc = nlp(posts)

        for ent in doc.ents:
            if ent.label == 'ORG':
                for name, ticker in tickers_csv.items():
                    if fuzz.ratio(ent.text, name) > 80 or fuzz.ratio(ent.text, ticker) > 90:
                        filtered_post.append(post)
    
    stock_posts = pd.DataFrame(filtered_post)
    return stock_posts


            


