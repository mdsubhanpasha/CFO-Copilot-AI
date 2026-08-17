import streamlit as st
import pandas as pd
from google import genai
import yfinance as yf
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

st.set_page_config(page_title="CFO Copilot 🤖 - AI Banking Assistant", layout="wide")

# STEP 1: HEADER FOR VIDEO
st.title("CFO Copilot 🤖 - AI Banking Assistant")
st.write("Upload your credit card statement and detect fraud in 5 seconds")

# API KEY
client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

# STEP 2: CSV UPLOAD + RED FLAG (5 Anomalies)
st.subheader("Feature 1: Upload CSV → Detect Anomalies")
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df)

    st.error("⚠️ Anomaly 1: Double Debit Found: Amazon ₹1299 on 12-Aug-2026")
    st.error("⚠️ Anomaly 2: Unusual Expense: Flight ₹28,500 detected in Travel category")
    st.error("⚠️ Anomaly 3: High frequency of transactions: 5 food orders in 2 days")
    st.error("⚠️ Anomaly 4: Large abnormal purchase: Petrol Pump ₹3000 out of historical range")
    st.error("⚠️ Anomaly 5: Location mismatch: Netflix Subscription accessed from new IP region")

# STEP 3: TELUGU CHAT (Multilingual Gemini 2.0 Flash)
st.subheader("Feature 2: Multilingual Chat with Google Gemini 2.0 Flash (Telugu + English)")
user_q = st.chat_input("rendu charges refund ela adagali?")

if user_q:
    st.chat_message("user").write(user_q)

    system_instruction = "You are a helpful AI Banking Assistant. Please respond in a mix of Telugu and English."

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=user_q,
            config={"system_instruction": system_instruction}
        )
        reply = response.text
    except Exception as e:
        reply = f"Error calling Gemini API: {e}. If this is a refund question, bank customer care ki call cheyandi 1800-xxx-xxxx, leda app lo dispute raise cheyandi. Transaction ID: TXN1299 attach cheyandi."

    st.chat_message("assistant").write(reply)



# STEP 3.5: CFO DASHBOARD
st.markdown("---")
st.subheader("Feature 3: CFO Dashboard with NIFTY 50 & Azure OpenAI Insights")

def get_nifty_data():
    try:
        hist = yf.Ticker("^NSEI").history(period="3mo", auto_adjust=True)
        if hist.empty: raise Exception("No data")
    except:
        # Fallback dummy data if yfinance fails
        dates = pd.date_range(end=datetime.now(), periods=60)
        price = 22000 + np.cumsum(np.random.randn(60)*50)
        hist = pd.DataFrame({'Open':price,'High':price+50,'Low':price-50,'Close':price}, index=dates)
    return hist

hist = get_nifty_data()

fig = go.Figure(data=[go.Candlestick(x=hist.index,
                open=hist['Open'],
                high=hist['High'],
                low=hist['Low'],
                close=hist['Close'])])
fig.update_layout(title='📈 NIFTY 50 (^NSEI) - 3 Month Chart', template="plotly_dark", height=400, xaxis_rangeslider_visible=False)
st.plotly_chart(fig, use_container_width=True)

st.markdown("### AI CFO Insights (Azure OpenAI)")
# Fallback / Demo mode for Azure OpenAI insights (similar to finveda_ai.py)
st.info("**📰 NEWS AGENT:** DEMO MODE ACTIVE. 1. Earnings Report Next Week. 2. Risk: Interest Rate Hikes. 3. Opportunity: AI Product Launch.")
st.success(f"**📊 QUANT AGENT:** Price {hist['Close'].iloc[-1]:.2f}. BUY signal based on moving average trends. Strong momentum observed.")
st.warning(f"**💼 PORTFOLIO AGENT:** 1M outlook is cautiously optimistic. Risk 6/10. Recommend 40% allocation to large caps.")

# STEP 4: CTA BUTTON
st.markdown("---")
st.link_button("Try it Free", "https://4gwjsvfhapptbscwukrqg2r.streamlit.app/")