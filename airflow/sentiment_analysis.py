import discern_stocks
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

# Load ticker and company name
df = pd.read_csv('sp500_companies.csv')
tickers_csv = pd.Series(df['Symbol'].values, index=df['Longname']).to_dict()
name_to_ticker = {
    name.lower() : ticker
    for name,ticker in tickers_csv.items()
    }
#Add aliases for popular or alternative names
manual_aliases = {
    'google': 'GOOGL',       
    'facebook': 'META',
    'waymo': 'GOOGL'       
}
name_to_ticker.update(manual_aliases)

# Save stock tickers and company name
stock_names = []
stock_tickers = []
for name, tickers in name_to_ticker.items():
    stock_names.append(name)
    stock_tickers.append(tickers.upper())

def analyze_sentiment(post_text):
    #post_text = post.get('title') + '. ' + post.get('selftext')
    sentences = sent_tokenize(post_text)

    current_stock = None
    stock_and_sentiment= {}
    for sentence in sentences:
        stock_match = stock_ticker_finder(sentence)
        if stock_match:
            if current_stock is None:
                current_stock = stock_match
                sentiment = analyzer.polarity_scores(sentence)
                stock_and_sentiment[current_stock] = [sentiment]
            else:
                current_stock = stock_match
                sentiment = analyzer.polarity_scores(sentence)
                if current_stock in stock_and_sentiment:
                    stock_and_sentiment[current_stock].append(sentiment)
                else:
                    stock_and_sentiment[current_stock] = [sentiment]
        #If stock_match returns None, continue to the next sentence
        else:
            continue

    for stock,sentiments in stock_and_sentiment.items():
        compound_scores = [sentiment['compound'] for sentiment in sentiments]
        avg_sentiment = sum(compound_scores) / len(compound_scores)
        stock_and_sentiment[stock] = avg_sentiment
        #This is due to sentiment from VADER is not a direct value
    
    return stock_and_sentiment

def stock_ticker_finder(sentence):
    ambiguous_tickers = ['V', 'T', 'C', 'O', 'D', 'F', 'A', 'K', 'L', 'J']  #Reduce false positives
    #Using REGEX to find potential stock tickers
    ticker_pattern = r'\b[A-Z]{1,5}\b'
    potential_ticker_matches = set(re.findall(ticker_pattern, sentence))
    for ticker_match in potential_ticker_matches:
        if ticker_match in stock_tickers and ticker_match not in ambiguous_tickers:
            print(f"Ticker match : {ticker_match}")
            return ticker_match
    #If no name check for company/stock name
    return stock_name_finder(sentence)

def stock_name_finder(sentence):
    spcy = nlp(sentence)
    print("Entities detected:", [(ent.text, ent.label_) for ent in spcy.ents]) 
    for ent in spcy.ents:
        if ent.label_ in ['ORG']:
            ent_text = ent.text.lower()
            for stock_name in stock_names:
                if ent_text in stock_name and len(ent_text)> 3:
                    print(f"Name match : {ent_text}")
                    return name_to_ticker.get(stock_name)
    #If no match returns None
    return None


def restructure_data(sentiment, original_post):
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
        }
        structured_post = pd.Series(post)
        return structured_post

def main():
    df = discern_stocks.main()
    series_of_posts = []
    for index,series in df.iterrows():
        sentiment, post = analyze_sentiment(series)
        try:
            structured_series = restructure_data(sentiment,post)
            series_of_posts.append(structured_series)
        except Exception as e:
            print(f"Houston we got a problem: {e}")
    
    structured_df = pd.DataFrame(series_of_posts)
    print(structured_df[['title','stock','sentiment']])


post_text = "Google valuation attempt with Waymo’s hidden value inside of GOOGLE  Stock Analysis I love Google as the number one company on earth that I wouldn’t want to do without(at least before my brother started giving me hand me down iPhones). We effectively have a duopoly for humans most loved electronic, the phone. Microsoft and Amazon and Facebook gave up on having phones with the own competitor to IOS and Android.  Below I will try to value Google without looking at hard numbers as I have AI models and dcf models and people with accounting or other business PHDs on YouTube (a Google company) to model Google’s valuation.  YouTube The number one streaming app platform in the world by usage even though Netflix wins in revenue. Netflix is currently at 487 billion. A 300- 400 billion dollar market cap might be reasonable. 2 Android a member of the duopoly for humans favorite electronic that I don’t see being displace for decades meta dreams of displacing the phone because they were beat soundly. I remember Bill gates saying losing out on the mobile phone market was a 500 billion dollar miss. And this was pre COVID inflation estimate. So a 500 billion dollar plus market value I will consider the floor for Android.  3. Google cloud: sorry as I need help with valuation even though they appear to be in a triopoly(oligopoly) with Microsoft and Amazon I will need perplexity’s help…. lower margins and a good growth growth rate has an estimate around 490 billion even though they are clearly in 3rd place.  4: Google’s search add revenue which I will need some tour of help with from perplexity…. I asked for a heavy discount and to exclude YouTube and Android add revenue and they still came up with a valuation of 1 trillion for just the ads.  So we are at 2.29 trillion before Google’s cash on hand which is 95 billion. So we are at 2.385 trillion without valuing any other bets or waymo. Let’s make an attempt at waymo.  5. Waymo: ChatGPT game me values of 50 billion all the way up to 835 billion. So I have to use my peanut brain to try to value Waymo. Waymo has been giving self driving rides since October 2020. That is a 5 year lead since Cruise was dismantled. And the reason they aren’t profitable now is because each vehicle cost 250-300k due to the cost of lidar and the lack of scale in building these off the assembly line but that is changing. Those of us old enough to remember 42 inch plasma tvs costing 20,000 around year 2000 know that the cost of self driving stack is going to drop like a rock. I’ve seen estimates of 50,000 to 60,000 a vehicle for the next gen coming out next year and then the 3rd gen in 2030 as low as 3,000$ more per vehicle. Leading waymo having a valuation nearer the upper limit. 500 billion plus maybe 800 billion and that might be too low. From my simpleton reasoning. I mean Netflix is Netflix because of their leadership in streaming and I expect Waymo to perform similarly as well with fantastic margins on a very low cost stack that will be willing to deal with every single automobile producer, into a multi trillion dollar a year market as the leader with a massive head-start.  That gives us a valuation of 2.885 trillion without a margin of safety.  219.39 a share so today price in google would be a 35% percent margin of safety."
print(analyze_sentiment(post_text))


