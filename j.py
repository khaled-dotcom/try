import streamlit as st
from groq import Groq
import os

# Use environment variable for security
os.environ["GROQ_API_KEY"] = "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"

# =====================
# 1. Laptop data
# =====================
laptop_data = [
    {
        "brand": "Dell XPS 13",
        "cpu": "Intel Core i7",
        "ram": "16GB",
        "storage": "512GB SSD",
        "gpu": "Intel Iris Xe",
        "features": ["Touchscreen", "Lightweight", "Good Battery"],
        "price": "$1200"
    },
    {
        "brand": "Microsoft Surface Laptop Studio",
        "cpu": "Intel Core i7",
        "ram": "32GB",
        "storage": "1TB SSD",
        "gpu": "NVIDIA RTX 3050 Ti",
        "features": ["Touchscreen", "Stylus Support", "Convertible"],
        "price": "$2200"
    },
    {
        "brand": "Apple MacBook Air M2",
        "cpu": "Apple M2",
        "ram": "8GB",
        "storage": "256GB SSD",
        "gpu": "Integrated",
        "features": ["Lightweight", "Long Battery Life"],
        "price": "$999"
    },
    {
        "brand": "HP Spectre x360",
        "cpu": "Intel Core i7",
        "ram": "16GB",
        "storage": "1TB SSD",
        "gpu": "Intel Iris Xe",
        "features": ["Touchscreen", "Stylus Support", "Convertible"],
        "price": "$1500"
    }
]

laptop_data_str = "\n".join([str(laptop) for laptop in laptop_data])

# =====================
# 2. Initialize Groq client
# =====================
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# =====================
# 3. Streamlit UI
# =====================
st.set_page_config(page_title="khaled Laptop Chatbot", page_icon="💻", layout="centered")
st.title("khaled  Laptop Recommendation Chatbot")
st.write("Ask me anything about laptops from our store!")

# Store chat messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Query Groq API with STRICT rules
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": (
                    f"You are a strict laptop store assistant. Only answer questions "
                    f"that are about the laptops in the store based on this data:\n{laptop_data_str}\n"
                    f"If a user asks about anything else (not related to these laptops), politely respond: "
                    f'\"Sorry, I can only help with laptops in our store.\"'
                ),
            },
            *[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]
        ]
    )
    response = completion.choices[0].message.content

    # Add assistant message
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

