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

     - added json elements - DAB 12/8/2025

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

## Writing on .json 

def write_json(data, filename="exportData.json"):
    with open(filename, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)
    return filename

## Write .json on sql 

def json_to_sql(json_file, sql_file, table_name="vulns"):

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    with open(sql_file, "w", encoding="utf-8") as f:
        f.write(f"-- SQL script to insert data into the {table_name} table\n\n")
        f.write(f"CREATE TABLE IF NOT EXISTS {table_name} (\n")
        f.write("    id INT PRIMARY KEY,\n")
        f.write("    description TEXT,\n")
        f.write("    author TEXT,\n")
        f.write("    platform TEXT,\n")
        f.write("    type TEXT\n")
        f.write(");\n\n")

        for entry in data:
            # Safely retrieve and process each field
            id = entry.get("id", "NULL")
            if id is None:
                id = "NULL"

            # Handle 'description' field
            description = entry.get("description", "")
            if isinstance(description, list):  # If it's a list, join it into a string
                description = " ".join(description)
            elif not isinstance(description, str):  # If it's not a string, convert to an empty string
                description = ""
            description = description.replace("'", "''")  # Escape single quotes

            # Handle 'author' field
            author = entry.get("author", "")
            if not isinstance(author, str):  # Ensure it's a string
                author = ""
            author = author.replace("'", "''")

            # Handle 'platform' field
            platform = entry.get("platform", "")
            if not isinstance(platform, str):  # Ensure it's a string
                platform = ""
            platform = platform.replace("'", "''")

            # Handle 'type' field
            type_ = entry.get("type", "")
            if not isinstance(type_, str):  # Ensure it's a string
                type_ = ""
            type_ = type_.replace("'", "''")

            f.write(
                f"INSERT INTO {table_name} (id, description, author, platform, type) VALUES "
                f"({id}, '{description}', '{author}', '{platform}', '{type_}');\n"
            )

    print(f"[*] SQL file successfully created: {sql_file}")

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

    ## Data stores .json output 
    
    data = scrape_site(pages=3, page_size=50)

    ## Insert .csv save here using data as the parameter 
    fileName = write_json(data)
    print(fileName)

    json_to_sql(fileName, "exportData.sql")
    
    #print_vulns(data)
