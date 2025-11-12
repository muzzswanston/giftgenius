# app.py - GiftGenius Pro (Clean, Reliable, No Affiliate Mention)
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
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36",
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
            title_tag = item.select_one("h2 a")
            title = title_tag.get_text(strip=True) if title_tag else "Great Gift Idea"

            # Link
            link = f"https://www.amazon.com/dp/{asin}"

            # Image - multiple fallback methods
            img = ""
            img_tag = item.select_one("img.s-image")
            if img_tag and img_tag.get("src"):
                img = img_tag["src"]
            elif img_tag and img_tag.get("data-image-source-density"):
                img = img_tag.get("srcset", "").split(",")[0].split(" ")[0]
            else:
                img = "https://via.placeholder.com/300x300.png?text=Gift"

            # Price
            price_whole = item.select_one("span.a-price-whole")
            price_frac = item.select_one("span.a-price-fraction")
            price_sym = item.select_one("span.a-price-symbol")
            price = ""
            if price_sym: price += price_sym.get_text(strip=True)
            if price_whole: price += price_whole.get_text(strip=True)
            if price_frac: price += price_frac.get_text(strip=True)
            price = price or "View price"

            # Rating
            rating_tag = item.select_one("span.a-icon-alt")
            rating = rating_tag.get_text(strip=True).split(" out")[0] if rating_tag else "N/A"

            products.append({
                "title": title,
                "link": link,
                "image": img,
                "price": price,
                "rating": rating
            })
        # Fallback if no results
        if not products:
            products = [{
                "title": f"More {query} gifts available on Amazon",
                "link": url,
                "image": "https://via.placeholder.com/300x300.png?text=See+More",
                "price": "View on Amazon",
                "rating": "N/A"
            }]
        return products
    except Exception as e:
        # Ultimate fallback
        return [{
            "title": "Explore gift ideas on Amazon",
            "link": "https://www.amazon.com",
            "image": "https://via.placeholder.com/300x300.png?text=Gifts",
            "price": "Open Amazon",
            "rating": "N/A"
        }]

# --- UI ---
st.title("GiftGenius Pro")
st.markdown("### Find the perfect wedding anniversary gift in seconds")

with st.sidebar:
    st.header("Settings")
    year = st.number_input("Anniversary Year", 1, 70, 10, step=1)
    num = st.slider("Gifts per theme", 3, 8, 5)

# Get themes
theme_data = ANNIVERSARIES.get(year, {"traditional": "Special Gift", "modern": "Special Gift"})
trad = theme_data["traditional"]
mod = theme_data["modern"]

st.success(f"**{year}th Anniversary** – Traditional: **{trad}** | Modern: **{mod}**")

# Auto-load on year change or first run
if "last_year" not in st.session_state or year != st.session_state.last_year:
    st.session_state.last_year = year
    st.session_state.clear_results = True

col1, col2 = st.columns(2)
with col1:
    if st.button("Traditional Gifts", use_container_width=True) or st.session_state.get("clear_results"):
        with st.spinner("Finding
