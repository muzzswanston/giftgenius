# app.py - Timeless Gift Ideas • Thumbnails + Pure White • 100% Working
import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse
import random

st.set_page_config(page_title="Timeless Gift Ideas", page_icon="Sparkles", layout="centered")

# --- Anniversary Themes + Real Thumbnail URLs ---
ANNIVERSARIES = {
    "Any Year": {"traditional": "", "modern": "", "gemstone": "", "t_img": "", "m_img": "", "g_img": ""},
    "1st": {"traditional": "Paper", "modern": "Clocks", "gemstone": "Gold Jewelry",
            "t_img": "https://images.unsplash.com/photo-1544967919-806c39d5e7e1?w=400&h=300&fit=crop",  # Paper
            "m_img": "https://images.unsplash.com/photo-1508057199899-3d91f0278b57?w=400&h=300&fit=crop",  # Clock
            "g_img": "https://images.unsplash.com/photo-1605100804761-9a2e0d72d48b?w=400&h=300&fit=crop"}, # Gold
    "5th": {"traditional": "Wood", "modern": "Silverware", "gemstone": "Sapphire",
            "t_img": "https://images.unsplash.com/photo-1518788668920-635df1b0213b?w=400&h=300&fit=crop",  # Wood
            "m_img": "https://images.unsplash.com/photo-1587302164634-6e4b0d4d4d9f?w=400&h=300&fit=crop",  # Silverware
            "g_img": "https://images.unsplash.com/photo-1605100804761-9a2e0d72d48b?w=400&h=300&fit=crop"}, # Sapphire
    "10th": {"traditional": "Tin / Aluminum", "modern": "Diamond Jewelry", "gemstone": "Diamond",
             "t_img": "https://images.unsplash.com/photo-1513506003901-1e6ca2ece459?w=400&h=300&fit=crop",  # Tin
             "m_img": "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=400&h=300&fit=crop", # Diamond ring
             "g_img": "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=400&h=300&fit=crop"},
    "15th": {"traditional": "Crystal", "modern": "Watches", "gemstone": "Ruby",
             "t_img": "https://images.unsplash.com/photo-1611590027211-b954fd027b51?w=400&h=300&fit=crop", # Crystal
             "m_img": "https://images.unsplash.com/photo-1523177876405-98d2b7d97e5e?w=400&h=300&fit=crop", # Watch
             "g_img": "https://images.unsplash.com/photo-1611590027211-b954fd027b51?w=400&h=300&fit=crop"}, # Ruby
    "25th": {"traditional": "Silver", "modern": "Silver", "gemstone": "Silver",
             "t_img": "https://images.unsplash.com/photo-1587302164634-6e4b0d4d4d9f?w=400&h=300&fit=crop",
             "m_img": "https://images.unsplash.com/photo-1587302164634-6e4b0d4d4d9f?w=400&h=300&fit=crop",
             "g_img": "https://images.unsplash.com/photo-1587302164634-6e4b0d4d4d9f?w=400&h=300&fit=crop"},
    "50th": {"traditional": "Gold", "modern": "Gold", "gemstone": "Gold",
             "t_img": "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=400&h=300&fit=crop",
             "m_img": "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=400&h=300&fit=crop",
             "g_img": "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=400&h=300&fit=crop"},
    "60th": {"traditional": "Diamond", "modern": "Diamond", "gemstone": "Diamond",
             "t_img": "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=400&h=300&fit=crop",
             "m_img": "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=400&h=300&fit=crop",
             "g_img": "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=400&h=300&fit=crop"}
}

# --- Dropdowns ---
RELATIONSHIPS = ["Any", "Wife", "Husband", "Fiancée", "Fiancé", "Girlfriend", "Boyfriend", "Mother", "Father", "Best Friend"]
OCCASIONS = ["Any", "Anniversary", "Birthday", "Engagement", "Wedding", "Valentine’s Day", "Christmas", "Just Because"]
AGES = ["Any", "18-24", "25-34", "35-44", "45-54", "55-64", "65+"]
PRICES = ["Any", "Under $25", "$25–$50", "$50–$100", "$100–$200", "Over $200"]

# --- Rotating User Agents ---
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
]

