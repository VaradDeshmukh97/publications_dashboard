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
sheet_url_comp = "https://docs.google.com/spreadsheets/d/1WD5zUbyX74X0Z9xikWK7Xs7QfX-6IIFyjoUGmt53Fck/export?format=xlsx&id=1WD5zUbyX74X0Z9xikWK7Xs7QfX-6IIFyjoUGmt53Fck&gid=1516348627"

def load_data():
    df_main = pd.read_excel(sheet_url_main)
    df_comp = pd.read_excel(sheet_url_comp)
    for df in [df_main, df_comp]:
        df.fillna("-", inplace=True)
        #if 'Date' in df.columns:
        #    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
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
st.markdown("""
<div class="logo">
    <img src="https://github.com/VaradDeshmukh97/publications_dashboard/blob/main/data/intro-act_logo.png" alt="Intro-act Logo">
    <h3>Intro-act Research Publications Dashboard</h3>
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

    st.subheader(f"✅ Found {len(filtered_df)} matching publications...")
    st.write(filtered_df[['Sector', 'Type', 'Date', 'Topic', 'Alpha Idea', 'Link']].to_markdown(index=False), unsafe_allow_html=True)

# --------------------------------------------
# TAB 2: comp
# --------------------------------------------
if tab == "Sell-Side Equity Research":
    companies = st.sidebar.multiselect("Ticker", df_comp['Ticker'].unique())
    filtered_df = df_comp.copy()
    if companies:
        filtered_df = filtered_df[filtered_df['Ticker'].isin(companies)]

    st.subheader(f"✅ Found {len(filtered_df)} matching publications...")
    st.write(filtered_df[['Ticker', 'Type', 'Date', 'Banner', 'Title', 'Link']].to_markdown(index=False), unsafe_allow_html=True)