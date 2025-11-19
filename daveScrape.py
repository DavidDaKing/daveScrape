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
BASE_URL = "https://www.exploit-db.com"
HEADERS = {
        "authority": "www.exploit-db.com",
        "sec-ch-ua": '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
        "accept": "application/json, text/javascript, */*; q=0.01",
        "x-requested-with": "XMLHttpRequest",
        "sec-ch-ua-mobile": "?0",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://www.exploit-db.com/",
        "accept-language": "en-US,en;q=0.9",

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
def scrape_page():

    exploits = []

    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    # select what you want

    title = soup.select_one('h1').text
    text = soup.select_one('p').text
    link = soup.select_one('a').get('href')

    print(title)
    print(text)
    print(link)


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
    scrape_page()
    #data = scrape_site(pages=3)
    #print_vulns(data)
