import sys
import requests
from bs4 import BeautifulSoup

# Ensure stdout handles UTF-8
sys.stdout.reconfigure(encoding='utf-8')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

def check_view(v_param):
    url = f"https://finviz.com/screener.ashx?v={v_param}&f=sh_price_o15,sh_relvol_o1"
    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the table containing data rows
    for t_idx, table in enumerate(soup.find_all('table')):
        rows = table.find_all('tr')
        if not rows:
            continue
        
        # Check if it has data rows
        is_data_table = False
        data_rows = []
        for r_idx, r in enumerate(rows):
            tds = r.find_all('td')
            if len(tds) >= 10:
                first_val = tds[0].get_text(strip=True)
                if first_val.isdigit():
                    is_data_table = True
                    data_rows.append(tds)
                    
        if is_data_table:
            print(f"\n--- Found Data Table in View v={v_param} (Table {t_idx}) ---")
            
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
                print(f"Header Row: {header_texts}")
            else:
                print("No header row found inside the table containing data.")
            
            # Print columns of the first data row
            if data_rows:
                first_row_tds = data_rows[0]
                td_texts = [td.get_text(strip=True) for td in first_row_tds]
                print(f"First Data Row: {td_texts}")
            break

check_view("111")
check_view("171")
