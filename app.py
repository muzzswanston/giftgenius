# app.py - Wedding Anniversary Gift Suggester with Streamlit GUI
# Run with: streamlit run app.py

import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse

# --- Anniversary Themes (Traditional + Modern) ---
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

# --- Amazon Search Function ---
def search_amazon(query, tag, num_results=5):
    """Scrape Amazon search results and return title + affiliate link."""
    if not query:
        return []
    url = f"https://www.amazon.com/s?k={urllib.parse.quote(query)}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.find_all("div", {"data-component-type": "s-search-result"})[:num_results]
        products = []
        for item in results:
            asin = item.get("data-asin")
            if not asin:
                continue
            title_tag = item.find("h2")
            title = title_tag.get_text(strip=True) if title_tag else "No title"
            link = f"https://www.amazon.com/dp/{asin}/?tag={tag}"
            products.append({"title": title, "link": link})
        return products or [{"title": "No results found. Try another search.", "link": "#"}]
    except Exception as e:
        return [{"title": f"Error: {str(e)}", "link": "#"}]

# --- Streamlit App ---
st.set_page_config(page_title="Anniversary Gift Finder", page_icon="💍", layout="centered")

st.title("💍 Wedding Anniversary Gift Suggester")
st.markdown("### Get perfect gift ideas + earn Amazon commissions instantly!")

# Sidebar inputs
with st.sidebar:
    st.header("Your Settings")
    affiliate_tag = st.text_input("Amazon Associates Tag", value="ssbudge604-22", help="e.g., yourname-20")
    year = st.number_input("Anniversary Year", min_value=1, max_value=70, value=5, step=1)

# Main content
if year in ANNIVERSARIES:
    trad = ANNIVERSARIES[year]["traditional"]
    mod = ANNIVERSARIES[year]["modern"]
    st.success(f"**{year}th Anniversary**")
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**Traditional:** {trad}")
    with col2:
        st.info(f"**Modern:** {mod}")
else:
    st.warning(f"No standard theme for year {year}. Using general anniversary searches.")
    trad = mod = "Anniversary Gift"

# Search queries
query_trad = f"{year}th wedding anniversary {trad} gift"
query_mod = f"{year}th wedding anniversary {mod} gift"

# Search buttons
col1, col2 = st.columns(2)
with col1:
    if st.button(f"Find Traditional Gifts ({trad})", use_container_width=True):
        with st.spinner("Searching Amazon..."):
            trad_products = search_amazon(query_trad, affiliate_tag)
        st.session_state.trad_results = trad_products

with col2:
    if st.button(f"Find Modern Gifts ({mod})", use_container_width=True):
        with st.spinner("Searching Amazon..."):
            mod_products = search_amazon(query_mod, affiliate_tag)
        st.session_state.mod_results = mod_products

# Display results if available
if "trad_results" in st.session_state:
    st.subheader(f"Traditional Gifts – {trad}")
    for i, prod in enumerate(st.session_state.trad_results, 1):
        st.markdown(f"**{i}.** [{prod['title']}]({prod['link']})")

if "mod_results" in st.session_state:
    st.subheader(f"Modern Gifts – {mod}")
    for i, prod in enumerate(st.session_state.mod_results, 1):
        st.markdown(f"**{i}.** [{prod['title']}]({prod['link']})")

# Footer
st.markdown("---")
st.caption("Made with ❤️ by Grok • All links contain your affiliate tag • Live Amazon data as of November 12, 2025")

# Optional: Auto-search on load (uncomment if you want)
// if st.session_state.get("first_run", True):
//     st.session_state.first_run = False
//     st.rerun()