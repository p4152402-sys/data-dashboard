import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Universal Data Dashboard", layout="wide")

st.title("📊 Universal Data Analysis Dashboard")
st.write("Upload ANY CSV file and explore your data")

file = st.file_uploader("Upload CSV file", type=["csv"])

if file is not None:
    df = pd.read_csv(file)

    # ---------------- SIDEBAR FILTERS ----------------
    st.sidebar.header("🔍 Filters")

    column = st.sidebar.selectbox("Choose column to filter", df.columns)

    if pd.api.types.is_numeric_dtype(df[column]):
        min_val = float(df[column].min())
        max_val = float(df[column].max())

        value_range = st.sidebar.slider(
            "Select range",
            min_val,
            max_val,
            (min_val, max_val)
        )

        df = df[(df[column] >= value_range[0]) & (df[column] <= value_range[1])]

    # ---------------- DATA PREVIEW ----------------
    st.subheader("👀 Data Preview")
    st.dataframe(df.head())

    # ---------------- BASIC INFO ----------------
    st.subheader("📌 Dataset Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Rows", df.shape[0])

    with col2:
        st.metric("Columns", df.shape[1])

    with col3:
        st.metric("Missing Values", df.isnull().sum().sum())

    st.write("### Column Names")
    st.write(list(df.columns))

    # ---------------- SUMMARY ----------------
    st.subheader("📊 Statistical Summary")
    st.dataframe(df.describe())

    # ---------------- COLUMN ANALYSIS ----------------
    st.subheader("📈 Column Analysis")

    all_columns = df.columns
    selected_column = st.selectbox("Select a column", all_columns)

    if pd.api.types.is_numeric_dtype(df[selected_column]):
        st.write("📊 Numeric Column Analysis")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Mean", round(df[selected_column].mean(), 2))

        with col2:
            st.metric("Max", df[selected_column].max())

        with col3:
            st.metric("Min", df[selected_column].min())

        st.bar_chart(df[selected_column])

    else:
        st.write("📊 Categorical Column Analysis")

        st.write("Unique Values:", df[selected_column].nunique())
        st.dataframe(df[selected_column].value_counts().head(10))

        st.bar_chart(df[selected_column].value_counts())

    # ---------------- CORRELATION HEATMAP ----------------
    st.subheader("🔥 Correlation Heatmap")

    numeric_df = df.select_dtypes(include="number")

    if numeric_df.shape[1] > 1:
        fig, ax = plt.subplots()
        sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)
    else:
        st.write("Not enough numeric columns for correlation")

        
    st.subheader("⬇ Export Data")

    csv = df.to_csv(index=False).encode('utf-8')

    st.download_button(
        "Download Filtered Data",
        csv,
        "filtered_data.csv",
        "text/csv"
    )