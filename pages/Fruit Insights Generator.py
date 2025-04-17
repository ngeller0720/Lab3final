import streamlit as st
import requests
import google.generativeai as genai
import os

genai.configure(api_key=st.secrets["gemini"]["api_key"])

model = genai.GenerativeModel("gemini-1.5-flash")

@st.cache_data
def get_fruit_data():
    url = "https://www.fruityvice.com/api/fruit/all"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else []

data = get_fruit_data()
fruit_names = [fruit["name"] for fruit in data]

st.title("Fruit Insights Generator")

# User Inputs
fruit1 = st.selectbox("Choose the first fruit", fruit_names)
fruit2 = st.selectbox("Choose the second fruit", fruit_names)
detail_level = st.slider("Level of Detail", 1, 3, 2, help="1=Brief, 3=In-depth")

if st.button("Generate Comparison"):
    fruit1_data = next((f for f in data if f["name"] == fruit1), None)
    fruit2_data = next((f for f in data if f["name"] == fruit2), None)

    if fruit1_data and fruit2_data:
        prompt = (
            f"Compare the nutritional values of {fruit1} and {fruit2} based on this data:\n\n"
            f"{fruit1}: {fruit1_data['nutritions']}\n"
            f"{fruit2}: {fruit2_data['nutritions']}\n\n"
            f"Write a level-{detail_level} summary that highlights differences, health impacts, and tips."
        )

        with st.spinner("Thinking..."):
            response = model.generate_content(prompt)
            st.success("Here’s what Gemini says:")
            st.write(response.text)