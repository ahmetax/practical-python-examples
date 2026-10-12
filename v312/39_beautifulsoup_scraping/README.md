# Project 39: Web Scraping with requests and BeautifulSoup

A short scraper that downloads a web page with `requests` and parses it with `BeautifulSoup`. It looks for blog post blocks (`<article class="blog-post">`) and prints the title, author and link of each one. If the page has no such blocks, it falls back to printing the page `<title>`.

## How It Works
- `requests.get()` downloads the page with a browser-like `User-Agent` header and a 10-second timeout.
- If the status code is not `200`, the script prints it and stops. Network errors (DNS failure, timeout, refused connection) are caught as `requests.exceptions.RequestException`.
- `BeautifulSoup(response.text, "html.parser")` builds the parse tree with Python's built-in HTML parser, so no extra parser such as `lxml` is needed.
- `find_all("article", class_="blog-post")` collects the post blocks. Inside each block, the script reads:
  - the text of `<h2 class="post-title">` (or `No Title`),
  - the `href` of the first `<a>` (or `No Link`),
  - the text of `<span class="post-author">` (or `Anonymous`).
- If no post blocks are found, it prints the page title instead.

The default target is `https://example.com`, which has no `<article>` elements, so a normal run always takes the fallback path and prints only the page title. To see the post-extraction loop at work, point `target_sandbox_url` in `main.py` at a page that uses this markup. `https://gurmezin.com` (commented out in the code) does not use it either and also ends in the fallback.

## Project Structure
```text
39_beautifulsoup_scraping/
├── main.py
├── README.md
└── README_TR.md
```

## Requirements
- Python 3.10 or newer for the current `requests` release (the script itself uses nothing newer than f-strings). Tested on 3.12.3.
- `requests` (tested with 2.34.2) and `beautifulsoup4` (tested with 4.15.0).
- Internet access.

## Running
On Ubuntu 24.04, `pip install` outside a virtual environment fails with `externally-managed-environment`, so create one first:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install requests beautifulsoup4
python3 main.py
```
Ubuntu's own `python3-requests` and `python3-bs4` packages (`sudo apt install python3-requests python3-bs4`) also work; the script was tested with those versions too (2.31.0 and 4.12.3).

## Sample Output (Python 3.12.3)
```text
--- Initiating Web Scraping Connection ---
Target URL: https://example.com

=== Extracted Article Elements ===
[Warning] No elements matched the target class layout.
Displaying raw page title instead as fallback:
Page Title Tag -> Example Domain
```

When the page does contain matching blocks, each post is printed like this:
```text
[Post #1]
 Title  : Hello
 Author : Ahmet
 Link   : /a
```
This second output was produced by feeding the function a small test HTML page, not a live site.

Error cases:
```text
[Error] Failed to connect. HTTP Status Code: 404
[Critical Network Error] Connection timed out or failed: HTTPSConnectionPool(host='nonexistent.invalid', port=443): ...
```
Note that the 404 message says "Failed to connect" even though the connection worked and the server answered.

## Further Reading
- Blog post (Turkish): https://gurmezin.com/2026/09/24/beautifulsoup-ile-web-scraping-html-corbasindan-anlamli-veri-cikarmak/
- Beautiful Soup documentation: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- Requests documentation: https://requests.readthedocs.io/
