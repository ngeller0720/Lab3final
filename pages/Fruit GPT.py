import streamlit as st
import google.generativeai as genai
import requests

genai.configure(api_key=st.secrets["gemini"]["api_key"])
model = genai.GenerativeModel("gemini-1.5-flash")

@st.cache_data
def get_api_data():
    try:
        response = requests.get("https://fruityvice.com/api/fruit/all")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error("Failed to load API data. Check your connection or API endpoint.")
        return []

fruit_data = get_api_data()

fruit_facts = "\n".join([
    f"{fruit['name']}: {fruit['nutritions']}" for fruit in fruit_data
])

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("🍍 Fruit Nutrition Chatbot")

#display existing messages
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Ask me something about fruit nutrition!")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)

    st.session_state.chat_history.append({"role": "user", "content": user_input})

    prompt = (
        "You are a helpful nutrition assistant. Here is some fruit data you can use:\n"
        f"{fruit_facts}\n\n"
        f"User: {user_input}\nAssistant:"
    )

    # error handling
    try:
        response = model.generate_content(prompt)
        bot_reply = response.text.strip()

        with st.chat_message("assistant"):
            st.write(bot_reply)

        st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})

    except Exception as e:
        with st.chat_message("assistant"):
            st.error("⚠️ Sorry, something went wrong.")
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": "⚠️ Sorry, something went wrong."
        })