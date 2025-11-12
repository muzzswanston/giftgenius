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
        soup = BeautifulSoup(r.text, "html.parser")
        items = soup.find_all("div", {"data-component-type": "s-search-result"})[:num_results]
        products = []
        for item in items:
            asin = item.get("data-asin")
            if not asin: continue
            title = item.find("h2").get_text(strip=True) if item.find("h2") else "No title"
            link = f"https://www.amazon.com/dp/{asin}/?tag={tag}"
            img = item.find("img", {"class": "s-image"})["src"] if item.find("img", {"class": "s-image"}) else ""
            price = item.find("span", {"class": "a-price-whole"})
            price = price.get_text(strip=True) + (item.find("span", {"class": "a-price-fraction"}).get_text(strip=True) if item.find("span", {"class": "a-price-fraction"}) else "") if price else "Check price"
            rating = item.find("span", {"class": "a-icon-alt"})
            rating = rating.get_text(strip=True).split()[0] if rating else "N/A"
            products.append({"title": title, "link": link, "image": img, "price": price, "rating": rating})
        return products or [{"title": "No results", "link": "#", "image": "", "price": "", "rating": ""}]
    except:
        return [{"title": "Search failed", "link": "#", "image": "", "price": "", "rating": ""}]

# --- UI ---
st.title("GiftGenius Pro – Anniversary Gift Finder")
st.markdown("### Your personal Amazon affiliate gift generator")

with st.sidebar:
    tag = st.text_input("Amazon Tag", "ssbudge604-22")
    year = st.number_input("Year", 1, 70, 10)
    num = st.slider("Gifts", 3, 8, 5)

trad = ANNIVERSARIES.get(year, {"traditional": "Gift", "modern": "Gift"})["traditional"]
mod = ANNIVERSARIES.get(year, {"traditional": "Gift", "modern": "Gift"})["modern"]

st.success(f"**{year}th Anniversary** – Traditional: **{trad}** | Modern: **{mod}**")

col1, col2 = st.columns(2)
with col1:
    if st.button("Traditional Gifts", use_container_width=True):
        with st.spinner("Searching..."):
            st.session_state.trad = search_amazon(f"{year}th anniversary {trad} gift", tag, num)
with col2:
    if st.button("Modern Gifts", use_container_width=True):
        with st.spinner("Searching..."):
            st.session_state.mod = search_amazon(f"{year}th anniversary {mod} gift", tag, num)

# Auto-load on first run
if "trad" not in st.session_state:
    with st.spinner("Loading gifts..."):
        st.session_state.trad = search_amazon(f"{year}th anniversary {trad} gift", tag, num)
        st.session_state.mod = search_amazon(f"{year}th anniversary {mod} gift", tag, num)

# Display
if "trad" in st.session_state:
    st.subheader(f"Traditional – {trad}")
    cols = st.columns(4)
    for i, p in enumerate(st.session_state.trad):
        with cols[i%4]:
            if p["image"]: st.image(p["image"], use_column_width=True)
            st.markdown(f"**{p['title'][:70]}...**")
            st.caption(f"Rating: {p['rating']} • {p['price']}")
            st.markdown(f"[Buy Now]({p['link']})")

if "mod" in st.session_state:
    st.subheader(f"Modern – {mod}")
    cols = st.columns(4)
    for i, p in enumerate(st.session_state.mod):
        with cols[i%4]:
            if p["image"]: st.image(p["image"], use_column_width=True)
            st.markdown(f"**{p['title'][:70]}...**")
            st.caption(f"Rating: {p['rating']} • {p['price']}")
            st.markdown(f"[Buy Now]({p['link']})")

st.caption("Made with love by Grok • All links include your tag")
