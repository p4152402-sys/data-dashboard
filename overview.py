import streamlit as st
import pandas as pd

st.title("📊 Overview Page")

file = st.file_uploader("Upload CSV", type=["csv"])

if file is not None:
    df = pd.read_csv(file)

    st.dataframe(df.head())

    st.metric("Rows", df.shape[0])
    st.metric("Columns", df.shape[1])