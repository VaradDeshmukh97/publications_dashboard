# dashboard.py - REFINED UI VERSION
import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
from streamlit_option_menu import option_menu

# --------------------------------------------
# CONFIGURATION
# --------------------------------------------
st.set_page_config(page_title="📚 Intro-act Research Publications Dashboard", layout="centered")

sheet_url_main = "https://docs.google.com/spreadsheets/d/1WD5zUbyX74X0Z9xikWK7Xs7QfX-6IIFyjoUGmt53Fck/export?format=xlsx&id=1WD5zUbyX74X0Z9xikWK7Xs7QfX-6IIFyjoUGmt53Fck&gid=0"
sheet_url_comp = "https://docs.google.com/spreadsheets/d/1WD5zUbyX74X0Z9xikWK7Xs7QfX-6IIFyjoUGmt53Fck/export?format=xlsx&id=1WD5zUbyX74X0Z9xikWK7Xs7QfX-6IIFyjoUGmt53Fck&gid=536512581"

def format_date_safe(x):
    if isinstance(x, str) or x == "-" or pd.isna(x):
        return "-"
    else:
        return x.strftime("%b %d, %Y")

def load_data():
    df_main = pd.read_excel(sheet_url_main)
    df_comp = pd.read_excel(sheet_url_comp)

    for df in [df_main, df_comp]:
        df.fillna("-", inplace=True)
        df["Approval Date"] = df["Approval Date"].apply(format_date_safe)
        df["Publishing Date"] = df["Publishing Date"].apply(format_date_safe)
        if 'URL' in df.columns:
            df['Link'] = df['URL'].apply(lambda x: f'<a href="{x}" target="_blank" style= "text-decoration: none !important;">🔗</a>' if x != "-" else "")
        if 'Alpha Idea' in df.columns:
            df['Topic'] = df['Topic'].apply(lambda x: f"<b>{x}</b>" if x != "-" else x)
        if 'Title' in df.columns:
            df['Title'] = df['Title'].apply(lambda x: f"<b>{x}</b>" if x != "-" else x)

    return df_main, df_comp

df_main, df_comp = load_data()
last_refreshed = datetime.now().strftime("%B %d, %Y")

# --------------------------------------------
# STYLING
# --------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lexend:wght@300;400;500&display=swap');

html, body, [class*="css"]  {
    font-family: 'Lexend', sans-serif;
    font-size: 0.95rem !important;
    color: #1f1f1f;
}

section[data-testid="stSidebar"] {
    background-color: #f4f6fa;
    padding: 1rem;
    border-right: 1px solid #ccc;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
}

.report-container {
    overflow-x: auto;
    max-height: 500px;
    border: 1px solid #ddd;
    background: #ffffff;
    border-radius: 8px;
    width: 100%;
}

.report-container table {
    width: 100%;
    border-collapse: collapse;
    table-layout: auto;
    font-size: 0.75rem;
    font-family: Lexend;
    position: relative;
}

.report-container thead th {
    position: sticky;
    top: 0;
    background: #08198A !important;
    color: white;
    font-family: Lexend;
    font-size: 10px;
    z-index: 100;
    padding: 12px 8px !important;
    border-bottom: 1px solid #ccc;
    text-align: left;
}

.report-container tbody tr:nth-child(even) td {
    background-color: #f9f9f9;
}

.report-container tbody tr:hover td {
    background-color: #e6f0ff;
}

.report-container tbody td {
    padding: 8px;
    border-bottom: 1px solid #ddd;
    z-index: 1;
    word-wrap: break-word;
    text-align: left;
}

.report-container table, .report-container thead th, .report-container tbody td {
    font-size: 12px !important;
}

.subheader-container {
    background-color: #08198A;
    margin-top: 10px;                        
    padding: 10px 15px;
    text-align: center;
    color: white;
    font-family: 'Lexend', sans-serif;
    font-size: 12px;
    border-radius: 6px;
    margin-bottom: 1rem;
}

