import requests
from bs4 import BeautifulSoup

url_gainers = "https://finviz.com/screener.ashx?v=111&f=sh_price_o15,sh_relvol_o1&o=-change"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

def test():
    response = requests.get(url_gainers, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    tables = soup.find_all('table')
    print(f"Total tables: {len(tables)}")
    
    for t_idx, table in enumerate(tables):
        rows = table.find_all('tr')
        if not rows:
            continue
        
        # Check if this table has screener data rows
        # Tickers are in links, let's look for link class "tab-link"
        has_screener_rows = False
        screener_rows = []
        for r_idx, r in enumerate(rows):
            # Check if this row looks like a stock row. A stock row has td's, typically 11 columns, and the first column contains a number.
            tds = r.find_all('td')
            if len(tds) >= 10:
                td_texts = [td.get_text(strip=True) for td in tds]
                # Is first td a number (e.g. 1, 2, 3...)?
                first_val = td_texts[0]
                if first_val.isdigit():
                    has_screener_rows = True
                    screener_rows.append((r_idx, td_texts))
        
        if has_screener_rows:
            print(f"Table {t_idx} has screener rows! Total rows: {len(rows)}, Screener rows: {len(screener_rows)}")
            for idx, text in screener_rows[:5]:
                print(f"  Row {idx}: {text[:12]}")
                
            # Let's inspect the HTML of the first screener row to see the exact structure of links
            first_screener_row = rows[screener_rows[0][0]]
            print(f"  First row HTML snippet: {str(first_screener_row)[:500]}")
            break

test()
