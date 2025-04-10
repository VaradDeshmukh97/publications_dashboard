import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------ CONFIG ------------------
st.set_page_config(
    page_title="Intro-act Progressive Industry Research Publications Dashboard",
    layout="wide",
    page_icon="📚"
)

# ------------------ CUSTOM CSS ------------------
def apply_branding():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

            html, body, [class*="css"] {
                font-family: 'Poppins', sans-serif;
                background-color: #f5f9ff;
            }

            .block-container {
                padding-top: 2rem;
                padding-left: 2rem;
                padding-right: 2rem;
            }

            .metric-container {
                background-color: white;
                padding: 1rem;
                border-radius: 12px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.05);
                text-align: center;
            }

            .stDownloadButton > button, .stButton > button {
                background-color: #174EA6;
                color: white;
                font-weight: 600;
                padding: 0.6em 1.2em;
                border-radius: 8px;
                border: none;
            }

            h1, h2, h3 {
                color: #174EA6;
                font-weight: 600;
            }

            a {
                color: #1a73e8 !important;
                text-decoration: none;
                font-weight: 500;
            }

            @media only screen and (max-width: 768px) {
                .block-container {
                    padding-left: 1rem;
                    padding-right: 1rem;
                }
                .metric-container {
                    margin-bottom: 1rem;
                }
            }
        </style>
    """, unsafe_allow_html=True)

apply_branding()

# ------------------ LOGO + HEADER ------------------
col_logo, col_title = st.columns([0.15, 0.85])
with col_logo:
    st.markdown(
        """
        <div style='padding-top: 10px; padding-bottom: 10px;'>
            <img src="data/intro-act_logo.png" width='200' style='margin-top: 5px;' />
        </div>
        """,
        unsafe_allow_html=True
    )
with col_title:
    st.title("Progressive Industry Research Publications Dashboard")
    st.markdown("#### Access Intro-act's cutting edge and proprietary research publications across 10 progressive industries.")

# ------------------ LOAD DATA ------------------
@st.cache_data(ttl=1800)
def load_data():
    # First sheet: ProgInd
    sheet_url_progind = "https://docs.google.com/spreadsheets/d/1WD5zUbyX74X0Z9xikWK7Xs7QfX-6IIFyjoUGmt53Fck/export?format=csv"
    df_main = pd.read_csv(sheet_url_progind)
    df_main['Date'] = pd.to_datetime(df_main['Date'], format="MMM DD, YYYY", errors='coerce')
    df_main['Link'] = df_main['URL'].apply(lambda x: f"[Read here.]({x})" if pd.notna(x) else "")
    df_main.fillna("-", inplace=True)

    # Second sheet: comp (company-specific)
    sheet_url_comp = "https://docs.google.com/spreadsheets/d/1WD5zUbyX74X0Z9xikWK7Xs7QfX-6IIFyjoUGmt53Fck/export?format=csv&gid=536512581"
    df_comp = pd.read_csv(sheet_url_comp)
    df_comp['Date'] = pd.to_datetime(df_comp['Date'], format="MMM DD, YYYY", errors='coerce')
    df_comp['Link'] = df_comp['URL'].apply(lambda x: f"[Read here.]({x})" if pd.notna(x) else "")
    df_comp.fillna("-", inplace=True)

    return df_main, df_comp

df_main, df_comp = load_data()
tab1, tab2 = st.tabs(["📚 Progressive Industry Research", "🏢 Sell-side Equity Research"])

# ------------------ SIDEBAR FILTERS ------------------
with tab1:
    st.header("🏢 Intro-act's Progressive Industry Research")

    st.sidebar.header("🔍 Filter")
    sectors = st.sidebar.multiselect("Select Sector(s)", df_main['Sector'].dropna().unique())
    types = st.sidebar.multiselect("Select Type(s)", df_main['Type'].dropna().unique())

    if st.sidebar.button("🔄 Refresh Data"):
        st.cache_data.clear()
        
    # ------------------ FILTERING ------------------
    filtered_df = df_main.copy()
    if sectors:
        filtered_df = filtered_df[filtered_df['Sector'].isin(sectors)]
    if types:
        filtered_df = filtered_df[filtered_df['Type'].isin(types)]



    # ------------------ TABLE ------------------
    st.markdown(f"### 📋 Found {len(filtered_df)} matching publications...")
    st.write(
        filtered_df[['Sector', 'Type', 'Date', 'Topic', 'Alpha Idea', 'Link']].to_markdown(index=False),
        unsafe_allow_html=True
    )

with tab2:
    st.header("🏢 Sell-Side Equity Research (Intro-act <> PartnerCap Securities)")

    companies = st.multiselect("Select Ticker", df_comp['Ticker'].unique())
    types_c = st.multiselect("Select Type", df_comp['Type'].unique())

    # Filtering
    filtered_comp_df = df_comp[
        (df_comp['Company'].isin(companies)) &
        (df_comp['Type'].isin(types_c))
    ]

    # Format link
    filtered_comp_df['Link'] = filtered_comp_df['URL'].apply(lambda x: f"[Read here.]({x})" if pd.notna(x) and x != "-" else "-")

    # Display table
    st.write(filtered_comp_df[['Ticker', 'Type', 'Date', 'Banner', 'Curator', 'Title', 'Link']].to_markdown(index=False), unsafe_allow_html=True)