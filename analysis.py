import streamlit as st
import pandas as pd

st.title("🔍 Analysis Page")

file = st.file_uploader("Upload CSV", type=["csv"])

if file is not None:
    df = pd.read_csv(file)

    st.write(df.describe())