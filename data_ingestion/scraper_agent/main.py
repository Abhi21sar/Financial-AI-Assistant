from fastapi import FastAPI, Query
import requests
from bs4 import BeautifulSoup
import json

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Scraper Agent is running"}

@app.get("/earnings_news")
def get_yahoo_earnings_news(ticker: str = Query(...)):
    url = f"https://finance.yahoo.com/quote/{ticker}/analysis"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    # Extract earnings data (e.g., earnings surprise)
    tables = soup.find_all("table")
    earnings_data = []

    for table in tables:
        rows = table.find_all("tr")
        for row in rows:
            if "Earnings Surprise" in row.text:
                earnings_data.append(row.text.strip())

    return {"ticker": ticker, "earnings_surprise": earnings_data}


@app.get("/sec_filings")
def get_sec_filings(ticker: str = Query(...), form_type: str = "10-Q"):
    cik_lookup_url = f"https://www.sec.gov/files/company_tickers.json"
    cik_res = requests.get(cik_lookup_url)
    try:
        cik_data = cik_res.json()
    except Exception:
        return {"error": "Failed to parse SEC ticker lookup JSON"}


    # Find the CIK for the given ticker
    cik = None
    for entry in cik_data.values():
        if entry["ticker"].lower() == ticker.lower():
            cik = str(entry["cik_str"]).zfill(10)
            break

    if cik is None:
        return {"error": "CIK not found for ticker"}

    # Search EDGAR filings
    sec_url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    headers = {"User-Agent": "Multi-Agent Assistant/1.0"}
    res = requests.get(sec_url, headers=headers)

    if res.status_code != 200:
        return {"error": "Unable to retrieve filings"}

    data = res.json()
    matching_filings = [
        filing for filing in data.get("filings", {}).get("recent", {}).get("form", [])
        if filing == form_type
    ]

    return {
        "ticker": ticker,
        "form_type": form_type,
        "matches": matching_filings
    }