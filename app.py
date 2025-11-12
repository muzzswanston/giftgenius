# app.py - GiftGenius Pro (Perfect, No Errors, No Affiliate Mention)
import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse

st.set_page_config(page_title="GiftGenius Pro", page_icon="Gift", layout="wide")

# --- Anniversary Themes ---
ANNIVERSARIES = {
    1: {"traditional": "Paper", "modern": "Clocks"},
    2: {"traditional": "Cotton", "modern": "China"},
    3: {"traditional": "Leather", "modern": "Crystal/Glass"},
    4: {"traditional": "Fruit/Flowers", "modern": "Appliances"},
    5: {"traditional": "Wood", "modern": "Silverware"},
    6: {"traditional": "Iron", "modern": "Wood"},
    7: {"traditional": "Copper/Wool", "modern": "Desk Sets"},
    8: {"traditional": "Bronze/Pottery", "modern": "Linen/Lace"},
    9: {"traditional": "Willow/Pottery", "modern": "Leather"},
    10: {"traditional": "Aluminum/Tin", "modern": "Diamond Jewelry"},
    15: {"traditional": "Crystal", "modern": "Watches"},
    20: {"traditional": "China", "modern": "Platinum"},
    25: {"traditional": "Silver", "modern": "Silver"},
    30: {"traditional": "Pearl", "modern": "Diamond"},
    40: {"traditional": "Ruby", "modern": "Ruby"},
    50: {"traditional": "Gold", "modern": "Gold"},
    60: {"traditional": "Diamond", "modern": "Diamond"},
}

def search_amazon(query, num_results=5):
    url = f"https://www.amazon.com/s?k={urllib.parse.quote(query)}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }
    try:
        r = requests.get(url, headers=headers, timeout=20)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        items = soup.select('div[data-component-type="s-search-result"]')[:num_results]
        products = []
        for item in items:
            asin = item.get("data-asin")
            if not asin:
                continue

            # Title
            title_tag =