/* Sidebar layout fix: clean scroll behavior and styling */
section[data-testid="stSidebar"] {
    background-color: #f4f6fa !important;
    padding: 1.5rem 1rem;
    border-right: 1px solid #dcdcdc;
    font-family: Lexend !important;
    font-size: 10px !important;
    max-height: 100vh;
    overflow-y: auto;
    overflow-x: hidden;
    scrollbar-width: thin;
}

/* Sidebar titles and labels */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] label {
    font-family: 'Lexend', sans-serif !important;
    font-size: 10px !important;
    color: #08198A;
    font-weight: 600;
}

/* Subheader block inside sidebar */
.sidebar-subheader {
    background-color: #08198A;
    color: white;
    padding: 6px 10px;
    border-radius: 5px;
    font-size: 12px;
    font-family: 'Lexend', sans-serif;
    margin-top: 1rem;
    margin-bottom: 0.5rem;
    display: block;
}

/* Sidebar text inputs and multiselects */
section[data-testid="stSidebar"] input[type="text"],
section[data-testid="stSidebar"] .stTextInput > div > input,
section[data-testid="stSidebar"] .stSelectbox > div > div,
section[data-testid="stSidebar"] .stMultiSelect > div {
    font-family: 'Lexend', sans-serif;
    font-size: 10px;
    background-color: #fff8dc !important;
    border-radius: 4px;
    padding: 6px;
}

/* Sidebar column layout fix */
section[data-testid="stSidebar"] .block-container {
    display: block !important;
}

/* Sidebar multiselects and radio buttons */
section[data-testid="stSidebar"] label {
    font-family: 'Lexend', sans-serif;
    font-size: 11px;
    color: #333;
}

button, div.stButton > button, div[data-testid="stButton"] > button {
    font-family: 'Lexend', sans-serif !important;
    font-size: 12px !important;
    background-color: #E8E8E8;
    color: black;
    padding: 0.4rem 1rem;
    border: 1px solid #08198A !important;
    border-radius: 6px !important;
}

div[data-testid="column"] div.stButton > button,
div[data-testid="stExpander"] div.stButton > button {
    font-family: 'Lexend', sans-serif !important;
    font-size: 12px !important;
}
                                                           
/* Force Lexend font on all buttons */
div.stButton > button, button[kind] {
    background-color: #E8E8E8;
    color: black;
    padding: 0.4rem 1rem;
    font-size: 12px !important;
    font-family: 'Lexend', sans-serif !important;
    border-radius: 6px;
    border: none;
}

div.stButton > button:hover {
    background-color: #08198A;
    color: white;
    font-weight: bold;
    transition: 0.3s;
}

/* Specific button colors */
div[data-testid="column"] div.stButton:nth-child(1) button {
    background-color: green !important;
}
div[data-testid="column"] div.stButton:nth-child(2) button {
    background-color: red !important;
}
div[data-testid="column"] div.stButton:nth-child(3) button {
    background-color: orange !important;
}

/* Expander Header styling */
.streamlit-expanderHeader {
    font-family: Lexend;
    font-size: 10px;
    font-weight: 600;
    background-color: #f0f0f0 !important;
    padding: 6px 12px;
    border-radius: 5px;
}

/* Expander content background */
details[open] {
    background-color: #FEF2D4;
    padding: 10px;
    border-radius: 5px;
    margin-bottom: 10px;
}

div[data-testid="stExpander"] summary {
    font-family: Lexend !important;
    font-size: 10px !important;
    font-weight: 600 !important;
    background-color: #f0f0f0 !important;
    padding: 6px 12px;
    border-radius: 5px;
}

div[data-testid="column"] div.stButton button {
    font-size: 12px !important;
    font-family: Lexend !important;
}

section[data-testid="stSidebar"] .stRadio > div > label {
    font-family: 'Lexend', sans-serif !important;
    font-size: 10px !important;
    color: #08198A;
}
            
section[data-testid="stSidebar"] .stRadio > div > div[role="radiogroup"] > label[data-selected="true"] {
    background-color: #e0eaff;
    padding: 4px 8px;
    border-radius: 5px;
}
                                                            
