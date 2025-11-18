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
BASE_URL = "https://www.exploit-db.com/ajax/system/search"
HEADERS = {"User-Agent": "Mozilla/5.0 (WINDOWS NT 10.0; Win64; x64)",
           "X-Requested-With": "XMLHttpRequest",
           "Content-Type": "application/json",
           "Accept": "application/json"}


"""
    - Scrapes a single page from exploit-db
    - returns values desired from the site  
"""
def scrape_page(start=0, length=50):

    params = {
        "draw": 1,
        "columns": [
            {"data": "date", "name": "", "searchable": True, "orderable": True},
            {"data": "description", "searchable": True, "orderable": False},
            {"data": "author", "searchable": True, "orderable": True},
            {"data": "type", "searchable": True, "orderable": True},
            {"data": "platform", "searchable": True, "orderable": True},
            {"data": "port", "searchable": True, "orderable": True}
        ],
        "order": [{"column": 0, "dir": "desc"}],
        "start": start,
        "length": length,
        "search": {"value": "", "regex": False}
    }

    r = requests.post(BASE_URL, json=params, headers=HEADERS)
    data = r.json()

    exploits = []

    for row in data.get("data", []): 
        exploits.append({
            "date": row["date"],
            "title": row["title"],
            "platform": row["platform"],
            "type": row["type"]
        })

    return exploits


"""
    - Scrapes multiple pages from exploit-db
        - for n in pages
"""
def scrape_site(pages=3, page_size=50):
    all_data = []
    
    for i in range(pages):
        print(f"[+] Scraping page {i+1}...")
        start = i * page_size
        page_data = scrape_page(start=start, length=page_size)
        all_data.extend(page_data)
        time.sleep(1)

    return all_data


def print_vulns(data):
    print("\n==============================")
    print("       EXPLOIT STATS")
    print("==============================")

    total = len(data)
    if total == 0:
        print("Nothing was scraped")
        return
    
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
    data = scrape_site(pages=3)
    print_vulns(data)
