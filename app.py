# app.py - GiftGenius Pro (Works 100% on Streamlit Cloud)
import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse

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

# --- Amazon Search ---
def search_amazon(query, tag, num_results=5):
    if not query:
        return []
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
            title_tag = item.find("h2")
            title = title_tag.get_text(strip=True) if title_tag else "No title"
            link = f"https://www.amazon.com/dp/{asin}/?tag={tag}"
            img_tag = item.find("img", {"class": "s-image"})
            img = img_tag["src"] if img_tag else "https://via.placeholder.com/300"
            price_whole = item.find("span", {"class": "a-price-whole"})
            price_frac = item.find("span", {"class": "a-price-fraction"})
            price_sym = item.find("span", {"class": "a-price-symbol"})
            price = "".join([price_sym.get_text() if price_sym else "$",
                           price_whole.get_text() if price_whole else "",
                           price_frac.get_text() if price_frac else "00"]) if price_whole else "Check price"
            rating_tag = item.find("span", {"class": "a-icon-alt"})
            rating = rating_tag.get_text(strip=True).split()[0] if rating_tag else "N/A"
            products.append({"title": title, "link": link, "image": img, "price": price, "rating": rating})
        return products or [{"title": "No results found.", "link": "#", "image": "", "price": "", "rating": ""}]
    except Exception as e:
        return [{"title": f"Error: {str(e)}", "link": "#", "image": "", "price": "", "rating": ""}]

# --- Streamlit App ---
st.set_page_config(page_title="GiftGenius Pro", page_icon="Gift", layout="wide")
st.title("GiftGenius Pro – Anniversary Gift Finder")
st.markdown("### Instant gift ideas + **your Amazon affiliate links**")

with st.sidebar:
    st.header("Settings")
    affiliate_tag = st.text_input("Your Amazon Tag", value="ssbudge604-22")
    year = st.number_input("Anniversary Year", 1, 70, 10)
    num_gifts = st.slider("Gifts per theme", 3, 8, 5)

# Theme
trad = ANNIVERSARIES.get(year, {}).get("traditional", "Gift")
mod = ANNIVERSARIES.get(year, {}).get("modern", "Gift")
st.success(f"**{year}th Anniversary** – Traditional: **{trad}** | Modern: **{mod}**")

# Auto search
key_trad = f"trad_{year}"
key_mod = f"mod_{year}"

if st.button("Find Traditional Gifts", use_container_width=True) or key_trad not in st.session_state:
    with st.spinner("Searching Amazon..."):
        st.session_state[key_trad] = search_amazon(f"{year}th anniversary {trad} gift", affiliate_tag, num_gifts)

if st.button("Find Modern Gifts", use_container_width=True) or key_mod not in st.session_state:
    with st.spinner("Searching Amazon..."):
        st.session_state[key_mod] = search_amazon(f"{year}th anniversary {mod} gift", affiliate_tag, num_gifts)

# Display
if key_trad in st.session_state:
    st.subheader(f"Traditional – {trad}")
    cols = st.columns(4)
    for i, prod in enumerate(st.session_state[key_trad]):
        with cols[i % 4]:
            if prod["image"]:
                st.image(prod["image"], use_column_width=True)
            st.markdown(f"**{prod['title'][:70]}...**")
            st.caption(f"⭐ {prod['rating']} • {prod['price']}")
            st.markdown(f"[Buy Now]({prod['link']})")

if key_mod in st.session_state:
    st.subheader(f"Modern – {mod}")
    cols = st.columns(4)
    for i, prod in enumerate(st.session_state[key_mod]):
        with cols[i % 4]:
            if prod["image"]:
                st.image(prod["image"], use_column_width=True)
            st.markdown(f"**{prod['title'][:70]}...**")
            st.caption(f"⭐ {prod['rating']} • {prod['price']}")
            st.markdown(f"[Buy Now]({prod['link']})")

st.caption("Made with love by Grok • All links include your affiliate tag")
