import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Hackathon Starter",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 AI Hackathon Starter Kit")

st.write("Welcome! Your Streamlit application is running.")

st.sidebar.header("Navigation")

page = st.sidebar.selectbox(
    "Choose a page",
    ["Home", "Data Analysis", "About"]
)

if page == "Home":
    st.subheader("Home")
    st.write("Build your hackathon solution here!")

    name = st.text_input("Enter your name")

    if st.button("Submit"):
        if name.strip():
            st.success(f"Welcome, {name}!")
        else:
            st.warning("Please enter your name.")

elif page == "Data Analysis":
    st.subheader("Data Analysis")

    uploaded_file = st.file_uploader(
        "Upload a CSV file",
        type=["csv"]
    )

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        st.write("Dataset Preview")
        st.dataframe(df)

        st.write("Dataset Statistics")
        st.write(df.describe(include="all"))

        st.write("Missing Values")
        st.write(df.isnull().sum())

elif page == "About":
    st.subheader("About")
    st.write("A reusable starter application for AI hackathons.")