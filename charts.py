import streamlit as st
import pandas as pd

st.title("📈 Charts Page")

file = st.file_uploader("Upload CSV", type=["csv"])

if file is not None:
    df = pd.read_csv(file)

    numeric_df = df.select_dtypes(include="number")

    st.bar_chart(numeric_df)