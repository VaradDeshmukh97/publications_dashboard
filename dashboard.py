# app.py
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Research Publications Dashboard", layout="wide")

@st.cache_data(ttl=3600)
def load_data():
    df = pd.read_excel("data/publications.xlsx")
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = load_data()

# Sidebar Filters
st.sidebar.title("📊 Filter Publications")
date_range = st.sidebar.date_input("Date Range", [df['Date'].min(), df['Date'].max()])
sectors = st.sidebar.multiselect("Sector", df['Sector'].unique(), default=df['Sector'].unique())
types = st.sidebar.multiselect("Type", df['Type'].unique(), default=df['Type'].unique())
picks = st.sidebar.multiselect("Pick(s)", df['Pick(s)'].dropna().unique(), default=df['Pick(s)'].dropna().unique())

# Filter Logic
filtered_df = df[
    (df['Date'] >= pd.to_datetime(date_range[0])) &
    (df['Date'] <= pd.to_datetime(date_range[1])) &
    (df['Sector'].isin(sectors)) &
    (df['Type'].isin(types)) &
    (df['Pick(s)'].isin(picks) | df['Pick(s)'].isna())
]

st.title("📚 Publications Dashboard")
st.markdown("Filter and explore research publications.")

# Show Data Table
st.dataframe(
    filtered_df[["Date", "Sector", "Type", "Pick(s)", "Topic", "URL"]],
    use_container_width=True,
    hide_index=True
)

# Download
st.download_button(
    label="📥 Download Filtered Data",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_publications.csv",
    mime="text/csv"
)