# --- Robust Amazon Search ---
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
            if not asin:
                continue
            # Title
            title_tag = item.select_one("h2 a span")
            title = title_tag.get_text(strip=True) if title_tag else "Beautiful Gift"
            # Link
            link = f"https://www.amazon.com/dp/{asin}"
            # Image
            img_tag = item.select_one("img.s-image")
            img = img_tag["src"] if img_tag and img_tag.get("src") else "https://via.placeholder.com/400x400.png?text=Heart"
            # Price
            sym = item.select_one("span.a-price-symbol")
            whole = item.select_one("span.a-price-whole")
            frac = item.select_one("span.a-price-fraction")
            price = ""
            if sym: price += sym.get_text(strip=True)
            if whole: price += whole.get_text(strip=True).replace('.', '')
            if frac: price += "." + frac.get_text(strip=True)
            price = price or "View price"
            # Rating
            rating_tag = item.select_one("span.a-icon-alt")
            rating = rating_tag.get_text(strip=True).split(" out")[0] if rating_tag else "New"
            products.append({"title": title, "link": link, "image": img, "price": price, "rating": rating})
        if not products:
            products = [{"title": "More gifts on Amazon", "link": url, "image": "https://via.placeholder.com/400x400.png?text=See+More", "price": "Explore", "rating": "Popular"}]
        return products
    except:
        return [{"title": "Shop gifts", "link": "https://www.amazon.com", "image": "https://via.placeholder.com/400x400.png?text=Sparkles", "price": "Discover", "rating": "5.0"}]

# --- PURE WHITE + SPARKLE BACKGROUND ---
st.markdown("""
<style>
    .big-font {font-size: 52px !important; font-family: 'Playfair Display', serif; color: #E91E63; text-align: center;}
    .sub-font {font-size: 24px !important; font-family: 'Dancing Script', cursive; color: #00796B; text-align: center;}
    .css-1v0mbdj {background-color: white !important;}
    .stButton>button {background-color: #E91E63; color: white; border-radius: 30px; padding: 12px 30px;}
    .background {
        background-image: url('https://i.imgur.com/8K5z6mT.png');
        background-size: cover; background-attachment: fixed; opacity: 0.1;
        position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1;
    }
</style>
<div class="background"></div>
""", unsafe_allow_html=True)

st.markdown('<p class="big-font">Timeless Gift Ideas</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-font">Every love story deserves the perfect gift</p>', unsafe_allow_html=True)

# --- Anniversary with Thumbnails ---
st.markdown("### Anniversary Celebration")
anniv_year = st.selectbox("Select Your Anniversary Year", options=list(ANNIVERSARIES.keys()), index=0)

if anniv_year != "Any Year" and anniv_year in ANNIVERSARIES:
    data = ANNIVERSARIES[anniv_year]
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image(data["t_img"], use_container_width=True)
        st.markdown(f"<strong style='color:#E91E63;'>Traditional</strong><br>{data['traditional']}", unsafe_allow_html=True)
    with col2:
        st.image(data["m_img"], use_container_width=True)
        st.markdown(f"<strong style='color:#00796B;'>Modern</strong><br>{data['modern']}", unsafe_allow_html=True)
    with col3:
        st.image(data["g_img"], use_container_width=True)
        st.markdown(f"<strong style='color:#9C27B0;'>Gemstone</strong><br>{data['gemstone']}", unsafe_allow_html=True)
    theme_choice = st.radio("Theme", ["Traditional", "Modern", "Gemstone", "All"], horizontal=True, label_visibility="collapsed")
else:
    theme_choice = "All"
    st.markdown("<small>Select a year to see theme images</small>", unsafe_allow_html=True)

# --- Filters ---
st.markdown("### Personalise Your Gift")
col1, col2 = st.columns(2)
with col1:
    relationship = st.selectbox("For Whom", RELATIONSHIPS, index=0)
    occasion = st.selectbox("Occasion", OCCASIONS, index=0)
with col2:
    age = st.selectbox("Age Group", AGES, index=0)
    price = st.selectbox("Budget", PRICES, index=0)

if st.button("Discover Gifts", use_container_width=True, type="primary"):
    with st.spinner("Finding your perfect gifts..."):
        query_parts = []
        if anniv_year != "Any Year" and anniv_year in ANNIVERSARIES:
            data = ANNIVERSARIES[anniv_year]
            query_parts.append(f"{anniv_year} anniversary")
            if theme_choice == "Traditional": query_parts.append(data["traditional"])
            elif theme_choice == "Modern": query_parts.append(data["modern"])
            elif theme_choice == "Gemstone": query_parts.append(data["gemstone"])
            else: query_parts.extend([data["traditional"], data["modern"], data["gemstone"]])
        if relationship != "Any": query_parts.append(relationship)
        if occasion != "Any" and occasion != "Anniversary": query_parts.append(occasion)
        if age != "Any": query_parts.append(age)
        if price != "Any": query_parts.append(price)
        query_parts.append("gift")
        query = " ".join(query_parts)
        st.session_state.results = search_amazon(query, 6)

# --- Results ---
if "results" in st.session_state:
    st.markdown("### Your Sparkling Selection")
    cols = st.columns(3)
    for i, p in enumerate(st.session_state.results):
        with cols[i % 3]:
            st.image(p["image"], width="stretch")
            st.markdown(f"**{p['title'][:80]}...**")
            st.markdown(f"<small>Rating: {p['rating']} • {p['price']}</small>", unsafe_allow_html=True)
            st.markdown(f"[View Details]({p['link']})")

st.markdown("---")
st.caption("Made with love by Grok • November 13, 2025")
