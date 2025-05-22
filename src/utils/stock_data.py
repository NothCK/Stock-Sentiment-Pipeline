import pandas as pd
import os

#Constants to reduce false positives
false_positive_tickers = {'V', 'T', 'C', 'O', 'D', 'F', 'A', 'K', 'L', 'J','IT','DD','PEG'}  
false_positive_names = {'house'}

#Add aliases for popular or alternative names
manual_aliases = {
    'google': 'GOOGL',       
    'facebook': 'META',
    'waymo': 'GOOGL',
    'youtube': 'GOOGL'       
}

def load_stock_data(extra_aliases:dict = None) -> tuple[dict,set,set]:
    #Get the absolute path to this script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, '..', '..', 'sp500_companies.csv')

    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV path not found: {csv_path}")

    # Load ticker and company name
    df = pd.read_csv(csv_path)
    tickers_csv = pd.Series(df['Symbol'].values, index=df['Longname']).to_dict()
    
    #Ensure lowercase name and upper ticker
    name_to_ticker = {
        name.lower() : ticker.upper()
        for name,ticker in tickers_csv.items()
    }

    if extra_aliases is None:
        extra_aliases = manual_aliases
    name_to_ticker.update(extra_aliases)
    
    # Save stock tickers and company name
    stock_names = set(name_to_ticker.keys())
    stock_tickers = set(name_to_ticker.values())
    
    return name_to_ticker, stock_names, stock_tickers

