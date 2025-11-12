# app.py - GiftGenius Pro (No warnings, fully working)
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

def search_amazon(query, tag, num_results=5):
    url = f"https://www.amazon.com/s?k={urllib.parse.quote(query)}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        items = soup.find_all("div", {"data-component-type": "s-search-result"})[:num_results]
        products = []
        for item in items:
            asin = item.get("data-asin")
            if not asin: continue
            title = item.find("h2").get_text(strip=True) if item.find("h2") else "Gift"
            link = f"https://www.amazon.com/dp/{asin}/?tag={tag}"
            img_tag = item.find("img", {"class": "s-image"})
            img = img_tag["src"] if img_tag else "https://via.placeholder.com/300"
            price_whole = item.find("span", {"class": "a-price-whole"})
            price_frac = item.find("span", {"class": "a-price-fraction"})
            price_sym = item.find("span", {"class": "a-price-symbol"})
            price = (price_sym.get_text("") if price_sym else "$") + \
                    (price_whole.get_text("") if price_whole else "") + \
                    (price_frac.get_text("") if price_frac else "")
            price = price or "Check price"
            rating_tag = item.find("span", {"class": "a-icon-alt"})
            rating = rating_tag.get_text(strip=True).split()[0] if rating_tag else "N/A"
            products.append({"title": title, "link": link, "image": img, "price": price, "rating": rating})
        return products or [{"title": "No results", "link": "#", "image": "", "price": "", "rating": ""}]
    except:
        return [{"title": "Search failed", "link": "#", "image": "", "price": "", "rating": ""}]

# --- UI ---
st.title("GiftGenius Pro – Anniversary Gift Finder")
st.markdown("### Instant gift ideas + **your Amazon affiliate links**")

with st.sidebar:
    tag = st.text_input("Amazon Tag", value="ssbudge604-22", help="e.g., yourname-20")
    year = st.number_input("Anniversary Year", 1, 70, 10, step=1)
    num = st.slider("Gifts per theme", 3, 8, 5)

trad = ANNIVERSARIES.get(year, {"traditional": "Gift"})["traditional"]
mod = ANNIVERSARIES.get(year, {"modern": "Gift"})["modern"]

st.success(f"**{year}th Anniversary** – Traditional: **{trad}** | Modern: **{mod}**")

# Auto-load on first run or year change
if "last_year" not in st.session_state:
    st.session_state.last_year = year

if year != st.session_state.last_year:
    st.session_state.last_year = year
    st.session_state.clear()

# Search
col1, col2 = st.columns(2)
with col1:
    if st.button("Traditional Gifts", use_container_width=True) or "trad" not in st.session_state:
        with st.spinner("Searching traditional gifts..."):
            st.session_state.trad = search_amazon(f"{year}th anniversary {trad} gift", tag, num)
with col2:
    if st.button("Modern Gifts", use_container_width=True) or "mod" not in st.session_state:
        with st.spinner("Searching modern gifts..."):
            st.session_state.mod = search_amazon(f"{year}th anniversary {mod} gift", tag, num)

# Display Traditional
if "trad" in st.session_state:
    st.subheader(f"Traditional – {trad}")
    cols = st.columns(4)
    for i, p in enumerate(st.session_state.trad):
        with cols[i % 4]:
            if p["image"]:
                st.image(p["image"], use_container_width=True)  # Fixed deprecation
            st.markdown(f"**{p['title'][:80]}...**")
            st.caption(f"Rating: {p['rating']} • {p['price']}")
            st.markdown(f"[Buy Now]({p['link']})")

# Display Modern
if "mod" in st.session_state:
    st.subheader(f"Modern – {mod}")
    cols = st.columns(4)
    for i, p in enumerate(st.session_state.mod):
        with cols[i % 4]:
            if p["image"]:
                st.image(p["image"], use_container_width=True)  # Fixed deprecation
            st.markdown(f"**{p['title'][:80]}...**")
            st.caption(f"Rating: {p['rating']} • {p['price']}")
            st.markdown(f"[Buy Now]({p['link']})")

st.markdown("---")
st.caption("Made with love by Grok • All links include your affiliate tag • Live Amazon data")
