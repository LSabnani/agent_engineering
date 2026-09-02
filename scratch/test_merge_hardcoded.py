import requests
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

def parse_finviz_screener_hardcoded(url, view_type):
    # view_type is 'overview' or 'performance'
    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code != 200:
        print(f"Failed to fetch {url}, status code: {response.status_code}")
        return []
        
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the data table
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
        print(f"No data table found for {url}")
        return []
        
    stocks = []
    for r in data_table.find_all('tr'):
        tds = r.find_all('td')
        # Skip if not a data row
        if not tds:
            continue
        first_val = tds[0].get_text(strip=True)
        if not first_val.isdigit():
            continue
            
        td_texts = [td.get_text(strip=True) for td in tds]
        
        # Get ticker safely using class tab-link
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

def get_market_movers():
    # 1. Gainers
    print("Fetching Gainers Overview...")
    gainers_overview = parse_finviz_screener_hardcoded(
        "https://finviz.com/screener.ashx?v=111&f=sh_price_o15,sh_relvol_o1&o=-change", 'overview'
    )
    print("Fetching Gainers Performance...")
    gainers_perf = parse_finviz_screener_hardcoded(
        "https://finviz.com/screener.ashx?v=141&f=sh_price_o15,sh_relvol_o1&o=-change", 'performance'
    )
    
    # Merge Gainers
    gainers = []
    perf_dict = {s['ticker']: s for s in gainers_perf}
    for s in gainers_overview[:5]: # We only need top 5
        ticker = s['ticker']
        perf_data = perf_dict.get(ticker, {})
        merged = {
            'ticker': ticker,
            'company': s.get('company', ''),
            'price': s.get('price', ''),
            'change': s.get('change', ''),
            'volume': s.get('volume', ''),
            'rel_volume': perf_data.get('rel_volume', '1.0'),
            'avg_volume': perf_data.get('avg_volume', '')
        }
        gainers.append(merged)
        
    # 2. Losers
    print("Fetching Losers Overview...")
    losers_overview = parse_finviz_screener_hardcoded(
        "https://finviz.com/screener.ashx?v=111&f=sh_price_o15,sh_relvol_o1&o=change", 'overview'
    )
    print("Fetching Losers Performance...")
    losers_perf = parse_finviz_screener_hardcoded(
        "https://finviz.com/screener.ashx?v=141&f=sh_price_o15,sh_relvol_o1&o=change", 'performance'
    )
    
    # Merge Losers
    losers = []
    perf_dict_losers = {s['ticker']: s for s in losers_perf}
    for s in losers_overview[:5]: # We only need top 5
        ticker = s['ticker']
        perf_data = perf_dict_losers.get(ticker, {})
        merged = {
            'ticker': ticker,
            'company': s.get('company', ''),
            'price': s.get('price', ''),
            'change': s.get('change', ''),
            'volume': s.get('volume', ''),
            'rel_volume': perf_data.get('rel_volume', '1.0'),
            'avg_volume': perf_data.get('avg_volume', '')
        }
        losers.append(merged)
        
    return gainers, losers

gainers, losers = get_market_movers()
print("\n--- TOP GAINERS ---")
for idx, s in enumerate(gainers):
    print(f"{idx+1}. {s}")
print("\n--- TOP LOSERS ---")
for idx, s in enumerate(losers):
    print(f"{idx+1}. {s}")
