import os
import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__, template_folder='.', static_folder='.')
CORS(app)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

def parse_finviz_screener_hardcoded(url, view_type):
    """
    Scrapes Finviz screener page and extracts stock metrics using fixed column indexing.
    view_type can be 'overview' or 'performance'.
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            return []
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the correct stock data table (typically containing data rows with digital row numbers)
        data_table = None
        for table in soup.find_all('table'):
            rows = table.find_all('tr')
            if not rows:
                continue
            is_data = False
            for r in rows:
                tds = r.find_all('td')
                if len(tds) >= 10:
                    first_val = tds[0].get_text(strip=True)
                    if first_val.isdigit():
                        is_data = True
                        break
            if is_data:
                data_table = table
                break
                
        if not data_table:
            return []
            
        stocks = []
        for r in data_table.find_all('tr'):
            tds = r.find_all('td')
            if not tds:
                continue
            first_val = tds[0].get_text(strip=True)
            if not first_val.isdigit():
                continue
                
            td_texts = [td.get_text(strip=True) for td in tds]
            
            # Extract clean ticker using tab-link class to avoid overlapping logo spans
            ticker_td = tds[1]
            tab_link = ticker_td.find('a', class_='tab-link')
            ticker = tab_link.get_text(strip=True) if tab_link else td_texts[1]
            
            stock_data = {'ticker': ticker}
            
            if view_type == 'overview':
                # 1: Ticker, 2: Company, 8: Price, 9: Change %, 10: Volume
                if len(td_texts) >= 11:
                    stock_data['company'] = td_texts[2]
                    stock_data['price'] = td_texts[8]
                    stock_data['change'] = td_texts[9]
                    stock_data['volume'] = td_texts[10]
            elif view_type == 'performance':
                # 1: Ticker, 13: Avg Volume, 14: Rel Volume, 15: Price, 16: Change %, 17: Volume
                if len(td_texts) >= 18:
                    stock_data['avg_volume'] = td_texts[13]
                    stock_data['rel_volume'] = td_texts[14]
                    stock_data['price'] = td_texts[15]
                    stock_data['change'] = td_texts[16]
                    stock_data['volume'] = td_texts[17]
                    
            stocks.append(stock_data)
            
        return stocks
    except Exception as e:
        app.logger.error(f"Error parsing finviz screener: {e}")
        return []

def get_market_movers():
    """
    Fetches, parses, and merges overview and performance screener views for gainers and losers.
    """
    # 1. Fetch Gainers
    gainers_overview = parse_finviz_screener_hardcoded(
        "https://finviz.com/screener.ashx?v=111&f=sh_price_o15,sh_relvol_o1&o=-change", 'overview'
    )
    gainers_perf = parse_finviz_screener_hardcoded(
        "https://finviz.com/screener.ashx?v=141&f=sh_price_o15,sh_relvol_o1&o=-change", 'performance'
    )
    
    gainers = []
    perf_dict_gainers = {s['ticker']: s for s in gainers_perf}
    for s in gainers_overview[:5]:
        ticker = s['ticker']
        perf_data = perf_dict_gainers.get(ticker, {})
        gainers.append({
            'ticker': ticker,
            'company': s.get('company', ''),
            'price': s.get('price', ''),
            'change': s.get('change', ''),
            'volume': s.get('volume', ''),
            'rel_volume': perf_data.get('rel_volume', '1.0'),
            'avg_volume': perf_data.get('avg_volume', '')
        })
        
    # 2. Fetch Losers
    losers_overview = parse_finviz_screener_hardcoded(
        "https://finviz.com/screener.ashx?v=111&f=sh_price_o15,sh_relvol_o1&o=change", 'overview'
    )
    losers_perf = parse_finviz_screener_hardcoded(
        "https://finviz.com/screener.ashx?v=141&f=sh_price_o15,sh_relvol_o1&o=change", 'performance'
    )
    
    losers = []
    perf_dict_losers = {s['ticker']: s for s in losers_perf}
    for s in losers_overview[:5]:
        ticker = s['ticker']
        perf_data = perf_dict_losers.get(ticker, {})
        losers.append({
            'ticker': ticker,
            'company': s.get('company', ''),
            'price': s.get('price', ''),
            'change': s.get('change', ''),
            'volume': s.get('volume', ''),
            'rel_volume': perf_data.get('rel_volume', '1.0'),
            'avg_volume': perf_data.get('avg_volume', '')
        })
        
    return gainers, losers

def get_mag7_data():
    """
    Scrapes Finviz performance view (v=141) for Mag7 tickers and returns their performance statistics.
    """
    url = "https://finviz.com/screener.ashx?v=141&t=NVDA,MSFT,AAPL,GOOGL,AMZN,META,TSLA"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            return []
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        data_table = None
        for table in soup.find_all('table'):
            rows = table.find_all('tr')
            if not rows:
                continue
            is_data = False
            for r in rows:
                tds = r.find_all('td')
                if len(tds) >= 10:
                    first_val = tds[0].get_text(strip=True)
                    if first_val.isdigit():
                        is_data = True
                        break
            if is_data:
                data_table = table
                break
                
        if not data_table:
            return []
            
        stocks = {}
        for r in data_table.find_all('tr'):
            tds = r.find_all('td')
            if len(tds) < 18:
                continue
            first_val = tds[0].get_text(strip=True)
            if not first_val.isdigit():
                continue
                
            td_texts = [td.get_text(strip=True) for td in tds]
            
            ticker_td = tds[1]
            tab_link = ticker_td.find('a', class_='tab-link')
            ticker = tab_link.get_text(strip=True) if tab_link else td_texts[1]
            
            stocks[ticker] = {
                'price': td_texts[15],
                'day': td_texts[16],
                'week': td_texts[2],
                'month': td_texts[3],
                'qtr': td_texts[4],
                'year': td_texts[7]
            }
            
        # Return Mag7 stocks in specific logical order matching frontend index
        ordered_tickers = ['NVDA', 'MSFT', 'AAPL', 'GOOGL', 'AMZN', 'META', 'TSLA']
        result = []
        for ticker in ordered_tickers:
            if ticker in stocks:
                result.append({
                    'ticker': ticker,
                    **stocks[ticker]
                })
        return result
    except Exception as e:
        app.logger.error(f"Error parsing mag7 data: {e}")
        return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index.html')
def index_html():
    return render_template('index.html')

@app.route('/stocks.html')
def stocks():
    return render_template('stocks.html')

@app.route('/mag7.html')
def mag7():
    return render_template('mag7.html')

@app.route('/api/stocks', methods=['GET'])
def api_stocks():
    gainers, losers = get_market_movers()
    if not gainers and not losers:
        return jsonify({
            "status": "error",
            "message": "Failed to retrieve stock data from Finviz."
        }), 500
        
    return jsonify({
        "status": "success",
        "gainers": gainers,
        "losers": losers
    })

@app.route('/api/mag7', methods=['GET'])
def api_mag7():
    data = get_mag7_data()
    if not data:
        return jsonify({
            "status": "error",
            "message": "Failed to retrieve Magnificent 7 data from Finviz."
        }), 500
        
    return jsonify({
        "status": "success",
        "stocks": data
    })

if __name__ == '__main__':
    # Running on local port 5000
    app.run(host='127.0.0.1', port=5000, debug=True)
