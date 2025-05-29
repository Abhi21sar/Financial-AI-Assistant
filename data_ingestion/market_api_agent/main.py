from fastapi import FastAPI, Query
import requests
import os

app = FastAPI()

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
BASE_URL = "https://www.alphavantage.co/query"

@app.get("/")
def read_root():
    return {"message": "Market API Agent is running"}

@app.get("/price")
def get_current_price(symbol: str = Query(..., description="Stock symbol (e.g. AAPL)")):
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": ALPHA_VANTAGE_API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    return response.json()

@app.get("/history")
def get_daily_history(symbol: str = Query(...), outputsize: str = "compact"):
    params = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": symbol,
        "outputsize": outputsize,
        "apikey": ALPHA_VANTAGE_API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    return response.json()