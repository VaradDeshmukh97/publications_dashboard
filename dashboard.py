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
    st.image("https://www.intro-act.com/wp-content/uploads/2021/06/logo.png", width=80)
with col_title:
    st.title("Intro-act Progressive Industry Research Publications Dashboard")
    st.markdown("#### Access Intro-act's cutting edge and proprietary research publications across 10 progressive industries.")

# ------------------ LOAD DATA ------------------
@st.cache_data(ttl=1800)
def load_data():
    sheet_url = "https://docs.google.com/spreadsheets/d/1WD5zUbyX74X0Z9xikWK7Xs7QfX-6IIFyjoUGmt53Fck/export?format=csv"
    df = pd.read_csv(sheet_url)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.to_period('M').astype(str)
    df['Link'] = df['URL'].apply(lambda x: f"[Read here.]({x})" if pd.notna(x) else "")
    return df

df = load_data()

# ------------------ SIDEBAR FILTERS ------------------
st.sidebar.header("🔍 Filter")
sectors = st.sidebar.multiselect("Select Sector(s)", df['Sector'].dropna().unique())
types = st.sidebar.multiselect("Select Type(s)", df['Type'].dropna().unique())

# ------------------ FILTERING ------------------
filtered_df = df.copy()
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