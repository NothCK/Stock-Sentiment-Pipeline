import discern_stocks
import os, re, ast
import pandas as pd
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from llama_index.core.node_parser import SentenceSplitter

#Load environment variable from .env
dotenv_path = os.path.join(os.path.dirname(__file__),"..",".env")
load_dotenv(dotenv_path)

client = InferenceClient(
    provider= "hf-inference",
    api_key= os.getenv("HF_TOKEN")
)

def analyze_sentiment(post):
    post_text = post.get('title') + '. ' + post.get('selftext')
    text_splitter = SentenceSplitter(chunk_size=500, chunk_overlap=100)
    chunks = text_splitter.split_text(post_text)

    results = {}
    for chunk in chunks:
        prompt_message = [
            {"role": "system", "content": "You are a financial NLP assistant that extracts stock sentiment."}
            ,{"role": "user", "content": 
            f"""Give me the stock ticker and sentiment of every US stock in the text below (-1 to 1).
            Return a dictionary format like this: {{'Stock ticker': sentiment}}. REMEMBER ONLY STOCK TICKER (NO stock/company name) AND THE SENTIMENT
            Don't explain anything. Just return the dictionary.\n\nText: {chunk}"""}
            ]

        completion = client.chat.completions.create(
            model="mistralai/Mistral-7B-Instruct-v0.3",
            messages= prompt_message,
            max_tokens= 256
        )

        print(completion.choices[0].message.content)
        response_text = completion.choices[0].message.content

        match = re.search(r"\{.*?\}", response_text, re.DOTALL)
        if match:
            try:
                chunk_result = ast.literal_eval(match.group(0))
                for ticker, score in chunk_result.items():
                    if ticker in results:
                        results[ticker].append(score)   #append score as a list {ticker:[score1,score2..]}
                    else:
                        results[ticker] = [score]       #add new ticker and score
            except (SyntaxError, ValueError) as e:
                print(f"Parsing failed: {e}")
        else:
            print("No dictionary found in response.")

    final_result = {ticker: sum(scores)/len(scores) for ticker, scores in results.items()}
    print('Final Result:',final_result)
    return final_result, post

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

if __name__ == "__main__":
    main()
        
    


