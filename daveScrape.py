# Module dave_scrape.py

# ***************************************************
"""
    **PURPOSE**
    This tool was created to scrape information from exploit-db and then used to display 
    on a website.

    **DEVELOPER** -- 
    David Bower

    **MODIFICATION HISTORY** -- 
     - initial implementation - DAB 11/17/2025 

"""


# ***************************************************


import requests 
from bs4 import BeautifulSoup
from collections import Counter
import time

# Include base URL and header
BASE_URL = "https://www.exploit-db.com/?order_by=date&order=desc&pg="
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/",
    "DNT": "1",
    "Upgrade-Insecure-Requests": "1",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache"
}


"""
    - Scrapes a single page from exploit-db
    - returns values desired from the site  
"""
def scrape_page(page_num):
    url = BASE_URL + str(page_num)
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")

    if soup.title:
        print(f"[DEBUG] Page {page_num} Title:", soup.title.string)

        
    table = soup.find("table", id="exploits-table")
    if not table:
        return []

    rows = table.find("tbody").find_all("tr", attrs={"data-id": True})

    exploits = []

    for row in rows: 
        cols = row.find_all("td")
        if len(cols) < 5:
            continue

        date = cols[0].text.strip()
        title = cols[1].text.strip()
        platform = cols[3].text.strip()
        exploit_type = cols[4].text.strip()

        exploits.append({
            "date": date,
            "title": title,
            "platform": platform,
            "type": exploit_type
        })

    return exploits


"""
    - Scrapes multiple pages from exploit-db
        - for n in pages
"""
def scrape_site(n):
    all_data = []
    
    for i in range(1, n + 1):
        print(f"[+] Scraping page {i}...")
        page_data = scrape_page(i)
        if not page_data:
            break
        all_data.extend(page_data)
        time.sleep(1)

    return all_data


def print_vulns(data):
    print("\n==============================")
    print("       EXPLOIT STATS")
    print("==============================")

    total = len(data)
    print(f"Total vulnerablilties scraped: {total}")

    platforms = Counter(d["platform"] for d in data)
    types = Counter(d["type"] for d in data)
    years = Counter(d["date"][:4] for d in data)

    print("\n--- By Platform ---")
    for k,v in platforms.most_common():
        print(f"{k}: {v}")
    
    print("\n--- By Type ---")
    for k,v in types.most_common():
        print(f"{k}: {v}")

    print("\n--- By Year ---")
    for k,v in years.most_common():
        print(f"{k}: {v}")

if __name__ == "__main__":
    data = scrape_site(n=3)
    print_vulns(data)
