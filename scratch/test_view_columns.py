import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

def check_view(v_param):
    url = f"https://finviz.com/screener.ashx?v={v_param}&f=sh_price_o15,sh_relvol_o1"
    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    for table in soup.find_all('table'):
        first_row = table.find('tr')
        if first_row:
            headers_list = [td.get_text(strip=True) for td in first_row.find_all('td')]
            if 'Ticker' in headers_list:
                print(f"View v={v_param} Headers: {headers_list}")
                # Print first row data
                rows = table.find_all('tr')
                for r in rows:
                    tds = r.find_all('td')
                    if len(tds) >= len(headers_list):
                        td_texts = [td.get_text(strip=True) for td in tds]
                        if td_texts[0].isdigit():
                            print(f"  First Data Row: {td_texts}")
                            break
                break

check_view("111")
check_view("171")
