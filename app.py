# app.py - Wedding Anniversary Gift Suggester PRO (with images, prices & ratings)
# Run: streamlit run app.py

import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse
import re

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

# --- Enhanced Amazon Search with Image, Price & Rating ---
def search_amazon(query, tag, num_results=5):
    url = f"https://www.amazon.com/s?k={urllib.parse.quote(query)}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.find_all("div", {"data-component-type": "s-search-result"})[:num_results]
        products = []
        for item in items:
            asin = item.get("data-asin")
            if not asin:
                continue

            # Title
            title_tag = item.find("h2")
            title = title_tag.get_text(strip=True) if title_tag else "No title"

            # Link
            link = f"https://www.amazon.com/dp/{asin}/?tag={tag}"

            # Image
            img_tag = item.find("img", {"class": "s-image"})
            img = img_tag["src"] if img_tag else "https://via.placeholder.com/300x300.png?text=No+Image"

            # Price
            price_whole = item.find("span", {"class": "a-price-whole"})
            price_frac = item.find("span", {"class": "a-price-fraction"})
            price_sym = item.find("span", {"class": "a-price-symbol"})
            price = "".join([price_sym.get_text() if price_sym else "$",
                            price_whole.get_text() if price_whole else "",
                            price_frac.get_text() if price_frac else "00"]) if price_whole else "Price not available"

            # Rating
            rating_tag = item.find("span", {"class": "a-icon-alt"})
            rating = rating_tag.get_text(strip=True).split()[0] if rating_tag else "N/A"

            products.append({
                "title": title,
                "link": link,
                "image": img,
                "price": price,
                "rating": rating
            })
        return products if products else [{"title": "No results found.", "link": "#", "image": "", "price": "", "rating": ""}]
    except Exception as e:
        return [{"title": f"Error: {str(e)}", "link": "#", "image": "", "price": "", "rating": ""}]

# --- Streamlit App ---
st.set_page_config(page_title="GiftGenius Pro", page_icon="💎", layout="wide")

st.title("💍 GiftGenius Pro – Anniversary Gift Finder")
st.markdown("### Instant gift ideas + Amazon affiliate links with **your tag**")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    affiliate_tag = st.text_input("Your Amazon Tag", value="ssbudge604-22", help="e.g., yourname-20")
    year = st.number_input("Anniversary Year", min_value=1, max_value=70, value=10, step=1)
    num_gifts = st.slider("Gifts per theme", 3, 8, 5)

# Theme display
if year in ANNIVERSARIES:
    trad = ANNIVERSARIES[year]["traditional"]
    mod = ANNIVERSARIES[year]["modern"]
    st.success(f"**{year}th Anniversary** – Traditional: **{trad}** | Modern: **{mod}**")
else:
    st.warning(f"No standard theme for year {year}. Using general searches.")
    trad = mod = "Anniversary Gift"

# Auto-search when year changes
if "last_year" not in st.session_state:
    st.session_state.last_year = year

if year != st.session_state.last_year:
    st.session_state.last_year = year
    st.session_state.clear_results = True

# Search buttons
col1, col2 = st.columns(2)
with col1:
    if st.button(f"🔍 Traditional Gifts ({trad})", use_container_width=True) or st.session_state.get("clear_results"):
        with st.spinner("Searching Amazon for traditional gifts..."):
            st.session_state.trad_results = search_amazon(f"{year}th anniversary {trad} gift", affiliate_tag, num_gifts)
        st.session_state.clear_results = False

with col2:
    if st.button(f"🔍 Modern Gifts ({mod})", use_container_width=True) or st.session_state.get("clear_results"):
        with st.spinner("Searching Amazon for modern gifts..."):
            st.session_state.mod_results = search_amazon(f"{year}th anniversary {mod} gift", affiliate_tag, num_gifts)
        st.session_state.clear_results = False

# Display results
if "trad_results" in st.session_state:
    st.subheader(f"🎁 Traditional – {trad}")
    cols = st.columns(min(len(st.session_state.trad_results), 4))
    for idx, prod in enumerate(st.session_state.trad_results):
        with cols[idx % 4]:
            if prod["image"]:
                st.image(prod["image"], use_column_width=True)
            st.markdown(f"**{prod['title'][:80]}...**")
            if prod["rating"] != "N/A":
                st.markdown(f"⭐ **{prod['rating']}** • **{prod['price']}**")
            else:
                st.markdown(f"**{prod['price']}**")
            st.markdown(f"[🛒 Buy Now]({prod['link']})")

if "mod_results" in st.session_state:
    st.subheader(f"💎 Modern – {mod}")
    cols = st.columns(min(len(st.session_state.mod_results), 4))
    for idx, prod in enumerate(st.session_state.mod_results):
        with cols[idx % 4]:
            if prod["image"]:
                st.image(prod["image"], use_column_width=True)
            st.markdown(f"**{prod['title'][:80]}...**")
            if prod["rating"] != "N/A":
                st.markdown(f"⭐ **{prod['rating']}** • **{prod['price']}**")
            else:
                st.markdown(f"**{prod['price']}**")
            st.markdown(f"[Buy Now]({prod['link']})")

# Footer
st.markdown("---")
st.caption("Made with ❤️ by Grok • All links include your affiliate tag • Live Amazon data • Deploy free on [Streamlit Cloud](https://share.streamlit.io)")

# Auto-run on first load
if "first_run" not in st.session_state:
    st.session_state.first_run = False
    st.rerun()
