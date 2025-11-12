# app.py - Timeless Gift Ideas (US Amazon • Hitched.co.uk Style)
import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse

st.set_page_config(page_title="Timeless Gift Ideas", page_icon="Ring", layout="centered")

# --- Sophisticated Anniversary Themes (US Focus) ---
ANNIVERSARIES = {
    "Any Year": {"traditional": "", "modern": "", "gemstone": ""},
    "1st": {"traditional": "Paper", "modern": "Clocks", "gemstone": "Gold Jewelry"},
    "2nd": {"traditional": "Cotton", "modern": "China", "gemstone": "Garnet"},
    "3rd": {"traditional": "Leather", "modern": "Crystal", "gemstone": "Pearl"},
    "4th": {"traditional": "Linen / Fruit & Flowers", "modern": "Appliances", "gemstone": "Blue Topaz"},
    "5th": {"traditional": "Wood", "modern": "Silverware", "gemstone": "Sapphire"},
    "6th": {"traditional": "Iron", "modern": "Wood", "gemstone": "Amethyst"},
    "7th": {"traditional": "Wool / Copper", "modern": "Desk Sets", "gemstone": "Onyx"},
    "8th": {"traditional": "Bronze", "modern": "Linens & Lace", "gemstone": "Tourmaline"},
    "9th": {"traditional": "Pottery", "modern": "Leather", "gemstone": "Lapis Lazuli"},
    "10th": {"traditional": "Tin / Aluminum", "modern": "Diamond Jewelry", "gemstone": "Diamond"},
    "15th": {"traditional": "Crystal", "modern": "Watches", "gemstone": "Ruby"},
    "20th": {"traditional": "China", "modern": "Platinum", "gemstone": "Emerald"},
    "25th": {"traditional": "Silver", "modern": "Silver", "gemstone": "Silver"},
    "30th": {"traditional": "Pearl", "modern": "Diamond", "gemstone": "Pearl"},
    "40th": {"traditional": "Ruby", "modern": "Ruby", "gemstone": "Ruby"},
    "50th": {"traditional": "Gold", "modern": "Gold", "gemstone": "Gold"},
    "60th": {"traditional": "Diamond", "modern": "Diamond", "gemstone": "Diamond"},
}

# --- Refined Dropdowns ---
RELATIONSHIPS = ["Any", "Wife", "Husband", "Fiancée", "Fiancé", "Girlfriend", "Boyfriend", "Mother", "Father", "Best Friend"]
OCCASIONS = ["Any", "Anniversary", "Birthday", "Engagement", "Wedding", "Valentine’s Day", "Christmas", "Just Because"]
AGES = ["Any", "18-24", "25-34", "35-44", "45-54", "55-64", "65+"]
PRICES = ["Any", "Under $25", "$25–$50", "$50–$100", "$100–$200", "Over $200"]

# --- Amazon.com Search (US) ---
def search_amazon(query, num_results=6):
    url = f"https://www.amazon.com/s?k={urllib.parse.quote(query)}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(r.text, "html.parser")
        items = soup.select('div[data-component-type="s-search-result"]')[:num_results]
        products = []
        for item in items:
            asin = item.get("data-asin")
            if not asin: continue
            title_tag = item.select_one("h2 a")
            title = title_tag.get_text(strip=True) if title_tag else "Timeless Gift"
            link = f"https://www.amazon.com/dp/{asin}"
            img_tag = item.select_one("img.s-image")
            img = img_tag["src"] if img_tag and img_tag.get("src") else "https://via.placeholder.com/400x400.png?text=Heart"
            price = ""
            sym = item.select_one("span.a-price-symbol")
            whole = item.select_one("span.a-price-whole")
            frac = item.select_one("span.a-price-fraction")
            if sym: price += sym.get_text(strip=True)
            if whole: price += whole.get_text(strip=True)
            if frac: price += frac.get_text(strip=True)
            price = price or "View price"
            rating_tag = item.select_one("span.a-icon-alt")
            rating = rating_tag.get_text(strip=True).split(" out")[0] if rating_tag else "New"
            products.append({"title": title, "link": link, "image": img, "price": price, "rating": rating})
        return products or [{"title": "More beautiful gifts", "link": url, "image": "https://via.placeholder.com/400x400.png?text=See+More", "price": "Explore", "rating": ""}]
    except:
        return [{"title": "Shop on Amazon", "link": "https://www.amazon.com", "image": "https://via.placeholder.com/400x400.png?text=Heart", "price": "Discover", "rating": ""}]

