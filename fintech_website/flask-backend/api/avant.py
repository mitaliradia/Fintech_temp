from dotenv import load_dotenv
import os

import requests

load_dotenv()

def get_latest_stock_price(symbol, api_key):
    base_url = "https://www.alphavantage.co/query"
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": api_key
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if "Global Quote" in data:
            latest_price = data["Global Quote"]["05. price"]
            return latest_price
        else:
            return None
    else:
        return None

# Example usage
api_key = os.getenv("API_KEY")
symbol = "AMZN"
print(api_key)
latest_price = get_latest_stock_price(symbol, api_key)
print(f"The latest price for {symbol} is: {latest_price}")
