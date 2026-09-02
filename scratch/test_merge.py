import requests
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

def parse_finviz_screener(url):
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
        
    # Get the header row to map columns dynamically
    header_row = None
    for r in data_table.find_all('tr'):
        tds = r.find_all(['td', 'th'])
        if len(tds) >= 10:
            first_val = tds[0].get_text(strip=True)
            td_texts = [td.get_text(strip=True) for td in tds]
            if not first_val.isdigit() and 'Ticker' in td_texts:
                header_row = tds
                break
                
    if not header_row:
        print(f"No header row found for {url}")
        return []
        
    headers_list = [td.get_text(strip=True) for td in header_row]
    header_indices = {name: idx for idx, name in enumerate(headers_list)}
    
    stocks = []
    for r in data_table.find_all('tr'):
        tds = r.find_all('td')
        if len(tds) < len(headers_list):
            continue
        first_val = tds[0].get_text(strip=True)
        if not first_val.isdigit():
            continue
            
        stock_data = {}
        # Parse Ticker safely using tab-link class to avoid logo spans
        ticker_td = tds[header_indices['Ticker']]
        tab_link = ticker_td.find('a', class_='tab-link')
        ticker = tab_link.get_text(strip=True) if tab_link else ticker_td.get_text(strip=True)
        
        stock_data['ticker'] = ticker
        
        for name, idx in header_indices.items():
            if name != 'Ticker' and name != 'No.':
                stock_data[name.lower()] = tds[idx].get_text(strip=True)
                
        stocks.append(stock_data)
        
    return stocks

def get_market_movers():
    # 1. Gainers
    print("Fetching Gainers Overview...")
    gainers_overview = parse_finviz_screener("https://finviz.com/screener.ashx?v=111&f=sh_price_o15,sh_relvol_o1&o=-change")
    print("Fetching Gainers Performance...")
    gainers_perf = parse_finviz_screener("https://finviz.com/screener.ashx?v=141&f=sh_price_o15,sh_relvol_o1&o=-change")
    
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
            'change': s.get('change %', ''),
            'volume': s.get('volume', ''),
            'rel_volume': perf_data.get('rel volume', ''),
            'avg_volume': perf_data.get('avg volume', '')
        }
        gainers.append(merged)
        
    # 2. Losers
    print("Fetching Losers Overview...")
    losers_overview = parse_finviz_screener("https://finviz.com/screener.ashx?v=111&f=sh_price_o15,sh_relvol_o1&o=change")
    print("Fetching Losers Performance...")
    losers_perf = parse_finviz_screener("https://finviz.com/screener.ashx?v=141&f=sh_price_o15,sh_relvol_o1&o=change")
    
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
            'change': s.get('change %', ''),
            'volume': s.get('volume', ''),
            'rel_volume': perf_data.get('rel volume', ''),
            'avg_volume': perf_data.get('avg volume', '')
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
