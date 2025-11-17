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
HEADERS = {"User-Agent": "Mozilla/5.0"}


"""
    - Scrapes a single page from exploit-db
    - returns values desired from the site  
"""
def scrape_page(page_num):
    
    return 


"""
    - Scrapes multiple pages from exploit-db
        - for n in pages
"""
def scrape_site(n):
    return

if __name__ == "__main__":
    print("helllo world")
