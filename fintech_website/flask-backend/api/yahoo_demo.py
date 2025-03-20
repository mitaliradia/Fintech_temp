import yahoo_fin.stock_info as si
from yahoo_fin import options as ops
from yahoo_fin.stock_info import get_data

import requests

import requests_html

import time
import datetime
import pytz

# amazon_data = get_data("amzn")
# print(amazon_data.head())

# apple_data = get_data("aapl")
# print(apple_data.head())

def get_stock_data_custom(ticker):
    try:
        data = get_data(ticker)
        return data
    except Exception as e:
        print(f"An error occured {e}")

        end = datetime.datetime.now(pytz.timezone("US/Eastern"))
        start = end - datetime.timedelta(days=7)

        # url = f"https://query1.finance.yahoo.com/v7/finance/download/{ticker}"
        url = f"https://query2.finance.yahoo.com/v7/finance/download/{ticker}"
        params ={
            "period1": int(start.timestamp()),  
            "period2": int(end.timestamp()),
            "interval": "1d",
            "events": "history",
            "includeAdjustedClose": "true"
        }

        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            print("Response is OK")
            # You can try to parse the response content here
            print(response.text)
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")


amazon_data = get_stock_data_custom("amzn")