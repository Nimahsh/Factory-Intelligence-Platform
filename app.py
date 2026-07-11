import pandas as pd
import streamlit as st

st.write("Loading Excel...")

df = pd.read_excel("FirstSeason2026.xlsx")

st.success("Excel Loaded")

st.write(df.head())