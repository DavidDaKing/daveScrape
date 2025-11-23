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
import json
import os

# Include base URL and headeri


## Some version of this is to keep, retype rest
BASE_URL = "https://exploit-db.com/search" # Works for a plain example website 
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "X-Requested-With":"XMLHttpRequest",
    "Accept":"application/json",

}

row_retrieval_cap = 50

row_start_offset = 0

# Create file to save data to 
data_json = './exportData.json'
if os.path.exists(data_json):
    with open(data_json, "w") as filp:
        pass

"""
    - Scrapes a single page from exploit-db
    - returns values desired from the site  
"""
def scrape_page(start=0, length=50):

    params = {
        "draw": 1,
        "columns[0][data]": "date",
        "start": start,
        "length": length,
    }

    r = requests.get(BASE_URL, headers=HEADERS, params=params)

    r.raise_for_status()


    return r.json()["data"]


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

    for e in data:
        output = {
            "id": e["id"],
            "description": e["description"],
            #"date": e.get("date"),
            "author": e["author"],
            "platform": e["platform"],
            "type": e["type"],    
        }
        print(output)
        print("~~~~~~~~~")


if __name__ == "__main__":
    scrape_page()
    data = scrape_site(pages=3, page_size=50)
    print_vulns(data)
