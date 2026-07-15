# Author: Ahmet Aksoy
# Date: 27.05.2026
# Python3.12 Ubuntu 24.04

"""
BeautifulSoup Web Scraping Example
Demonstrates HTML parsing, DOM traversal, and data extraction using 
the third-party 'requests' and 'beautifulsoup4' packages.
"""

import requests
from bs4 import BeautifulSoup


def scrape_mock_blog(url: str) -> None:
    """
    Fetches raw HTML from a target server and processes the DOM tree
    to extract structured article parameters.
    """
    print(f"--- Initiating Web Scraping Connection ---")
    print(f"Target URL: {url}\n")

    try:
        # 1. Send an HTTP GET request to the target web server
        # Adding a basic User-Agent header simulates a standard browser request
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0"
        }
        response = requests.get(url, headers=headers, timeout=10)

        # Verify that the server responded with a 200 OK status code
        if response.status_code != 200:
            print(f"[Error] Failed to connect. HTTP Status Code: {response.status_code}")
            return

        # 2. Ingest the raw HTML payload into the BeautifulSoup DOM engine
        # We explicitly command it to use Python's built-in 'html.parser'
        soup = BeautifulSoup(response.text, "html.parser")

        print("=== Extracted Article Elements ===")
        
        # 3. Target specific container blocks (Simulating scraping a blog timeline)
        # We assume articles are wrapped inside <article class="blog-post"> elements
        articles = soup.find_all("article", class_="blog-post")

        if not articles:
            print("[Warning] No elements matched the target class layout.")
            print("Displaying raw page title instead as fallback:")
            print(f"Page Title Tag -> {soup.title.string if soup.title else 'No Title Found'}")
            return

        for idx, article in enumerate(articles, start=1):
            # Extract the nested title link element inside the <h2> header tag
            title_element = article.find("h2", class_="post-title")
            title_text = title_element.get_text(strip=True) if title_element else "No Title"
            
            # Extract hyperlinks safely
            link_element = article.find("a")
            link_href = link_element["href"] if link_element and link_element.has_attr("href") else "No Link"

            # Extract semantic metadata tags (e.g., author name)
            author_element = article.find("span", class_="post-author")
            author_name = author_element.get_text(strip=True) if author_element else "Anonymous"

            print(f"\n[Post #{idx}]")
            print(f" Title  : {title_text}")
            print(f" Author : {author_name}")
            print(f" Link   : {link_href}")

    except requests.exceptions.RequestException as e:
        print(f"[Critical Network Error] Connection timed out or failed: {e}")


if __name__ == "__main__":
    # Using an official, public scraping sandbox endpoint provided by the QA community
    target_sandbox_url = "https://example.com" 
    # target_sandbox_url = "https://gurmezin.com"
    
    # Note: Since example.com has a very flat structure, the code falls back gracefully 
    # to printing the page title, showcasing how a robust scraper handles variable layouts.
    scrape_mock_blog(target_sandbox_url)