@media (max-width: 768px) {
    .report-container table, .report-container thead, .report-container tbody, .report-container th, .report-container td, .report-container tr {
        display: block;
        width: 100%;
    }
    .report-container thead {
        display: none;
    }
    .report-container td {
        text-align: right;
        padding-left: 50%;
        position: relative;
    }
    .report-container td::before {
        content: attr(data-label);
        position: absolute;
        left: 10px;
        width: 45%;
        padding-right: 10px;
        white-space: nowrap;
        text-align: left;
        font-weight: bold;
    }
}
            
div.stAlert[data-testid="stAlert-success"] {
    background-color: #e6f4ea;
    color: #1b5e20;
    border-left: 6px solid #2e7d32;
    font-family: Lexend;
    font-size: 10px;
    padding: 10px;
    border-radius: 6px;
    margin-top: 10px;
} 

/* Style the radio label container */
section[data-testid="stSidebar"] .stRadio > div > div[role="radiogroup"] {
    display: flex;
    flex-direction: column;
    gap: 6px;
}

/* Make the radio labels look like toggle buttons */
section[data-testid="stSidebar"] .stRadio > div > div[role="radiogroup"] > label {
    background-color: #ffffff;
    border: 1px solid #ccc;
    padding: 8px 12px;
    border-radius: 6px;
    font-family: 'Lexend', sans-serif !important;
    font-size: 10px !important;
    color: #08198A;
    cursor: pointer;
    transition: 0.2s ease-in-out;
    display: block;
    margin-bottom: 6px;
    box-shadow: 1px 1px 2px rgba(0,0,0,0.05);
}
                        
/* Hover effect */
section[data-testid="stSidebar"] .stRadio > div > div[role="radiogroup"] > label:hover {
    background-color: #f0f4ff;
    border-color: #0f52ba;
}

* Highlight active selection */
section[data-testid="stSidebar"] .stRadio > div > div[role="radiogroup"] > label[data-selected="true"] {
    background-color: #B9B8B8 !important;
    color: #ffffff !important;
    border: 1.5px solid #171717 !important;
    font-weight: 1000;
}

/* Sidebar custom button tabs */
section[data-testid="stSidebar"] button[kind="secondary"] {
    width: 100%;
    background-color: #ffffff;
    border: 1px solid #08198A;
    color: #08198A;
    font-family: 'Lexend', sans-serif !important;
    font-size: 10px !important;
    border-radius: 6px;
    margin-bottom: 6px;
    transition: background-color 0.2s ease-in-out;
}

section[data-testid="stSidebar"] button[kind="secondary"]:hover {
    background-color: #E7E6E6;
    color: black;
    font-family: Lexend;
    font-weight: bold;
}

/* Active tab button styling */
section[data-testid="stSidebar"] button[kind="secondary"][data-testid*="stButton"]:has(span:contains("Progressive Industries")),
section[data-testid="stSidebar"] button[kind="secondary"][data-testid*="stButton"]:has(span:contains("Sell-Side Equity Research")),
section[data-testid="stSidebar"] button[kind="secondary"][data-testid*="stButton"]:has(span:contains("Pending Approvals")) {
    font-weight: bold;
}
            
</style>
""", unsafe_allow_html=True)

# --------------------------------------------
# HEADER
# --------------------------------------------
st.markdown(f"""
<div style='background-color: #E7E6E6; padding: 10px 10px; border-radius: 8px; color: black;'>
<div style='display: flex; justify-content: space-between; align-items: center;'>
<div style='flex: 1; text-align: center;'>
<img src='https://www.intro-act.com/images/assets/images/logo/introact-logo.svg' style='height: 40px;'>
</div>
<div style='flex: 2; text-align: center;'>
<h1 style='margin: 0; font-size: 25px; font-family: Lexend;'>Research Publications Dashboard</h1>
<p style='margin: 4px 0 0; font-family: Lexend; font-size: 12px;'>Research coverage on Intro-act's ten progressive industries and PartnerCap Securities' sell-side research partership mandates<br><small><i>Last updated: {last_refreshed}</small></i></p>
</div>
<div style='flex: 1; text-align: center;'>
<!-- Placeholder for second logo -->
<img src='https://partnercap.com/wp-content/uploads/2023/04/logo.png' id='right-logo' style='height: 40px;'>
</div>
</div>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------
# SIDEBAR DESIGN: Clean Lexend UI with Sections
# --------------------------------------------