# --- Elegant Styling ---
st.markdown("""
<style>
    .big-font {font-size: 48px !important; font-family: 'Playfair Display', serif; color: #5D4037; text-align: center;}
    .sub-font {font-size: 22px !important; font-family: 'Crimson Text', serif; color: #6D4C41; text-align: center;}
    .css-1v0mbdj {background-color: #FFF8F0;}
    small {color: #8D6E63;}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-font">Timeless Gift Ideas</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-font">Curated with love for every milestone and moment</p>', unsafe_allow_html=True)

st.markdown("### Anniversary Celebration")
anniv_year = st.selectbox("Select Your Anniversary Year", options=list(ANNIVERSARIES.keys()), index=0)

if anniv_year != "Any Year":
    trad = ANNIVERSARIES[anniv_year]["traditional"]
    mod = ANNIVERSARIES[anniv_year]["modern"]
    gem = ANNIVERSARIES[anniv_year]["gemstone"]
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<strong>Traditional</strong><br>{trad}", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<strong>Modern</strong><br>{mod}", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<strong>Gemstone</strong><br>{gem}", unsafe_allow_html=True)
    theme_choice = st.radio("Theme Preference", ["Traditional", "Modern", "Gemstone", "All"], horizontal=True, label_visibility="collapsed")
else:
    theme_choice = "All"

st.markdown("### Refine Your Search")
col1, col2 = st.columns(2)
with col1:
    relationship = st.selectbox("For Whom", RELATIONSHIPS, index=0)
    occasion = st.selectbox("Occasion", OCCASIONS, index=0)
with col2:
    age = st.selectbox("Age Group", AGES, index=0)
    price = st.selectbox("Budget", PRICES, index=0)

if st.button("Discover Gifts", use_container_width=True, type="primary"):
    with st.spinner("Curating exquisite gifts for you..."):
        query_parts = []
        if anniv_year != "Any Year":
            query_parts.append(f"{anniv_year} anniversary")
            if theme_choice == "Traditional":
                query_parts.append(trad)
            elif theme_choice == "Modern":
                query_parts.append(mod)
            elif theme_choice == "Gemstone":
                query_parts.append(gem)
            else:
                query_parts.extend([trad, mod, gem])
        if relationship != "Any": query_parts.append(relationship)
        if occasion != "Any" and occasion != "Anniversary": query_parts.append(occasion)
        if age != "Any": query_parts.append(age)
        if price != "Any": query_parts.append(price)
        query_parts.append("gift")
        query = " ".join(query_parts)
        st.session_state.results = search_amazon(query, 6)

# --- Elegant Results ---
if "results" in st.session_state:
    st.markdown("### Your Curated Selection")
    st.markdown("<em>Timeless treasures chosen just for you</em>", unsafe_allow_html=True)
    cols = st.columns(3)
    for i, p in enumerate(st.session_state.results):
        with cols[i % 3]:
            st.image(p["image"], width="stretch")
            st.markdown(f"**{p['title'][:80]}...**")
            st.markdown(f"<small>Rating: {p['rating']} • {p['price']}</small>", unsafe_allow_html=True)
            st.markdown(f"[View Details]({p['link']})")

    st.markdown("<br><small>Tip: Adjust any filter above for a fresh collection of ideas.</small>", unsafe_allow_html=True)

st.markdown("---")
st.caption("Crafted with elegance by Grok • Inspired by Hitched.co.uk • November 13, 2025")
