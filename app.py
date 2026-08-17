import streamlit as st
import pandas as pd
from google import genai

st.set_page_config(page_title="FinVeda AI", layout="wide")

# STEP 1: HEADER FOR VIDEO
st.title("FinVeda AI 🚀 - Your AI Banking Assistant")
st.write("Upload your credit card statement and detect fraud in 5 seconds")

# API KEY
client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

# STEP 2: CSV UPLOAD + RED FLAG
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df)

    # Fake demo anomaly for video
    st.error("⚠️ Double Debit Found: Amazon ₹1299 on 12-Aug-2025")
    st.warning("⚠️ Unusual Expense: Flight ₹28,500 detected")

# STEP 3: TELUGU CHAT
st.subheader("Ask AI in Telugu or English")
user_q = st.chat_input("rendu charges refund ela adagali?")

if user_q:
    st.chat_message("user").write(user_q)

    if "refund" in user_q.lower() or "refund" in user_q:
        reply = "Bank customer care ki call cheyandi 1800-xxx-xxxx, leda app lo dispute raise cheyandi. Transaction ID: TXN1299 attach cheyandi."
    else:
        response = client.models.generate_content(model="gemini-2.0-flash", contents=user_q)
        reply = response.text

    st.chat_message("assistant").write(reply)

# STEP 4: CTA BUTTON
st.markdown("---")
st.link_button("Try it Free", "https://4gwjsvfhapptbscwukrqg2r.streamlit.app/")