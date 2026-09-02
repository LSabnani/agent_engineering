import requests
from bs4 import BeautifulSoup

url_gainers = "https://finviz.com/screener.ashx?v=111&f=sh_price_o15,sh_relvol_o1&o=-change"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

def test():
    response = requests.get(url_gainers, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    for table in soup.find_all('table'):
        rows = table.find_all('tr')
        for row in rows:
            tds = row.find_all('td')
            if len(tds) >= 10:
                first_val = tds[0].get_text(strip=True)
                if first_val.isdigit():
                    # This is a screener row
                    ticker_td = tds[1]
                    print(f"Ticker TD raw HTML: {ticker_td}")
                    print(f"Ticker TD get_text(): '{ticker_td.get_text(strip=True)}'")
                    # Try finding specific anchors/classes
                    for a in ticker_td.find_all('a'):
                        print(f"  Anchor: text='{a.get_text(strip=True)}', class={a.get('class')}, href={a.get('href')}")
                    break
        else:
            continue
        break

test()