# Sidebar title
st.sidebar.markdown("<div class='sidebar-subheader'>📂 Menu</div>", unsafe_allow_html=True)

if "selected_tab" not in st.session_state:
    st.session_state["selected_tab"] = "Progressive Industries"

# Navigation: radio buttons styled as tab switcher
# Define tabs
tabs = ["Progressive Industries", "Sell-Side Equity Research", "Pending Approvals"]
if "selected_tab" not in st.session_state:
    st.session_state.selected_tab = tabs[0]

# Display buttons
for tab in tabs:
    if st.sidebar.button(tab, key=tab):
        st.session_state.selected_tab = tab

selected_tab = st.session_state.selected_tab

# Search functionality
st.sidebar.markdown("<div class='sidebar-subheader'>🔍 Search Publications by Keyword</div>", unsafe_allow_html=True)

col_search, col_clear = st.sidebar.columns([3, 1])
with col_search:
    search_term = st.text_input("Keyword", label_visibility="collapsed")
with col_clear:
    if st.button("Clear"):
        search_term = ""
        '''st.session_state["sector_filter"] = []
        st.session_state["type_filter"] = []
        st.session_state["ticker_filter"] = []'''

# Dynamic filters based on selected tab
st.sidebar.markdown("<div class='sidebar-subheader'>🎛️ Filters</div>", unsafe_allow_html=True)

if selected_tab == "Progressive Industries":
    sectors = st.sidebar.multiselect("Filter by Sector", df_main['Sector'].unique(), key="sector_filter")
    types = st.sidebar.multiselect("Filter by Type", df_main['Type'].unique(), key="type_filter")

elif selected_tab == "Sell-Side Equity Research":
    tickers = st.sidebar.multiselect("Filter by Ticker", df_comp['Ticker'].unique(), key="ticker_filter")

# Data refresh
#st.sidebar.markdown("<div class='sidebar-subheader'>🔄 Data Controls</div>", unsafe_allow_html=True)
if st.sidebar.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()

st.sidebar.markdown("<hr style='margin: 1rem 0; border: none; border-top: 1px solid #ccc;'>", unsafe_allow_html=True)

# Manually adjust font-size
font_size = st.sidebar.select_slider(
    "Adjust Font Size", 
    options=["Small", "Medium", "Large"], 
    value="Medium"
)

font_size_map = {
    "Small": "0.8rem",
    "Medium": "0.95rem",
    "Large": "1.1rem"
}

# Dynamic font-size
st.markdown(f"""
<style>
/* Only apply dynamic font size to right container except for header */
section.main > div > :not(:first-child) {{
    font-size: {font_size_map[font_size]} !important;
    font-family: 'Lexend', sans-serif !important;
    color: #1f1f1f;
}}

/* Specifically target main report and expandable areas */
.report-container table,
.report-container td,
.report-container th,
.streamlit-expanderHeader,
div[data-testid="stExpander"] summary,
div[data-testid="stExpander"] p,
div[data-testid="stExpander"] li {{
    font-size: {font_size_map[font_size]} !important;
    font-family: 'Lexend', sans-serif !important;
}}
</style>
""", unsafe_allow_html=True)

# Disclaimer at the bottom
st.sidebar.markdown("""
    <hr style='margin-top: 2rem;'>
    <small style='font-family: Lexend; font-size: 4px; color: gray;'>
        ©️ <i>Copyright: 2025 Intro-act, LLC.</i>
    </small>
""", unsafe_allow_html=True)

# --------------------------------------------
# FILTER + SEARCH LOGIC
# --------------------------------------------
def filter_df(df, cols):
    if search_term:
        df = df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]
    return df[cols]

