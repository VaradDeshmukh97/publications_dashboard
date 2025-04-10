# app.py
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Research Publications Dashboard", layout="wide")

@st.cache_data(ttl=1800)  # Refresh every 30 minutes
def load_data():
    sheet_url = "https://docs.google.com/spreadsheets/d/1WD5zUbyX74X0Z9xikWK7Xs7QfX-6IIFyjoUGmt53Fck/export?format=csv"
    df = pd.read_csv(sheet_url)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = load_data()

# Sidebar Filters
st.sidebar.title("📊 Filter Publications")
#date_range = st.sidebar.date_input("Date Range", [df['Date'].min(), df['Date'].max()])
sectors = st.sidebar.multiselect("Sector", df['Sector'].unique())
types = st.sidebar.multiselect("Type", df['Type'].unique())

df['Link'] = df['URL'].apply(lambda x: f"[Read here.]({x})" if pd.notna(x) else "")

# Filter Logic
filtered_df = df[
#    (df['Date'] >= pd.to_datetime(date_range[0])) &
#    (df['Date'] <= pd.to_datetime(date_range[1])) &
    (df['Sector'].isin(sectors)) &
    (df['Type'].isin(types))
]

st.title("📚 Intro-act Research Publications Dashboard")
st.markdown("Filter and explore research publications spanning Intro-act's 10 Progressive Industries.")

# Show Data Table
#st.dataframe(
#    filtered_df[["Date", "Sector", "Type", "Alpha Idea", "Topic", "URL"]],
#    use_container_width=True,
#    hide_index=True
#)

st.write(df[['Sector', 'Type', 'Date', 'Topic', 'Alpha Idea', 'Link']].to_markdown(index=False), unsafe_allow_html=True)

#
# Download
#st.download_button(
#    label="📥 Download Filtered Data",
#    data=filtered_df.to_csv(index=False),
#    file_name="filtered_publications.csv",
#    mime="text/csv"
#)