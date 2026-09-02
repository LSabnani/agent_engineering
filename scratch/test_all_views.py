import sys
import requests
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

views = ["111", "121", "131", "141", "151", "161", "171", "181"]

for v in views:
    url = f"https://finviz.com/screener.ashx?v={v}&f=sh_price_o15,sh_relvol_o1"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the table containing data rows
        for t_idx, table in enumerate(soup.find_all('table')):
            rows = table.find_all('tr')
            if not rows:
                continue
            
            is_data_table = False
            for r in rows:
                tds = r.find_all('td')
                if len(tds) >= 10:
                    first_val = tds[0].get_text(strip=True)
                    if first_val.isdigit():
                        is_data_table = True
                        break
            
            if is_data_table:
                # Find the header row
                header_row = None
                for r in rows:
                    tds = r.find_all(['td', 'th'])
                    if len(tds) >= 10:
                        first_val = tds[0].get_text(strip=True)
                        td_texts = [td.get_text(strip=True) for td in tds]
                        if not first_val.isdigit() and 'Ticker' in td_texts:
                            header_row = tds
                            break
                if header_row:
                    header_texts = [td.get_text(strip=True) for td in header_row]
                    print(f"View v={v} headers: {header_texts}")
                else:
                    # Let's print the first data row cells to see if we can guess the columns
                    for r in rows:
                        tds = r.find_all('td')
                        if len(tds) >= 10:
                            first_val = tds[0].get_text(strip=True)
                            if first_val.isdigit():
                                print(f"View v={v} (no header row found) first row length: {len(tds)}, values: {[td.get_text(strip=True) for td in tds]}")
                                break
                break
    except Exception as e:
        print(f"Error on view {v}: {e}")
