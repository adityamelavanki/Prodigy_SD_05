
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE = "https://webscraper.io"
START = BASE + "/test-sites/e-commerce/allinone/computers/laptops"

def fetch(url):
    """Returns parsed HTML using BeautifulSoup."""
    hdr = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=hdr, timeout=10)
    return BeautifulSoup(response.text, "html.parser")

def parse_products(soup):
    """Extracts product info from one listing page."""
    products = []
    for card in soup.select("div.thumbnail"):
        title_tag = card.select_one("a.title")
        products.append({
            "Name": title_tag["title"],
            "Price": card.select_one("h4.price").text.strip(),
            "Rating": (
                card.select_one("p[data-rating]")["data-rating"]
                if card.select_one("p[data-rating]") else
                str(len(card.select("span.glyphicon-star")))
            ),
            "Description": card.select_one("p.description").text.strip(),
            "URL": urljoin(BASE, title_tag["href"])
        })
    return products

def next_page(soup):
    """Returns the absolute URL of the next page, or None if last page."""
    nxt = soup.select_one("ul.pagination li.active + li a")
    return urljoin(BASE, nxt["href"]) if nxt else None

# ---------- Crawl all pages ----------
print("⏳ Starting scrape …")
data = []
url = START
while url:
    print("  →", url)
    page = fetch(url)
    data.extend(parse_products(page))
    url = next_page(page)

print(f"✅ Scraped {len(data)} products.")

# ---------- Save CSV ----------
# ---------- Save CSV ----------
csv_path = "products.csv"
pd.DataFrame(data).to_csv(csv_path, index=False)
print("📄 Data saved to", csv_path)

# 👉 Open manually from VS Code or use:
# import os
# os.startfile(csv_path)  # Optional: opens file in Excel (Windows only)

