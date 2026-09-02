import requests
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

def test_mag7():
    url = "https://finviz.com/screener.ashx?v=141&t=NVDA,MSFT,AAPL,GOOGL,AMZN,META,TSLA"
    response = requests.get(url, headers=headers, timeout=10)
    print(f"Status: {response.status_code}")
    if response.status_code != 200:
        return
        
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find data table
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
        print("No data table found")
        return
        
    rows = data_table.find_all('tr')
    for r in rows:
        tds = r.find_all('td')
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
        
        # In performance view v=141:
        # Index 1: Ticker
        # Index 2: Perf Week (e.g. '4.44%')
        # Index 3: Perf Month (e.g. '2.08%')
        # Index 4: Perf Quart (e.g. '-27.54%')
        # Index 5: Perf Half
        # Index 6: Perf YTD
        # Index 7: Perf Year (e.g. '56.29%')
        # Index 15: Price
        # Index 16: Change % (day change)
        # Index 17: Volume
        if len(td_texts) >= 18:
            print(f"Ticker: {ticker}")
            print(f"  Price: {td_texts[15]}")
            print(f"  Day: {td_texts[16]}")
            print(f"  Week: {td_texts[2]}")
            print(f"  Month: {td_texts[3]}")
            print(f"  Qtr: {td_texts[4]}")
            print(f"  Year: {td_texts[7]}")

test_mag7()
