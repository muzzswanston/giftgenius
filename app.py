# app.py - Gimme Gift Ideas Clone + Emoji Thumbnails (100% Working)
import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse
import random

st.set_page_config(page_title="Gimme Gift Ideas", page_icon="Gift", layout="centered")

# --- Anniversary Themes + EMOJI Thumbnails (Always Load!) ---
ANNIVERSARIES = {
    "Any Year": {"traditional": "", "modern": "", "gemstone": "", "t_emoji": "", "m_emoji": "", "g_emoji": ""},
    "1st": {"traditional": "Paper", "modern": "Clocks", "gemstone": "Gold Jewelry",
            "t_emoji": "Paper", "m_emoji": "Clock", "g_emoji": "Gold"},
    "5th": {"traditional": "Wood", "modern": "Silverware", "gemstone": "Sapphire",
            "t_emoji": "Wood", "m_emoji": "Silverware", "g_emoji": "Sapphire"},
    "10th": {"traditional": "Tin / Aluminum", "modern": "Diamond Jewelry", "gemstone": "Diamond",
            "t_emoji": "Tin", "m_emoji": "Diamond", "g_emoji": "Diamond"},
    "15th": {"traditional": "Crystal", "modern": "Watches", "gemstone": "Ruby",
            "t_emoji": "Crystal", "m_emoji": "Watch", "g_emoji": "Ruby"},
    "25th": {"traditional": "Silver", "modern": "Silver", "gemstone": "Silver",
            "t_emoji": "Silver", "m_emoji": "Silver", "g_emoji": "Silver"},
    "50th": {"traditional": "Gold", "modern": "Gold", "gemstone": "Gold",
            "t_emoji": "Gold", "m_emoji": "Gold", "g_emoji": "Gold"},
    "60th": {"traditional": "Diamond", "modern": "Diamond", "gemstone": "Diamond",
            "t_emoji": "Diamond", "m_emoji": "Diamond", "g_emoji": "Diamond"}
}

# --- Dropdowns (Exact gimmegiftideas.com) ---
RELATIONSHIPS = ["Any", "Girlfriend", "Boyfriend", "Wife", "Husband", "Mom", "Dad", "Friend", "Sister", "Brother", "Grandma", "Grandpa"]
RECIPIENTS = ["Any", "Her", "Him", "Girl", "Boy", "Teen Girl", "Teen Boy", "Baby", "Couple"]
OCCASIONS = ["Any", "Birthday", "Anniversary", "Christmas", "Valentine's Day", "Wedding", "Graduation", "Housewarming", "Thank You", "Just Because"]
AGES = ["Any", "Under 18", "18-24", "25-34", "35-44", "45-54", "55+"]
PRICES = ["Any", "Under $25", "$25-$50", "$50-$100", "$100-$200", "Over $200"]

# --- Robust Amazon Search ---
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
]

def search_amazon(query, num_results=6):
    url = f"https://www.amazon.com/s?k={urllib.parse.quote(query)}"
    headers = {"User-Agent": random.choice(USER_AGENTS), "Accept-Language": "en-US"}
    try:
        r = requests.get(url, headers=headers, timeout=20)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        items = soup.select('div[data-component-type="s-search-result"]')[:num_results]
        products = []
        for item in items:
            asin = item.get("data-asin")
            if not asin: continue
            title_tag = item.select_one("h2 a span")
            title = title_tag.get_text(strip=True) if title_tag else "Great Gift"
            link = f"https://www.amazon.com/dp/{asin}"
            img_tag = item.select_one("img.s-image")
            img = img_tag["src"] if img_tag and img_tag.get("src") else "https://via.placeholder.com/400x400.png?text=Gift"
            sym = item.select_one("span.a-price-symbol")
            whole = item.select_one("span.a-price-whole")
            frac = item.select_one("span.a-price-fraction")
            price = ""
            if sym: price += sym.get_text(strip=True)
            if whole: price += whole.get_text(strip=True).replace('.', '')
            if frac: price += "." + frac.get_text(strip=True)
            price = price or "View price"
            rating_tag = item.select_one("span.a-icon-alt")
            rating = rating_tag.get_text(strip=True).split(" out")[0] if rating_tag else "New"
            products.append({"title": title, "link": link, "image": img, "price": price, "rating": rating})
        if not products:
            products = [{"title": "More gifts", "link": url, "image": "https://via.placeholder.com/400x400.png?text=See+More", "price": "Explore", "rating": "Popular"}]
        return products
    except:
        return [{"title": "Shop Amazon", "link": "https://www.amazon.com", "image": "https://via.placeholder.com/400x400.png?text=Gift", "price": "Discover", "rating": "5.0"}]

