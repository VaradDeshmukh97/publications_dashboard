# dashboard.py
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import plotly.express as px

# --------------------------------------------
# CONFIGURATION
# --------------------------------------------
st.set_page_config(page_title="📚 Intro-act Research Publications Dashboard", layout="wide")

sheet_url_main = "https://docs.google.com/spreadsheets/d/1WD5zUbyX74X0Z9xikWK7Xs7QfX-6IIFyjoUGmt53Fck/export?format=xlsx&id=1WD5zUbyX74X0Z9xikWK7Xs7QfX-6IIFyjoUGmt53Fck&gid=0"
sheet_url_comp = "https://docs.google.com/spreadsheets/d/1WD5zUbyX74X0Z9xikWK7Xs7QfX-6IIFyjoUGmt53Fck/export?format=xlsx&id=1WD5zUbyX74X0Z9xikWK7Xs7QfX-6IIFyjoUGmt53Fck&gid=536512581"

def load_data():
    df_main = pd.read_excel(sheet_url_main)
    df_comp = pd.read_excel(sheet_url_comp)
    for df in [df_main, df_comp]:
        df.fillna("-", inplace=True)
        df["Approval Date"] = df["Approval Date"].apply(lambda x: x.strftime("%B %d, %Y"))
        df["Publishing Date"] = df["Publishing Date"].apply(lambda x: x.strftime("%B %d, %Y"))
        if 'URL' in df.columns:
            df['Link'] = df['URL'].apply(lambda x: f"[Read here.]({x})" if x != "-" else "")
   
    return df_main, df_comp

# Load Data
df_main, df_comp = load_data()

# --------------------------------------------
# STYLING
# --------------------------------------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif;
        font-size: 14px;
    }
    .block-container {
        padding-top: 2rem;
    }
    .logo {
        display: flex;
        align-items: center;
        padding-bottom: 1rem;
    }
    .logo img {
        height: 50px;
        margin-right: 10px;
        padding-top: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Logo and Header
from datetime import datetime

# Last Refreshed Date
last_refreshed = datetime.now().strftime("%B %d, %Y")

# Header styling
st.markdown("""
    <style>
        .header-container {
            display: flex;
            flex-direction: row;
            width: 100%;
            margin-bottom: 20px;
        }

        .logo-column {
            width: 20%;
            background-color: #f0f0f0;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .logo-column svg {
            width: 120px;
            height: auto;
        }

        .title-column {
            width: 80%;
            background-color: #0f74ba;
            color: white;
            padding: 20px 30px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        .title-column h1 {
            font-family: 'Poppins', sans-serif;
            font-size: 2.2rem;
            margin: 0;
        }

        .title-column p {
            font-family: 'Poppins', sans-serif;
            font-size: 1rem;
            margin: 5px 0 0;
            opacity: 0.85;
        }
    </style>
""", unsafe_allow_html=True)

# Render the custom header with logo and content
st.markdown(f"""
<div class="header-container">
    <div class="logo-column">
        <img class="logo" src="https://www.intro-act.com/images/assets/images/logo/introact-logo.svg" alt="Intro-act Logo">
    </div>
    <div class="title-column">
        <h1>Intro-act Research Publications Dashboard</h1>
        <p>Explore Intro-act's cutting edge research across 10 progressive industries and curated sell-side equity research report in partnership with PartnerCap Securities. Last updated: {last_refreshed}</p>
    </div>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------
# TABS
# --------------------------------------------
tab = option_menu(
    menu_title=None,
    options=["Progressive Industries", "Sell-Side Equity Research"],
    icons=["bar-chart", "building"],
    orientation="horizontal"
)

# --------------------------------------------
# TAB 1: ProgInd
# --------------------------------------------
if tab == "Progressive Industries":

    sectors = st.sidebar.multiselect("Sector", df_main['Sector'].unique())
    types = st.sidebar.multiselect("Type", df_main['Type'].unique())

    filtered_df = df_main.copy()
    if sectors:
        filtered_df = filtered_df[filtered_df['Sector'].isin(sectors)]
    if types:
        filtered_df = filtered_df[filtered_df['Type'].isin(types)]
    
    if st.sidebar.button("🔄 Refresh Data"):
        st.cache_data.clear()

    st.subheader(f"✅ Found {len(filtered_df)} matching publications...")
    st.write(filtered_df[['Sector', 'Type', 'Approval Date', 'Publishing Date', 'Topic', 'Alpha Idea', 'Link']].to_markdown(index=False), unsafe_allow_html=True)

# --------------------------------------------
# TAB 2: comp
# --------------------------------------------
if tab == "Sell-Side Equity Research":

    companies = st.sidebar.multiselect("Ticker", df_comp['Ticker'].unique())
    filtered_df = df_comp.copy()
    if companies:
        filtered_df = filtered_df[filtered_df['Ticker'].isin(companies)]

    if st.sidebar.button("🔄 Refresh Data"):
        st.cache_data.clear()

    st.subheader(f"✅ Found {len(filtered_df)} matching publications...")
    st.write(filtered_df[['Ticker', 'Type', 'Approval Date', 'Publishing Date', 'Banner', 'Title', 'Link']].to_markdown(index=False), unsafe_allow_html=True)