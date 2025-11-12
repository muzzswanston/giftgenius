# app.py - Gimme Gift Ideas + Anniversary Themes (Pro Version)
import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse

st.set_page_config(page_title="Gimme Gift Ideas", page_icon="Gift", layout="centered")

# --- Anniversary Themes ---
ANNIVERSARIES = {
    "Any Year": {"traditional": "", "modern": ""},
    "1st": {"traditional": "Paper", "modern": "Clocks"},
    "2nd": {"traditional": "Cotton", "modern": "China"},
    "3rd": {"traditional": "Leather", "modern": "Crystal/Glass"},
    "4th": {"traditional": "Fruit/Flowers", "modern": "Appliances"},
    "5th": {"traditional": "Wood", "modern": "Silverware"},
    "6th": {"traditional": "Iron", "modern": "Wood"},
    "7th": {"traditional": "Copper/Wool", "modern": "Desk Sets"},
    "8th": {"traditional": "Bronze/Pottery", "modern": "Linen/Lace"},
    "9th": {"traditional": "Willow/Pottery", "modern": "Leather"},
    "10th": {"traditional": "Aluminum/Tin", "modern": "Diamond Jewelry"},
    "15th": {"traditional": "Crystal", "modern": "Watches"},
    "20th": {"traditional": "China", "modern": "Platinum"},
    "25th": {"traditional": "Silver", "modern": "Silver"},
    "30th": {"traditional": "Pearl", "modern": "Diamond"},
    "40th": {"traditional": "Ruby", "modern": "Ruby"},
    "50th": {"traditional": "Gold", "modern": "Gold"},
    "60th": {"traditional": "Diamond", "modern": "Diamond"},
}

# --- Dropdown Options ---
RELATIONSHIPS = ["Any", "Girlfriend", "Boyfriend", "Wife", "Husband", "Mom", "Dad", "Friend", "Sister", "Brother"]
RECIPIENTS = ["Any", "Her", "Him", "Girl", "Boy", "Couple"]
OCCASIONS = ["Any", "Birthday", "Anniversary", "Christmas", "Valentine's Day", "Wedding", "Just Because"]
AGES = ["Any", "Under 18", "18-24", "25-34", "35-44", "45-54", "55+"]
PRICES = ["Any", "Under $25", "$25-$50", "$50-$100", "$100-$200", "Over $200"]

# --- Amazon Search ---
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
            title = title_tag.get_text(strip=True) if title_tag else "Gift Idea"
            link = f"https://www.amazon.com/dp/{asin}"
            img_tag = item.select_one("img.s-image")
            img = img_tag["src"] if img_tag and img_tag.get("src") else "https://via.placeholder.com/300x300.png?text=Gift"
            price = ""
            sym = item.select_one("span.a-price-symbol")
            whole = item.select_one("span.a-price-whole")
            frac = item.select_one("span.a-price-fraction")
            if sym: price += sym.get_text(strip=True)
            if whole: price += whole.get_text(strip=True)
            if frac: price += frac.get_text(strip=True)
            price = price or "View price"
            rating_tag = item.select_one("span.a-icon-alt")
            rating = rating_tag.get_text(strip=True).split(" out")[0] if rating_tag else "N/A"
            products.append({"title": title, "link": link, "image": img, "price": price, "rating": rating})
        return products or [{"title": "More gifts", "link": url, "image": "https://via.placeholder.com/300x300.png?text=See+More", "price": "View all", "rating": "N/A"}]
    except:
        return [{"title": "Explore on Amazon", "link": "https://www.amazon.com", "image": "https://via.placeholder.com/300x300.png?text=Gift", "price": "Open", "rating": "N/A"}]

# --- UI ---
st.title("Gift Gimme Gift Ideas")
st.markdown("### _The perfect gift is just one click away._")

# Anniversary Special Section
st.markdown("### Anniversary Gift? Select Year & Theme")
anniv_year = st.selectbox("Anniversary Year", options=list(ANNIVERSARIES.keys()), index=0)

if anniv_year != "Any Year":
    trad = ANNIVERSARIES[anniv_year]["traditional"]
    mod = ANNIVERSARIES[anniv_year]["modern"]
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**Traditional:** {trad}")
    with col2:
        st.info(f"**Modern:** {mod}")
    theme_choice = st.radio("Gift Theme", ["Traditional", "Modern", "Both"], horizontal=True)
else:
    trad = mod = ""
    theme_choice = "Both"

st.markdown("### Or Use Advanced Filters")
col1, col2 = st.columns(2)
with col1:
    relationship = st.selectbox("Relationship", RELATIONSHIPS, index=0)
    recipient = st.selectbox("Recipient", RECIPIENTS, index=0)
with col2:
    occasion = st.selectbox("Occasion", OCCASIONS, index=0)
    age = st.selectbox("Age", AGES, index=0)

price = st.selectbox("Price Range", PRICES, index=0)

if st.button("Find Perfect Gifts", use_container_width=True, type="primary"):
    with st.spinner("Finding the best gifts just for you..."):
        query_parts = []

        # Anniversary priority
        if anniv_year != "Any Year":
            query_parts.append(anniv_year)
            query_parts.append("anniversary")
            if theme_choice == "Traditional":
                query_parts.append(trad)
            elif theme_choice == "Modern":
                query_parts.append(mod)
            else:
                query_parts.extend([trad, mod])

        # Other filters
        if relationship != "Any": query_parts.append(relationship)
        if recipient != "Any": query_parts.append(recipient)
        if occasion != "Any" and occasion != "Anniversary": query_parts.append(occasion)
        if age != "Any": query_parts.append(age.replace("+", " and over"))
        if price != "Any": query_parts.append(price)

        query_parts.append("gift")
        query = " ".join(query_parts)
        st.session_state.results = search_amazon(query, 9)

# --- Results ---
if "results" in st.session_state:
    st.success(f"Here are **9 perfect gift ideas** just for you!")
    cols = st.columns(3)
    for i, p in enumerate(st.session_state.results):
        with cols[i % 3]:
            st.image(p["image"], width="stretch")
            st.markdown(f"**{p['title'][:70]}...**")
            st.caption(f"Rating: {p['rating']} • {p['price']}")
            st.markdown(f"[View on Amazon]({p['link']})")

    st.info("Tip: Change any filter and search again for fresh ideas!")

st.markdown("---")
st.caption("Made with love by Grok • Inspired by gimmegiftideas.com • Updated November 13, 2025")