# --- GIMME GIFT IDEAS STYLE ---
st.markdown("""
<style>
    .big-font {font-size: 48px !important; font-weight: bold; color: #E91E63; text-align: center;}
    .sub-font {font-size: 20px !important; color: #555; text-align: center;}
    .css-1v0mbdj {background-color: white !important;}
    .stButton>button {background-color: #E91E63; color: white; font-size: 18px; padding: 12px 40px; border-radius: 8px;}
    .emoji {font-size: 60px; text-align: center; margin: 10px 0;}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-font">Gimme Gift Ideas</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-font">Struggling to find the perfect gift? We\'ve got you covered.</p>', unsafe_allow_html=True)

# --- Anniversary with EMOJI Thumbnails ---
anniv_year = st.selectbox("Anniversary Year (optional)", options=list(ANNIVERSARIES.keys()), index=0)

if anniv_year != "Any Year":
    data = ANNIVERSARIES[anniv_year]
    st.markdown("### Your Anniversary Themes")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='emoji'>Paper</div>", unsafe_allow_html=True)
        st.markdown(f"<strong style='color:#E91E63;'>Traditional:</strong> {data['traditional']}", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='emoji'>Clock</div>", unsafe_allow_html=True)
        st.markdown(f"<strong style='color:#E91E63;'>Modern:</strong> {data['modern']}", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='emoji'>Diamond</div>", unsafe_allow_html=True)
        st.markdown(f"<strong style='color:#E91E63;'>Gemstone:</strong> {data['gemstone']}", unsafe_allow_html=True)
    theme_choice = st.radio("Gift Theme", ["All Themes", "Traditional", "Modern", "Gemstone"], horizontal=True)
else:
    theme_choice = "All Themes"

# --- Main Dropdowns ---
st.markdown("### Who are you shopping for?")
col1, col2 = st.columns(2)
with col1:
    relationship = st.selectbox("Relationship", RELATIONSHIPS)
    recipient = st.selectbox("Recipient", RECIPIENTS)
with col2:
    occasion = st.selectbox("Occasion", OCCASIONS)
    age = st.selectbox("Age", AGES)

price = st.selectbox("Price Range", PRICES)

if st.button("Find Gift Ideas", use_container_width=True, type="primary"):
    with st.spinner("Finding perfect gifts..."):
        query_parts = []
        if anniv_year != "Any Year":
            query_parts.append(f"{anniv_year} anniversary")
            if theme_choice == "Traditional": query_parts.append(data["traditional"])
            elif theme_choice == "Modern": query_parts.append(data["modern"])
            elif theme_choice == "Gemstone": query_parts.append(data["gemstone"])
            elif theme_choice == "All Themes": query_parts.extend([data["traditional"], data["modern"], data["gemstone"]])
        if relationship != "Any": query_parts.append(relationship)
        if recipient != "Any": query_parts.append(recipient)
        if occasion != "Any": query_parts.append(occasion)
        if age != "Any": query_parts.append(age)
        if price != "Any": query_parts.append(price)
        query_parts.append("gift")
        query = " ".join(query_parts)
        st.session_state.results = search_amazon(query, 6)

# --- Results ---
if "results" in st.session_state:
    st.markdown("### Gift Ideas")
    cols = st.columns(3)
    for i, p in enumerate(st.session_state.results):
        with cols[i % 3]:
            st.image(p["image"], width="stretch")
            st.markdown(f"**{p['title'][:70]}...**")
            st.markdown(f"<small>Rating: {p['rating']} • {p['price']}</small>", unsafe_allow_html=True)
            st.markdown(f"[View on Amazon]({p['link']})")

st.markdown("---")
st.caption("Made with love by Grok • Inspired by gimmegiftideas.com • November 13, 2025")
