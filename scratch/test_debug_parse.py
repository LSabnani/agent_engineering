import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

def parse_finviz_screener(url):
    response = requests.get(url, headers=headers, timeout=10)
    print(f"URL: {url}, Status: {response.status_code}")
    if response.status_code != 200:
        return []
        
    soup = BeautifulSoup(response.text, 'html.parser')
    tables = soup.find_all('table')
    print(f"Total tables found: {len(tables)}")
    
    data_table = None
    for t_idx, table in enumerate(tables):
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
            print(f"Table {t_idx} is a data table! Rows: {len(rows)}")
            data_table = table
            break
            
    if not data_table:
        print("No data table found")
        return []
        
    # Get the header row
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
        print("No header row found inside the table")
        # Try to find header in the table immediately preceding it
        # Let's inspect the headers from the table immediately preceding table t_idx
        return []
        
    headers_list = [td.get_text(strip=True) for td in header_row]
    header_indices = {name: idx for idx, name in enumerate(headers_list)}
    print(f"Headers found: {headers_list}")
    
    stocks = []
    for r_idx, r in enumerate(data_table.find_all('tr')):
        tds = r.find_all('td')
        if len(tds) < len(headers_list):
            continue
        first_val = tds[0].get_text(strip=True)
        if not first_val.isdigit():
            continue
            
        ticker_td = tds[header_indices['Ticker']]
        tab_link = ticker_td.find('a', class_='tab-link')
        ticker = tab_link.get_text(strip=True) if tab_link else ticker_td.get_text(strip=True)
        
        stock_data = {'ticker': ticker}
        for name, idx in header_indices.items():
            if name != 'Ticker' and name != 'No.':
                stock_data[name.lower()] = tds[idx].get_text(strip=True)
        stocks.append(stock_data)
        
    print(f"Successfully parsed {len(stocks)} stocks")
    return stocks

parse_finviz_screener("https://finviz.com/screener.ashx?v=111&f=sh_price_o15,sh_relvol_o1&o=-change")