# --------------------------------------------
# DISPLAY SECTION
# --------------------------------------------
if selected_tab == "Progressive Industries":
    st.markdown("<div class='subheader-container'>Intro-act: Progressive Industry Research</div>", unsafe_allow_html=True)
    #sectors = st.sidebar.multiselect("Filter by Sector", df_main['Sector'].unique())
    #types = st.sidebar.multiselect("Filter by Type", df_main['Type'].unique())

    filtered = df_main.copy()
    if sectors:
        filtered = filtered[filtered['Sector'].isin(sectors)]
    if types:
        filtered = filtered[filtered['Type'].isin(types)]

    filtered = filter_df(filtered, ['Sector', 'Type', 'Approval Date', 'Publishing Date', 'Topic', 'Alpha Idea', 'Link'])

    st.markdown(f"<p style= 'font-family: Lexend;'>✅ Found {len(filtered)} publications...</p>", unsafe_allow_html=True)
    st.markdown("<div class='report-container'>" + filtered.to_html(index=False, escape=False) + "</div>", unsafe_allow_html=True)

elif selected_tab == "Sell-Side Equity Research":
    st.markdown("<div class='subheader-container'>PartnerCap Securities: Sell-Side Equity Research</div>", unsafe_allow_html=True)
    #tickers = st.sidebar.multiselect("Filter by Ticker", df_comp['Ticker'].unique())

    filtered = df_comp.copy()
    if tickers:
        filtered = filtered[filtered['Ticker'].isin(tickers)]

    filtered = filter_df(filtered, ['Ticker', 'Type', 'Approval Date', 'Publishing Date', 'Banner', 'Title', 'Link'])
    st.markdown(f"<p style= 'font-family: Lexend;'>✅ Found {len(filtered)} reports...</p>", unsafe_allow_html=True)
    st.markdown("<div class='report-container'>" + filtered.to_html(index=False, escape=False) + "</div>", unsafe_allow_html=True)

elif selected_tab == "Pending Approvals":
    def approval_view(df, label_cols):
        df_pending = df[df['Approval Date'] == "-"].reset_index(drop=True)
        if df_pending.empty:
            st.info("No pending pieces.")
            return

        for i, row in df_pending.iterrows():
            with st.expander(f"{row[label_cols[0]]} | {row[label_cols[1]]}"):
                if label_cols[0] == "Sector":
                    st.markdown(
                        f"""
                        <div style='font-family: Lexend; margin-bottom: 12px; margin-top: 12px;'>
                            <strong>{row[label_cols[2]]}</strong> <br>
                            Company Spotlights: <strong>{row[label_cols[3]]}</strong> <br>
                            Publication Date: <strong>{row[label_cols[4]]}</strong> 
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f"""
                        <div style='font-family: Lexend; margin-bottom: 12px; margin-top: 12px;'>
                            <strong>{row[label_cols[2]]}</strong> <br>
                            Banner: <strong>{row[label_cols[3]]}</strong> <br>
                            Publication Date: <strong>{row[label_cols[4]]}</strong>  
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                #st.markdown(f"<div style= 'font-family: Lexend;'><strong>Link:</strong> {row['Link']}", unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"✅ Approve for distribution", key=f"approve_{i}"):
                        st.success(f"Approved on {datetime.now().strftime('%b %d, %Y')}")
                with col2:
                    if st.button(f"❌ Suggest Edits/Pause for Distribution", key=f"pause_{i}"):
                        st.success(f"Edits suggested on {datetime.now().strftime('%b %d, %Y')} and distribution paused until further review.")

    st.markdown("<div class='subheader-container'>🕒 Pending Progressive Industry Research Publications</div>", unsafe_allow_html=True)
    approval_view(df_main, ['Sector', 'Type', 'Topic', 'Alpha Idea', 'Publishing Date'])
    st.markdown("<div class='subheader-container'>🕒 Pending Equity Research Publications</div>", unsafe_allow_html=True)
    approval_view(df_comp, ['Ticker', 'Type', 'Title', 'Banner', 'Publishing Date'])