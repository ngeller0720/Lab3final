import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import time

fruit_images = {
    "Apple":"Images/Apple.jpg",
    "Banana":"Images/Banana.jpg",
    "Persimmon":"Images/Persimmons.jpg",
    "Strawberry":"Images/Strawberry.jpg",
    "Tomato":"Images/Tomato.jpg",
    "Pear":"Images/Pear.jpg",
    "Durian":"Images/Durian.jpg",
    "Blackberry":"Images/Blackberry.jpg",
    "Lingonberry":"Images/Lingonberry.jpg",
    "Kiwi":"Images/Kiwi.jpg",
    "Lychee":"Images/Lychee.jpg",
    "Pineapple":"Images/Pineapple.jpg",
    "Fig":"Images/Fig.jpg",
    "Gooseberry":"Images/Gooseberry.jpg",
    "Passionfruit":"Images/Passionfruit.jpg",
    "Plum":"Images/Plum.jpg",
    "Orange":"Images/Orange.jpg",
    "GreenApple":"Images/GreenApple.jpg",
    "Raspberry":"Images/Raspberry.jpg",
    "Watermelon":"Images/Watermelons.jpg",
    "Lemon":"Images/Lemon.jpg",
    "Mango":"Images/Mango.jpg",
    "Blueberry":"Images/Blueberry.jpg",
    "Guava":"Images/Guava.jpg",
    "Apricot":"Images/Apricots.jpg",
    "Melon":"Images/Melon.jpg",
    "Tangerine":"Images/Tangerine.jpg",
    "Pitahaya":"Images/Pitahaya.jpg",
    "Lime":"Images/Lime.jpg",
    "Pomegranate":"Images/Pomegranate.jpg",
    "Dragonfruit":"Images/Dragonfruit.jpg",
    "Grape":"Images/Grape.jpg",
    "Morus":"Images/Morus.jpg",
    "Feijoa":"Images/Feijoa.jpg",
    "Avocado":"Images/avocado.jpg",
    "Kiwifruit":"Images/Kiwi.jpg",
    "Cranberry":"Images/cranberry.jpg",
    "Cherry":"Images/cherry.jpg",
    "Peach":"Images/Peach.jpg",
    "Jackfruit":"Images/Jackfruit.jpg",
    "Horned Melon":"Images/Hornedmelon.jpg",
    "Hazelnut":"Images/Hazelnuts.jpg",
    "Pomelo":"Images/Pomelo_fruit.jpg",
    "Mangosteen":"Images/Mango.jpg",
    "Pumpkin":"Images/Pumpkin.jpg",
    "Japanese Persimmon":"Images/Japanese Persimon.jpg",
    "Papaya":"Images/Papaya.jpg",
    "Annona":"Images/Annona.jpg",
    "Ceylon Gooseberry":"Images/CeylonGooseberry.jpg",
    }

st.set_page_config(page_title="Fruit Nutrition Analyzer 🍎", layout="centered")

st.title("🍓 Fruit Nutrition Analyzer")
st.markdown("Compare the nutritional content of your favorite fruits using real-time data from the Fruityvice API.")
@st.cache_data
def get_fruit_data():
    url = "https://www.fruityvice.com/api/fruit/all"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Could not load fruit data from the API.")
        return []

data = get_fruit_data()
fruit_names = [fruit["name"] for fruit in data]
selected_fruits = st.multiselect("Select fruits to compare:", fruit_names, default=["Apple", "Banana"])
nutrient_choice = st.selectbox("Choose a nutrient to visualize:", ["calories", "sugar", "carbohydrates", "protein", "fat"])
if selected_fruits:
    st.subheader("🖼️ Selected Fruit Images")
    cols = st.columns(len(selected_fruits))
    for i, fruit in enumerate(selected_fruits):
        with cols[i]:
            img_url = fruit_images.get(fruit)
            if img_url:
                st.image(img_url, caption=fruit, use_container_width=True)
            else:
                st.markdown(f"🚫 No image found for {fruit}")
st.write("---")
if selected_fruits:
    selected_data = [fruit for fruit in data if fruit["name"] in selected_fruits]
    df = pd.DataFrame({
        "Fruit": [f["name"] for f in selected_data],
        nutrient_choice.capitalize(): [f["nutritions"][nutrient_choice] for f in selected_data]
    })
    st.subheader(f"{nutrient_choice.capitalize()} Comparison")
    fig, ax = plt.subplots()
    ax.bar(df["Fruit"], df[nutrient_choice.capitalize()])
    ax.set_ylabel(f"{nutrient_choice.capitalize()} (g)")
    ax.set_xlabel("Fruit")
    ax.set_title(f"{nutrient_choice.capitalize()} in Selected Fruits")
    plt.xticks(rotation=45, ha='right')

    st.pyplot(fig)
    st.write("---")
    st.subheader("Full Nutritional Table")
    full_table = pd.DataFrame([{
        "Fruit": f["name"],
        **f["nutritions"]
    } for f in selected_data])
    st.dataframe(full_table.set_index("Fruit"))
    st.write("---")


    st.subheader("Summary Stats")
    st.metric("Highest Value", f'{df[nutrient_choice.capitalize()].max()} g')
    st.metric("Lowest Value", f'{df[nutrient_choice.capitalize()].min()} g')
    st.metric("Average Value", f'{df[nutrient_choice.capitalize()].mean():.2f} g')

else:
    st.info("Please select at least one fruit to begin analysis.")
st.write("---")


st.markdown("---")
st.title("📊 Daily Nutrient Intake Summary")
goals = {
    "calories": 2000,
    "sugar": 36,           
    "carbohydrates": 275,  
    "protein": 50,         
    "fat": 70              
}

if selected_fruits:
    total_nutrients = {key: 0 for key in goals}

    for fruit in selected_data:
        for nutrient in total_nutrients:
            total_nutrients[nutrient] += fruit["nutritions"].get(nutrient, 0)

    st.subheader("🧮 Total Nutrients from Selected Fruits:")
    col1, col2, col3 = st.columns(3)
    for i, (nutrient, total) in enumerate(total_nutrients.items()):
        col = [col1, col2, col3][i % 3]
        percent = total / goals[nutrient] * 100
        col.metric(f"{nutrient.capitalize()}", f"{total:.1f}g", f"{percent:.0f}% of daily goal")

    st.subheader("🍽️ Nutrient Intake Feedback")
    for nutrient, total in total_nutrients.items():
        percent = total / goals[nutrient]
        if percent < 0.3:
            st.warning(f"⚠️ You are low on **{nutrient}**: only {percent*100:.1f}% of your goal.")
        elif percent < 1.0:
            st.info(f"🟡 You're getting some **{nutrient}**, but still under 100% of the goal.")
        else:
            st.success(f"✅ You’ve met or exceeded your **{nutrient}** intake for today!")

    st.markdown("✅ Tip: Mix high-carb fruits like bananas with protein-rich ones like avocados for balance.")


